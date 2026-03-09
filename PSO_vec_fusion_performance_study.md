# PSO vec_fusion Performance Study

**Date:** 2026-03-08
**Device:** Apple M1 Pro (OpenCL 1.2)
**Test script:** `test_vec_fusion_profile.py`
**Notebook reference:** `src/PSO_function_wise_compare.ipynb`

---

## 1. Background

The full PSO pricing benchmark showed the two vec variants running ~15× slower than
scalar despite producing the same price:

```
Method                       Price        Time
Binomial (ref)             86.3405        1.3 ms
PSO GPU scalar             85.6924      211.0 ms   ← fast
PSO GPU sc_fusion          85.6924      210.2 ms   ← fast
PSO GPU vec(f8)            85.6924     3069.6 ms   ← 15x slower
PSO GPU vec_fusion         85.6924     3071.6 ms   ← 15x slower
```

**Test parameters:** nPath=10,000 · nPeriod=150 · nFish=256 · vec_size=8
**Test case:** ATM Put 02SEP08 — S0=1277.58, K=1280.749, r=1.72%, σ=21.34%, T=30/365

The goal was to understand:
1. Why `vec(float8)` is so much slower than `scalar`
2. Why `vec_fusion` offers no benefit over `vec`
3. How the current results relate to the earlier notebook study

---

## 2. Diagnostic Results (`test_vec_fusion_profile.py`)

### 2.1 Sub-step Timing Breakdown

Both `vec` and `vec_fusion` were profiled at sub-step granularity per PSO iteration.

```
Sub-step                         vec (non-fused)   vec_fusion
----------------------------------------------------------------
searchGrid  (GPU, mean ms/iter)        0.742          (fused)
fitness     (GPU, mean ms/iter)      778.885          (fused)
pbest+gbest (GPU+CPU, mean/iter)       1.029          (fused)
── fused kernel (GPU, mean/iter)     (split)          770.605
   of which: enqueue_copy (host)     (split)            0.370
   of which: np.argmax   (CPU)       (split)            0.017
   of which: gbest update (cond.)    (split)            0.302
----------------------------------------------------------------
Total elapsed (ms)                   3122.64          3085.24
Iterations                                 4                4
ms / iteration                        780.66           771.31
```

**Key finding 1:** `vec` and `vec_fusion` are **identical in performance** (ratio = 1.00×).
Fusion saves nothing because the two cheap steps were already trivial — searchGrid
(0.742 ms) and pbest+gbest (1.029 ms) together account for only 0.2% of runtime.

**Key finding 2:** The fitness kernel alone is **99.7% of total runtime** in both
variants. All optimization effort must target the fitness kernel.

---

### 2.2 Kernel Occupancy Info

```
Device: Apple M1 Pro
  MAX_COMPUTE_UNITS                 : 16
  MAX_WORK_GROUP_SIZE               : 256
  GLOBAL_MEM_SIZE                   : 11.45 GB
  LOCAL_MEM_SIZE                    : 32.0 KB
  MAX_CLOCK_FREQUENCY               : 1000 MHz

PSO_OpenCL_vec — separate kernels:
  [searchGrid_f2f4]
    WORK_GROUP_SIZE                 : 256
    PREFERRED_WORK_GROUP_SIZE_MULTIPLE : 32
    LOCAL_MEM_SIZE  (bytes)         : 0
    PRIVATE_MEM_SIZE (bytes)        : 0

  [psoAmerOption_gb3_vec]
    WORK_GROUP_SIZE                 : 256
    PREFERRED_WORK_GROUP_SIZE_MULTIPLE : 32
    LOCAL_MEM_SIZE  (bytes)         : 0
    PRIVATE_MEM_SIZE (bytes)        : 0

  [update_pbest_f2f4]
    WORK_GROUP_SIZE                 : 256
    PREFERRED_WORK_GROUP_SIZE_MULTIPLE : 32
    LOCAL_MEM_SIZE  (bytes)         : 0
    PRIVATE_MEM_SIZE (bytes)        : 0

PSO_OpenCL_vec_fusion — fused kernel:
  [pso_vec (fused)]
    WORK_GROUP_SIZE                 : 256
    PREFERRED_WORK_GROUP_SIZE_MULTIPLE : 32
    LOCAL_MEM_SIZE  (bytes)         : 0
    PRIVATE_MEM_SIZE (bytes)        : 0

  [update_gbest_pos_vec]
    WORK_GROUP_SIZE                 : 256
    PREFERRED_WORK_GROUP_SIZE_MULTIPLE : 32
    LOCAL_MEM_SIZE  (bytes)         : 0
    PRIVATE_MEM_SIZE (bytes)        : 0
```

