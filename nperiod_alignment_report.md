# nPeriod Alignment Issue in PSO Vec Kernels

**Generated from:** `test_report.md` (run date 2026-03-08)
**Affected kernels:** `vec` and `vec_fusion` variants only
**Scalar/hybrid kernels:** unaffected

---

## Root Cause

Three OpenCL kernel files contain loops that stride through the particle position array in steps of **4**, and one loop uses `#pragma unroll 8` on the `nPeriod` dimension.  Both impose hard alignment requirements on `nPeriod` (`= nDim`):

| Requirement | Reason |
|------------|--------|
| `nPeriod % 4 == 0` | `for (i = 0; i < n_Dim; i += 4)` — reads `.s0/.s1/.s2/.s3` at offsets `i, i+1, i+2, i+3`; last iteration goes **out of bounds** if `n_Dim % 4 ≠ 0` |
| `nPeriod % 8 == 0` | `#pragma unroll 8` on `nPeriod` loop — compiler emits a scalar remainder loop when `n_PERIOD % 8 ≠ 0`, collapsing SIMD throughput |

---

## Affected Kernel Files

### 1. `knl_source_pso_searchGrid_vec.c` — `searchGrid_f2f4` kernel

**Constraint: `nPeriod % 4 == 0`**

```c
// comment: "must be divisible by 4"
for (int i = 0; i < n_Dim; i += 4) {          // ← stride-4 loop
    int base_idx = i * nParticle + gid;
    pos.s0 = position[base_idx + 0 * nParticle];
    pos.s1 = position[base_idx + 1 * nParticle];
    pos.s2 = position[base_idx + 2 * nParticle];
    pos.s3 = position[base_idx + 3 * nParticle]; // ← reads dim i+3
```

If `n_Dim = 150`: last iteration `i = 148` reads dimension `151` — **2 elements past array end**.
If `n_Dim = 250`: last iteration `i = 248` reads dimension `251` — **2 elements past array end**.

Same stride-4 loop also appears in `update_gbest_pos_vec` within the same file.

---

### 2. `knl_source_pso_getAmerOption_vec.c` — `psoAmerOption_gb3_vec` kernel

**Constraint: `nPeriod % 8 == 0`** (for full SIMD throughput)

```c
#pragma unroll 8                                 // ← demands nPeriod % 8 == 0
for (int prd = 0; prd < n_PERIOD; prd++) {
    float cur_fish_val = pso[gid + prd * nParticle];
    float_vec cur_St_val = St_vec[vec_path + prd * n_VecPath];
    ...
}
```

When `n_PERIOD % 8 ≠ 0`, the compiler cannot fully unroll and generates a scalar remainder loop, stalling the SIMD pipeline per vector group iteration.

---

### 3. `knl_source_pso_fusion_vec.c` — `pso_vec` fused kernel

**Constraint: `nPeriod % 4 == 0`** (three separate loops) + **`nPeriod % 8 == 0`** (fitness loop)

This kernel fuses all three PSO stages. All three stride-4 patterns are present:

```c
/* Stage 1 — searchGrid */
#pragma unroll 8
for (int i = 0; i < n_Dim; i += 4) { ... }     // ← OOB if nDim % 4 ≠ 0

/* Stage 2 — fitness (getAmerOption) */
#pragma unroll 8
for (int prd = 0; prd < n_PERIOD; prd++) { ... } // ← remainder if nPERIOD % 8 ≠ 0

/* Stage 3 — update pbest */
#pragma unroll 8
for (int i = 0; i < n_Dim; i += 4) { ... }     // ← OOB if nDim % 4 ≠ 0
```

Plus `update_gbest_pos_vec` within the same file:

```c
for (int i = 0; i < n_Dim; i += 4) { ... }     // ← OOB if nDim % 4 ≠ 0
```

---

## Evidence from Test Report

### Cases with `nPeriod = 200` (200 % 4 = 0, 200 % 8 = 0) — vec f8 FASTER

