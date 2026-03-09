import os
import pandas as pd
import time
from src.models.mc import hybridMonteCarlo
from src.models.longstaff import LSMC_Numpy, LSMC_OpenCL
import src.models.benchmarks as bm
from src.models.pso import PSO_Numpy, PSO_OpenCL_hybrid, PSO_OpenCL_scalar, PSO_OpenCL_vec,PSO_OpenCL_scalar_fusion,PSO_OpenCL_vec_fusion

from src.models.utils import checkOpenCL
import argparse

#===config file=====



def run_models_on_row(row):
    """
    Runs a suite of pricing models on a single row of option data.
    This version is modified to only run the PSO_OpenCL_scalar_fusion model,
    with other PSO variations commented out for focused testing.
    """
    nPath = 10000
    nPeriod = 250
    nFish = 10000
    # Extract parameters from the row
    T = row['days']/ 365
    S0 = row['forward_price']
    r = row['_3_MO'] / 100  # Convert % to decimal
    sigma = row['impl_volatility']
    K = row['strike_price']
    opttype = row['cp_flag'].upper()

    timings = {}
    
    try:
        # --- Standard Models ---
        
        # Monte Carlo Initialization
        start_mc = time.time()
        mc = hybridMonteCarlo(S0, r, sigma, T, nPath, nPeriod, K, opttype, nFish)
        timings['mc_setup'] = time.time() - start_mc

        # Binomial
        start_binomial = time.time()
        binomial = bm.binomialAmericanOption(S0, K, r, sigma, nPeriod, T, opttype)
        timings['binomial'] = time.time() - start_binomial

        # LSMC Numpy
        start_lsmc_np = time.time()
        lsmc_np = LSMC_Numpy(mc)
        lsmc_val_np = float(lsmc_np.longstaff_schwartz_itm_path_fast()[0])
        timings['lsmc_np'] = time.time() - start_lsmc_np

        # LSMC OpenCL
        start_lsmc_cl = time.time()
        lsmc_cl = LSMC_OpenCL(mc)
        lsmc_val_cl = float(lsmc_cl.longstaff_schwartz_itm_path_fast_hybrid()[0])
        timings['lsmc_cl'] = time.time() - start_lsmc_cl

        # --- PSO Models (only scalar_fusion is active) ---

        # PSO Numpy (commented out)
        pso_val_np = 0
        timings['pso_np'] = 0
        # start_pso_np = time.time()
        # pso_np = PSO_Numpy(mc, nFish, mc.costPsoAmerOption_np)
        # pso_val_np = pso_np.solvePsoAmerOption_np()
        # timings['pso_np'] = time.time() - start_pso_np

        # PSO OpenCL hybrid (commented out)
        p_pso_cl_hy = 0
        timings['pso_cl_hy'] = 0
        # start_pso_cl_hy = time.time()
        # pso_cl_hy = PSO_OpenCL_hybrid(mc, nFish)
        # p_pso_cl_hy = pso_cl_hy.solvePsoAmerOption_cl()
        # timings['pso_cl_hy'] = time.time() - start_pso_cl_hy

        # PSO OpenCL scalar (commented out)
        p_pso_cl_sc = 0
        timings['pso_cl_sc'] = 0
        # start_pso_cl_sc = time.time()
        # pso_cl_sc = PSO_OpenCL_scalar(mc, nFish, direction='backward')
        # p_pso_cl_sc = pso_cl_sc.solvePsoAmerOption_cl()
        # timings['pso_cl_sc'] = time.time() - start_pso_cl_sc

        # PSO OpenCL vec (commented out)
        p_pso_cl_vec = 0
        timings['pso_cl_vec'] = 0
        # start_pso_cl_vec = time.time()
        # pso_cl_vec = PSO_OpenCL_vec(mc, nFish, vec_size=4)
        # p_pso_cl_vec = pso_cl_vec.solvePsoAmerOption_cl()
        # timings['pso_cl_vec'] = time.time() - start_pso_cl_vec
        
        # PSO OpenCL vec fusion (commented out)
        p_pso_cl_vec_f = 0
        timings['p_pso_cl_vec_func'] = 0
        # start_pso_cl_vec_fusion = time.time()
        # pso_cl_vec_fusion = PSO_OpenCL_vec_fusion(mc, nFish)
        # p_pso_cl_vec_f = pso_cl_vec_fusion.solvePsoAmerOption_cl()
        # timings['p_pso_cl_vec_func'] = time.time() - start_pso_cl_vec_fusion

        # --- Active Model: PSO OpenCL scalar fusion ---
        start_pso_cl_sc_fusion = time.time()
        pso_cl_sc_fusion = PSO_OpenCL_scalar_fusion(mc, nFish)
        p_pso_cl_sc_f = pso_cl_sc_fusion.solvePsoAmerOption_cl()
        timings['pso_cl_sc_fun'] = time.time() - start_pso_cl_sc_fusion
        
        # Cleanup OpenCL resources
        mc.cleanUp()
        #lsmc_cl.cleanUp()
        #pso_cl_sc_fusion.cleanUp()
        # pso_cl_hy.cleanUp()
        # pso_cl_sc.cleanUp()
        # pso_cl_vec.cleanUp()
        # pso_cl_vec_fusion.cleanUp()

        # Return all results as a pandas Series
        return pd.Series([
            binomial, lsmc_val_np, lsmc_val_cl, pso_val_np, p_pso_cl_hy, p_pso_cl_sc, p_pso_cl_vec, p_pso_cl_sc_f, p_pso_cl_vec_f,
            timings['mc_setup'], timings['binomial'], timings['lsmc_np'],
            timings['lsmc_cl'], timings['pso_np'], timings['pso_cl_hy'], timings['pso_cl_sc'], timings['pso_cl_vec'], timings['pso_cl_sc_fun'],
            timings['p_pso_cl_vec_func']
        ])

    except Exception as e:
        print(f"Error processing row: {e}")
        # Return a series of Nones with the correct length if an error occurs
        return pd.Series([None]*19)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run pricing models on a CSV input file")
    parser.add_argument("input_file", type=str, help="Path to input CSV file")
    parser.add_argument("output_file", type=str, help="Path to output CSV file")
    args = parser.parse_args()

    # Construct full paths relative to the script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(script_dir, 'Data')
    input_path = args.input_file if os.path.isabs(args.input_file) else os.path.join(base_path, args.input_file)
    output_path = args.output_file if os.path.isabs(args.output_file) else os.path.join(base_path, args.output_file)
    
    # Check for OpenCL devices
    checkOpenCL()
    
    # Define columns to keep from the input file
    columns_to_keep = [
    'secid', 'date', 'cp_flag', 'days', 
    'impl_volatility', 'strike_price', 'premium',
     '_3_MO', 'forward_price'
    ]   
    
    # Load and filter input data
    df = pd.read_csv(input_path)
    df = df[columns_to_keep]

    # Apply models row-by-row
    print("Running pricing models on each row...")

    # Define column names for the output results
    model_columns = [
        'binomial', 'lsmc_cpu', 'lsmc_gpu', 'pso_cpu', 'pso_gpu_hybrid', 
        'pso_gpu_scalar', 'pso_gpu_vector', 'pso_gpu_scalar_fusion', 'pso_gpu_vector_fusion',
        'time_mc_setup', 'time_binomial', 'time_lsmc_cpu', 'time_lsmc_gpu', 
        'time_pso_cpu', 'time_pso_gpu_hybrid', 'time_pso_gpu_scalar', 
        'time_pso_gpu_vector', 'time_pso_gpu_scalar_fusion', 'time_pso_gpu_vector_fusion'
    ]

    # Apply the function and assign the new column names
    model_results = df.apply(run_models_on_row, axis=1)
    model_results.columns = model_columns

    # Combine original data with model output
    df_final = pd.concat([df, model_results], axis=1)

    # Save results to the specified output file
    if output_path.endswith('.xlsx'):
        import openpyxl
        df_final.to_excel(output_path, index=False, engine='openpyxl')
        print(f"✅ Done. Results saved to Excel file: {output_path}")
    else:
        df_final.to_csv(output_path, index=False)
        print(f"✅ Done. Results saved to CSV file: {output_path}")