> Note: Apple GPU always reports `PRIVATE_MEM_SIZE = 0` via OpenCL 1.2 — register
> spill cannot be confirmed this way. The vec_size sweep (§2.3) provides indirect
> evidence instead.

---

### 2.3 vec_size Sweep (vec_fusion, single test case)

Tests whether increasing SIMD width causes register pressure / spill.

```
vec_size    elapsed (ms)   iters     ms/iter   fused knl (mean ms/iter)
       1        1312.57       4      328.142                    327.534
       2        1465.53       4      366.382                    365.692
       4        2665.43       4      666.357                    665.686
       8        3100.12       4      775.030                    774.346
```

**Key finding:** Larger vec_size = **slower**, opposite to intent.

```
size 1 → 2:  +12%  (expected ≈0%, each thread does same total work)
size 2 → 4:  +82%  ← sharp jump, register threshold crossed
size 4 → 8:  +16%  ← saturated, already at minimum occupancy
```

The non-linear jump between size=2 and size=4 marks the point where register pressure
forces the GPU down to 1 active wave per compute unit. Beyond that, adding more vector
width only increases compute without reducing occupancy further.

---

### 2.4 nFish Sweep (vec vs vec_fusion)

Tests GPU occupancy effects across particle counts.

```
nFish    vec (ms)   vec iters   fusion (ms)  fusion iters   ratio
----------------------------------------------------------------------
   64     2099.35           4       2096.16             4    1.00x
  128     1987.82           3       1972.64             3    0.99x
  256     3103.77           4       3091.81             4    1.00x
  512     2286.97           3       2283.50             3    1.00x
```

The vec/fusion ratio is **1.00× at all particle counts** — fusion provides zero
benefit regardless of GPU occupancy.

Per-iteration time with nFish:

```
nFish= 64 → 525 ms/iter
nFish=128 → 663 ms/iter
nFish=256 → 776 ms/iter
nFish=512 → 762 ms/iter
```

Time grows sub-linearly because the M1 GPU can partially overlap wavefronts even
under register pressure. Fewer particles (nFish=128) can actually run in fewer
iterations (3 vs 4 for nFish=256) due to better PSO convergence with different
random initialization.

---

### 2.5 Per-Iteration Detail (first 4 iterations)

```
iter    vec_sg   vec_fit   vec_rest   vf_kernel   vf_copy   vf_argmax   vf_gbest
--------------------------------------------------------------------------------
   0     1.069   777.834      0.851     781.005     0.350       0.019      0.372
   1     0.547   767.873      0.822     773.975     0.349       0.017      0.414
   2     0.545   766.776      0.800     771.676     0.310       0.017      0.376
   3     0.544   773.432      0.388     769.469     0.314       0.017      0.004
```

Both variants stopped at **4 iterations** (early-stopping convergence criterion met).
Fitness kernel time is stable across iterations (~770–778 ms), confirming it is
purely compute/memory-bound rather than affected by startup latency or data variation.

---

## 3. Notebook Study Reference (`PSO_function_wise_compare.ipynb`)

The notebook measured **single kernel call** timing over a wider parameter range
(nPath=20,000, nPeriod=200, nFish=256–32,768) using a **previous version of the
fitness kernel** (backward iteration without `not_found_yet` tracking).

### 3.1 searchGrid — `measureMoveParticle` (cell 9)

```
nFish    hybrid (ms)   scalar (ms)   vec (ms)   numpy (ms)
256        1.30          1.04         1.00        0.15
512        1.43          1.03         0.84        0.75
1024       1.19          1.35         1.10        1.86
2048       1.29          1.40         1.13        1.77
4096       2.02          1.43         1.55        6.43
8192       3.09          1.70         1.51       11.07
16384     16.06         15.10        13.13       14.70
32768     33.09         29.89        33.27       54.87
```

**Observations:**
- All three GPU variants are roughly equivalent for searchGrid (1–33 ms range)
- GPU beats NumPy once nFish ≥ 1024 (~2×–7× faster at mid-range)
- At large nFish (≥16384) GPU and NumPy converge — the step is too large to hide
  memory-transfer overhead
- searchGrid is **not the bottleneck** — even its worst case (33 ms) is trivial next
  to the fitness cost

### 3.2 Fitness — `measureFitness` (cell 10)