| Test Case | Scalar (ms) | vec(f8) (ms) | Speedup |
|-----------|------------:|-------------:|--------:|
| ATM Put   (d=-50, 02SEP08) | 211.7 | 93.4 | **2.3x faster** |
| ATM Put   (d=-50, 29SEP08) | 212.7 | 82.2 | **2.6x faster** |
| OTM Put   (d=-25, 15SEP08) | 211.0 | 82.1 | **2.6x faster** |
| ITM Call  (d=+75, 15SEP08) | 494.1 | 192.2 | **2.6x faster** |
| ITM Put   (d=-75, 29SEP08) | 211.5 | 83.9 | **2.5x faster** |
| vOTM Put  (d=-15, 29SEP08) | 353.2 | 136.3 | **2.6x faster** |
| dOTM Put  (d=-10, 02SEP08) | 282.5 | 109.2 | **2.6x faster** |
| OTM Put   (S0=100,K=110,T=1y) | 693.9 | 267.7 | **2.6x faster** |
| ITM Put   (S0=100,K=105,T=1y) | 419.3 | 157.0 | **2.7x faster** |
| OTM Call  (S0=100,K=105,T=1y) | 1671.9 | 639.6 | **2.6x faster** |

### Cases with `nPeriod = 150` (150 % 4 = **2**, 150 % 8 = **6**) — vec f8 SLOWER

| Test Case | Scalar (ms) | vec(f8) (ms) | Degradation |
|-----------|------------:|-------------:|------------:|
| dITM Put  (d=-90, 29SEP08) | 170.5 | 2292.1 | **13.4x slower** |
| dITM Call (d=+90, 29SEP08) | 382.7 | 5295.0 | **13.8x slower** |

### Case with `nPeriod = 250` (250 % 4 = **2**, 250 % 8 = **2**) — vec f8 SLOWER

| Test Case | Scalar (ms) | vec(f8) (ms) | Degradation |
|-----------|------------:|-------------:|------------:|
| ATM Put   (S0=22.7,K=22.7,T=60d) | 968.0 | 14900.7 | **15.4x slower** |

> Note: All three failing cases still produce **correct prices** (pass the 15% tolerance test).
> The misalignment causes severe performance degradation, not incorrect results.

---

## Alignment Requirement Summary

| `nPeriod` | `% 4` | `% 8` | OOB in searchGrid? | Unroll penalty? | vec f8 outcome |
|----------:|:-----:|:-----:|:------------------:|:---------------:|:--------------|
| 200 | ✅ 0 | ✅ 0 | No | None | **~2.6x faster than scalar** |
| 160 | ✅ 0 | ✅ 0 | No | None | Expected ~2.6x faster |
| 240 | ✅ 0 | ✅ 0 | No | None | Expected ~2.6x faster |
| 150 | ❌ 2 | ❌ 6 | Yes (+2 elements) | Yes | **13–14x slower than scalar** |
| 250 | ❌ 2 | ❌ 2 | Yes (+2 elements) | Yes | **15x slower than scalar** |
| 256 | ✅ 0 | ✅ 0 | No | None | Expected ~2.6x faster |
| 248 | ✅ 0 | ✅ 0 | No | None | Expected ~2.6x faster |

---

## Recommended Fix

**Option A — Fix call site (no kernel changes):** Enforce the constraint in `test_pso.py` and any caller:

```python
# Before constructing hybridMonteCarlo, round nPeriod up to next multiple of 8
nPeriod = ((nPeriod + 7) // 8) * 8
```

**Option B — Fix kernel (handle remainder):** Add a scalar tail loop after the stride-4 loop to handle leftover dimensions when `n_Dim % 4 != 0`. Applies to all three kernel files listed above.

**Immediate action for current test suite:**

| Case | Current nPeriod | Suggested fix |
|------|---------------:|--------------|
| `dITM Put  (d=-90, 29SEP08)` | 150 | → **160** |
| `dITM Call (d=+90, 29SEP08)` | 150 | → **160** |
| `ATM Put   (S0=22.7,K=22.7,T=60d)` | 250 | → **248** or **256** |

---

*Report generated from `test_report.md` and kernel source analysis.*
