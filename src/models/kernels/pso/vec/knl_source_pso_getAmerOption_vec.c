// #define n_PATH %d
// #define n_PERIOD %d

// 编译时通过-DVEC_SIZE=4传入向量宽度, 默认float4
#ifndef VEC_SIZE
#define VEC_SIZE 4
#endif

// 动态定义向量类型和转换函数
#if VEC_SIZE == 1
    typedef float float_vec;
    typedef int int_vec;
    #define convert_float_vec(x) ((float)(x))
    #define SUM_VEC(v) (v)
#elif VEC_SIZE == 2
    typedef float2 float_vec;
    typedef int2 int_vec;
    #define convert_float_vec convert_float2
    #define SUM_VEC(v) (v.s0 + v.s1)
#elif VEC_SIZE == 4
    typedef float4 float_vec;
    typedef int4 int_vec;
    #define convert_float_vec convert_float4
    #define SUM_VEC(v) (v.s0 + v.s1 + v.s2 + v.s3)
#elif VEC_SIZE == 8
    typedef float8 float_vec;
    typedef int8 int_vec;
    #define convert_float_vec convert_float8
    #define SUM_VEC(v) (v.s0 + v.s1 + v.s2 + v.s3 + v.s4 + v.s5 + v.s6 + v.s7)
#elif VEC_SIZE == 16
    typedef float16 float_vec;
    typedef int16 int_vec;
    #define convert_float_vec convert_float16
    #define SUM_VEC(v) (v.s0 + v.s1 + v.s2 + v.s3 + v.s4 + v.s5 + v.s6 + v.s7 + \
                       v.s8 + v.s9 + v.sA + v.sB + v.sC + v.sD + v.sE + v.sF)
#else
    #error "Unsupported VEC_SIZE"
#endif

#define n_VecPath ((n_PATH + VEC_SIZE - 1) / VEC_SIZE)


__kernel void psoAmerOption_gb3_vec(
    __global const float_vec *St_vec,        // 向量化后的St，布局为[nPeriod, nVecPath]
    __global const float *pso,               // 位置矩阵 [nDim, nFish] 
    __global float *C_hat,                   // 输出成本 [nFish]
    const float r, 
    const float T, 
    const float K, 
    const char opt
){
    
    //global variables, one fish per thread (work-item), check for early aross, for all paths
    int gid = get_global_id(0);            //thread id, per fish
    int nParticle = get_global_size(0);    //number of fishes
    
    float dt = T / n_PERIOD;
    float tmp_cost = 0.0f;

    // 每个线程处理VEC_SIZE个路径 (Each thread handles VEC_SIZE paths)
    for (int vec_path=0; vec_path<n_VecPath; vec_path++){
        int_vec bound_idx = (int_vec)(n_PERIOD - 1);            // init to last period (exercise at maturity if no early crossing)
        int St_T_idx = (n_PERIOD-1) * n_VecPath + vec_path;
        float_vec early_excise = St_vec[St_T_idx];               // init to St path_i last period price

        /* OLD BUGGY CODE - BACKWARD ITERATION (INCORRECT!)
        // This loop iterated BACKWARD and found the LAST crossing instead of FIRST
        // Commented out on 2026-02-16 - caused 5x pricing error vs NumPy
        #pragma unroll 8
        for (int prd=n_PERIOD-1; prd>-1; prd--){
            float cur_fish_val = pso[gid + prd * nParticle];
            float_vec cur_St_val = St_vec[vec_path + prd * n_VecPath];
            int_vec cmp_mask = isgreaterequal((float_vec)cur_fish_val, cur_St_val);
            bound_idx = select(bound_idx, (int_vec)prd, cmp_mask);
            early_excise = select(early_excise, cur_St_val, cmp_mask);
        }
        */

        // FIXED: FORWARD iteration to find FIRST crossing (matches NumPy argmax behavior)
        // For American options, exercise at EARLIEST profitable opportunity
        #pragma unroll 8 //VEC_SIZE
        for (int prd=0; prd<n_PERIOD; prd++){  // FORWARD iteration: 0, 1, 2, ..., T-1
            float cur_fish_val = pso[gid + prd * nParticle];
            float_vec cur_St_val = St_vec[vec_path + prd * n_VecPath];

            // Vectorized comparison: check if particle >= St for each vector element
            int_vec cmp_mask = isgreaterequal((float_vec)cur_fish_val, cur_St_val);

            // Only update if we haven't found a crossing yet (still at initial value)
            // This ensures we capture the FIRST crossing, not subsequent ones
            int_vec not_found_yet = (bound_idx == (int_vec)(n_PERIOD - 1));
            int_vec condition = cmp_mask & not_found_yet;

            bound_idx = select(bound_idx, (int_vec)prd, condition);
            early_excise = select(early_excise, cur_St_val, condition);
        }

        // compute current path present value of simulated American option; then cumulate for average later
        // 计算当前向量路径组的期权价值
        float_vec payoffs = max((float_vec)(0.0f), (K - early_excise) * opt);
        float_vec discounts = exp(-r * (convert_float_vec(bound_idx) + 1) * dt);
        float_vec payoff_discount = payoffs * discounts;
        
        // 手动累加4个路径的值到标量tmp_cost
        tmp_cost += SUM_VEC(payoff_discount);
    }
    
    tmp_cost = tmp_cost / n_PATH;    // get average C_hat for current fish/thread investigation
    C_hat[gid] = tmp_cost;
}