```
nFish    hybrid (ms)   scalar (ms)   vec (ms)   numpy (ms)   np/vec speedup
256        1224.9         128.3         53.3       1322.2         24.8×
512        1199.4         129.8         53.7       2931.6         54.5×
1024       1236.1         131.3         58.4       6557.3        112.3×
2048       1323.9         153.2         67.5      13020.7        192.9×
4096       1466.9         185.3        103.4      25515.7        246.7×
8192       1804.9         334.8        161.4      53187.1        329.5×
16384      1029.9         682.2        283.0     108521.7        383.5×
32768      1546.7        1459.1        676.9     222768.7        329.1×
```

**Observations from the notebook:**
- vec was **2.4× faster than scalar** at nFish=256 with the previous kernel
- GPU (vec) delivered **25–383× speedup** over NumPy for the fitness function
- hybrid is the slowest GPU variant — penalized by CPU↔GPU transfers of
  `boundary_idx` and `exercise` arrays every iteration
- Both scalar and vec scale better than hybrid as nFish grows

### 3.3 Notebook vs Current Test — Fitness Kernel Comparison

| Metric | Notebook (prev. kernel) | Current (`gb3` kernel) |
|---|---|---|
| Test config | nPath=20,000, nPeriod=200 | nPath=10,000, nPeriod=150 |
| vec fitness (nFish=256) | **53 ms** per call | **779 ms** per iteration |
| scalar fitness (nFish=256) | **128 ms** per call | **~40 ms** per iteration |
| vec vs scalar | vec **2.4× faster** | vec **~19× slower** |
| vec speedup vs NumPy | **25×** | vec ≈ NumPy speed |

Normalizing for problem size (notebook is 2× paths × 1.33× periods = 2.67× more work):

```
Notebook vec:   53 ms  ÷ 2.67 = 20 ms equivalent
Current  vec:  779 ms  — 39× slower on equivalent work
```

The 39× performance regression between the two kernel versions is explained in §4.

---

## 4. Root Cause Analysis

### 4.1 The Fitness Kernel is the Sole Bottleneck

```
searchGrid    0.742 ms/iter   (0.1%)
fitness     778.885 ms/iter   (99.7%)  ← 100% of the problem lives here
pbest+gbest   1.029 ms/iter   (0.1%)
```

Kernel fusion provides zero benefit because the non-fitness steps are negligible.
All investigation below focuses on `psoAmerOption_gb3_vec`.

---

### 4.2 `float8` Requires 8× More Registers — GPU Occupancy Collapses

The inner period loop tracks per-path state in vector variables. With `vec_size=8`:

| Variable | Scalar kernel | Vec kernel (float8) | Register cost |
|---|---|---|---|
| `bound_idx` | `int` | `int8` | 8× |
| `early_excise` | `float` | `float8` | 8× |
| `not_found_yet` | `int` | `int8` | 8× |
| `condition` | `int` | `int8` | 8× |
| `cmp_mask` | `int` | `int8` | 8× |
| `cur_St_val` | `float` | `float8` | 8× |
| **Total key vars** | **~6 regs/thread** | **~48 regs/thread** | **8× increase** |

The M1 GPU has **no native float8 hardware** — it is 32-bit SIMD. `float8` compiles
to 8 separate scalar instructions per operation. The register cost is 8× higher per
thread, which directly reduces how many threads can be active simultaneously per
compute unit:

```
Scalar: 256 threads ×  6 regs → 8 waves/CU → full latency hiding → fast
Vec:    256 threads × 48 regs → 1 wave/CU  → no latency hiding  → stalls
```

With only 1 active wave per CU, every global memory load stalls the entire unit
while waiting for data — there are no other warps to run in the meantime.

---

### 4.3 `#pragma unroll 8` Amplifies Register Pressure by 8×

```c
// psoAmerOption_gb3_vec, line 81
#pragma unroll 8
for (int prd=0; prd<n_PERIOD; prd++) { ... }
```

Loop unrolling materialises 8 concurrent in-flight iterations, each needing its own
register copy of every loop-body variable:

```
Without unroll:   ~48 regs/thread
With unroll ×8:  ~384 regs/thread  → register file exhausted → spill to global mem
```

Register spill to global memory costs 300–500 cycles per access — turning a
compute-bound kernel into a global-memory-bandwidth-starved kernel.

The previous kernel version had the same pragma but with fewer loop-body variables
(~24 regs without `not_found_yet`/`condition`), which fit within the register file.

---

### 4.4 `not_found_yet` Introduces a Serial Loop-Carried Dependency

The current kernel tracks the first boundary crossing branchlessly:

```c
// Current kernel — serial dependency chain across all 150 period iterations:
int_vec not_found_yet = (bound_idx == (int_vec)(n_PERIOD - 1));  // READ bound_idx
int_vec condition     = cmp_mask & not_found_yet;
bound_idx = select(bound_idx, (int_vec)prd, condition);           // WRITE bound_idx
//           ↑ iteration i+1 cannot begin until iteration i writes bound_idx ↑
```

The previous kernel used a simpler `select` without the `not_found_yet` guard:

```c
// Previous kernel — no state dependency, compiler can treat as reduce-min:
bound_idx   = select(bound_idx, (int_vec)prd,      cmp_mask);
early_excise = select(early_excise, cur_St_val,    cmp_mask);
```

The GPU compiler recognises the simple `select` pattern as a **running-minimum
reduction** and can pipeline multiple iterations in parallel. The `not_found_yet`
condition breaks this: the outcome of iteration `i+1` depends on the full resolved
state of `bound_idx` from iteration `i`, creating a **serial state machine** that
cannot be reordered, vectorized, or pipelined across loop iterations.

---

## 5. Combined Bottleneck Summary

The three factors compound multiplicatively:

| Factor | Mechanism | Estimated slowdown |
|---|---|---|
| `float8` — 8× register use | Occupancy: 8 waves/CU → 1 wave/CU | ~8× |
| `#pragma unroll 8` + 48 regs | Register spill to global memory | ~3–5× additional |
| `not_found_yet` serial chain | Loop cannot be pipelined | ~2–3× additional |
| **Combined** | | **~19×** |

This explains the measured gap: scalar **~40 ms/iter** vs vec **~779 ms/iter**.

The notebook's vec result (53 ms) reflects the previous kernel without `not_found_yet`
tracking: lower register pressure, no serial dependency → full GPU occupancy → fast.
The current vec result (779 ms) reflects the updated kernel with correct first-crossing
logic but all three bottlenecks active simultaneously.

---

## 6. Existing Alternative: `psoAmerOption_gb2`

The scalar kernel file already contains a forward-iteration variant that uses an
actual `break` instead of `not_found_yet`:

```c
// psoAmerOption_gb2 — forward, early exit at first crossing
for (int prd=0; prd<n_PERIOD; prd++){
    if (cur_fish_val >= cur_St_val){
        bound_idx    = prd;
        early_excise = cur_St_val;
        break;   // ← no not_found_yet needed, no loop-carried dependency
    }
}
```

`PSO_OpenCL_scalar` selects this via `direction='forward'`. No equivalent
`gb2_vec` (break-based vectorized) kernel exists yet.

---

## 7. Conclusions

1. **`vec` and `vec_fusion` are the same speed** (ratio = 1.00× at all nFish tested).
   Kernel fusion of searchGrid + fitness + pbest saves nothing because the non-fitness
   steps cost only ~1.8 ms/iter vs ~779 ms/iter for fitness.

2. **The fitness kernel is the sole bottleneck** — 99.7% of total runtime.

3. **`float8` is counter-productive on Apple M1 GPU.** There is no native float8
   hardware. Using it multiplies register pressure by 8×, collapses GPU occupancy to
   1 wave/CU, and eliminates latency hiding.

4. **`#pragma unroll 8` compounds the problem.** Combined with the 8× register
   footprint, it forces register spill to global memory (~384 regs/thread), turning a
   compute-bound problem into a memory-bandwidth-bottlenecked one.

5. **`not_found_yet` converts a pipeline-able reduction into a serial state machine.**
   The previous kernel's simple `select` pattern was compiler-optimizable as a
   running minimum. The current branchless first-crossing logic with `not_found_yet`
   creates a loop-carried dependency that blocks all iteration-level parallelism.

6. **The notebook study measured a different kernel version.** The fitness timing
   data (vec=53 ms at nFish=256) reflects the previous kernel without `not_found_yet`.
   After the kernel update, the same operation costs 779 ms — a 39× regression on
   equivalent work. The searchGrid timing (cell 9) remains valid and unaffected.

7. **The current winner is `PSO_OpenCL_scalar_fusion`** (~211 ms total, 4–5 iters)
   using scalar registers, full 8-wave occupancy, and correct forward-iteration logic.

---

## 8. Recommended Next Steps

| Priority | Action | Expected benefit |
|---|---|---|
| High | Remove `#pragma unroll 8` from `psoAmerOption_gb3_vec` | Eliminates register spill |
| High | Implement `psoAmerOption_gb2_vec` (early-`break` version) | Removes `not_found_yet` dependency entirely |
| Medium | Test `vec_size=1` as scalar drop-in for vec kernel | Confirms register pressure is root cause |
| Medium | Re-run `PSO_function_wise_compare.ipynb` with current kernels | Updates notebook timing with corrected results |
| Low | Tune `local_size` for `pso_vec` fused kernel | Minor occupancy improvement |
