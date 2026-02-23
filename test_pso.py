"""
PSO & LSMC American Option Pricing - Multi-case test runner.
Run with: python test_pso.py
"""
import sys
import numpy as np
from pathlib import Path

# Path setup
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from src.models.mc import hybridMonteCarlo
import src.models.benchmarks as bm
from src.models.longstaff import LSMC_Numpy, LSMC_OpenCL
from src.models.pso import (
    PSO_Numpy,
    PSO_OpenCL_hybrid,
    PSO_OpenCL_scalar,
    PSO_OpenCL_scalar_fusion,
    PSO_OpenCL_vec,
    PSO_OpenCL_vec_fusion,
)

# ── Test cases ────────────────────────────────────────────────────────────────
# name, S0, K, r, sigma, T, opttype, nPath, nPeriod, nFish
TEST_CASES = [
    ("OTM Put  (S0=100, K=110, T=1y)",   100.0,    110.0, 0.03,   0.30,        1.0,      "P", 20000, 200, 256),
    ("ATM Put  (S0=22.7, K=22.7, T=60d)", 22.7389, 22.7389, 0.0102, 0.502026, 60/365,   "P", 10000, 250, 512),
    ("ITM Put  (S0=100, K=105, T=1y)",   100.0,    105.0, 0.03,   0.20,        1.0,      "P", 20000, 200, 256),
    ("OTM Call (S0=100, K=105, T=1y)",   100.0,    105.0, 0.05,   0.25,        1.0,      "C", 20000, 200, 256),
]

TOLERANCE = 0.15   # allow up to 15% relative error vs binomial (MC variance at these path counts)

# ── Helpers ───────────────────────────────────────────────────────────────────
def _rel_err(price, ref):
    return abs(price - ref) / ref if ref > 1e-8 else abs(price - ref)

def _pass(price, ref):
    return "PASS" if _rel_err(price, ref) <= TOLERANCE else "FAIL"

def run_case(name, S0, K, r, sigma, T, opttype, nPath, nPeriod, nFish):
    print(f"\n{'='*72}")
    print(f"  {name}")
    print(f"  S0={S0:.4f}  K={K:.4f}  r={r:.4f}  sigma={sigma:.4f}  "
          f"T={T:.4f}y  nPath={nPath}  nPeriod={nPeriod}  nFish={nFish}")
    print(f"{'='*72}")

    # ── Reference ─────────────────────────────────────────────────────────────
    binomial, t_bin = bm.binomialAmericanOption(S0, K, r, sigma, nPeriod, T, opttype)

    # ── Monte Carlo setup ─────────────────────────────────────────────────────
    mc = hybridMonteCarlo(S0, r, sigma, T, nPath, nPeriod, K, opttype, nFish)

    lsmc_results = []
    pso_results  = []

    # ── LSMC ──────────────────────────────────────────────────────────────────
    lsmc_np = LSMC_Numpy(mc)
    p_lsmc_np, t_lsmc_np = lsmc_np.longstaff_schwartz_itm_path_fast()
    lsmc_results.append(("LSMC NumPy",    float(p_lsmc_np), t_lsmc_np))

    lsmc_cl = LSMC_OpenCL(mc, preCalc="optimized")
    p_lsmc_cl, t_lsmc_cl = lsmc_cl.longstaff_schwartz_itm_path_fast_hybrid()
    lsmc_results.append(("LSMC GPU",      float(p_lsmc_cl), t_lsmc_cl))

    # ── PSO ───────────────────────────────────────────────────────────────────
    pso_np = PSO_Numpy(mc, nFish)
    p_np, t_np, _, _, _ = pso_np.solvePsoAmerOption_np()
    pso_results.append(("PSO NumPy",          float(p_np), t_np))

    pso_hy = PSO_OpenCL_hybrid(mc, nFish)
    p_hy, t_hy, _, _, _ = pso_hy.solvePsoAmerOption_cl()
    pso_results.append(("PSO GPU hybrid",     float(p_hy), t_hy))

    pso_sc = PSO_OpenCL_scalar(mc, nFish)
    p_sc, t_sc, _, _, _ = pso_sc.solvePsoAmerOption_cl()
    pso_results.append(("PSO GPU scalar",     float(p_sc), t_sc))

    pso_sf = PSO_OpenCL_scalar_fusion(mc, nFish)
    p_sf, t_sf, _, _ = pso_sf.solvePsoAmerOption_cl()
    pso_results.append(("PSO GPU sc_fusion",  float(p_sf), t_sf))

    pso_vc = PSO_OpenCL_vec(mc, nFish, vec_size=8)
    p_vc, t_vc, _, _, _ = pso_vc.solvePsoAmerOption_cl()
    pso_results.append(("PSO GPU vec(f8)",    float(p_vc), t_vc))

    pso_vf = PSO_OpenCL_vec_fusion(mc, nFish, vec_size=8)
    p_vf, t_vf, _, _ = pso_vf.solvePsoAmerOption_cl()
    pso_results.append(("PSO GPU vec_fusion", float(p_vf), t_vf))

    mc.cleanUp()

    # ── Print table ───────────────────────────────────────────────────────────
    W = 66
    print(f"\n  {'Method':<24} {'Price':>9}  {'Time':>10}  {'RelErr':>8}  Status")
    print(f"  {'-'*W}")
    print(f"  {'Binomial (ref)':<24} {binomial:>9.4f}  {t_bin*1e3:>9.1f} ms")
    print(f"  {'-'*W}")
    for group_label, group in [("── LSMC", lsmc_results), ("── PSO", pso_results)]:
        print(f"  {group_label}")
        for label, price, elapsed_ms in group:
            err = _rel_err(price, binomial)
            status = _pass(price, binomial)
            print(f"  {label:<24} {price:>9.4f}  {elapsed_ms:>9.1f} ms  {err:>7.2%}  {status}")

    all_results = lsmc_results + pso_results
    return all_results, float(binomial)


def write_report(summary, report_path):
    from datetime import datetime
    lines = []
    lines.append("# PSO & LSMC American Option Pricing — Test Report")
    lines.append(f"\n**Run date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ")
    lines.append(f"**Tolerance:** {TOLERANCE*100:.0f}% relative error vs Binomial tree\n")

    overall = all(ok for _, _, _, _, ok in summary)
    lines.append(f"## Overall result: {'✅ ALL PASSED' if overall else '❌ SOME FAILED'}\n")

    # ── Per-case sections ──────────────────────────────────────────────────
    for name, (S0, K, r, sigma, T, opttype, nPath, nPeriod, nFish), binomial, results, ok in summary:
        status_icon = "✅" if ok else "❌"
        lines.append(f"---\n")
        lines.append(f"## {status_icon} {name}\n")
        lines.append(f"| Parameter | Value |")
        lines.append(f"|-----------|-------|")
        lines.append(f"| S0 | {S0} |")
        lines.append(f"| K  | {K} |")
        lines.append(f"| r  | {r} |")
        lines.append(f"| σ  | {sigma} |")
        lines.append(f"| T  | {T:.4f} yr |")
        lines.append(f"| Type | {opttype} |")
        lines.append(f"| nPath | {nPath} |")
        lines.append(f"| nPeriod | {nPeriod} |")
        lines.append(f"| nFish | {nFish} |")
        lines.append("")
        lines.append(f"| Method | Price | Time (ms) | Rel Err | Status |")
        lines.append(f"|--------|------:|----------:|--------:|--------|")
        lines.append(f"| **Binomial (ref)** | **{binomial:.4f}** | — | — | — |")

        prev_group = None
        for label, price, elapsed_ms in results:
            group = "LSMC" if "LSMC" in label else "PSO"
            if group != prev_group:
                lines.append(f"| *{group}* | | | | |")
                prev_group = group
            err = _rel_err(price, binomial)
            icon = "✅" if _pass(price, binomial) == "PASS" else "❌"
            lines.append(f"| {label} | {price:.4f} | {elapsed_ms:.1f} | {err:.2%} | {icon} |")
        lines.append("")

    # ── Summary table ──────────────────────────────────────────────────────
    lines.append("---\n")
    lines.append("## Summary\n")
    lines.append("| Test Case | Binomial | Avg LSMC | Avg PSO | Result |")
    lines.append("|-----------|--------:|---------:|--------:|--------|")
    for name, _, binomial, results, ok in summary:
        icon = "✅" if ok else "❌"
        lsmc_p = [p for lbl, p, _ in results if "LSMC" in lbl]
        pso_p  = [p for lbl, p, _ in results if "PSO"  in lbl]
        avg_lsmc = f"{np.mean(lsmc_p):.4f}" if lsmc_p else "—"
        avg_pso  = f"{np.mean(pso_p):.4f}"  if pso_p  else "—"
        lines.append(f"| {name} | {binomial:.4f} | {avg_lsmc} | {avg_pso} | {icon} |")

    lines.append(f"\n*Generated by `test_pso.py`*\n")

    report_path.write_text("\n".join(lines))
    print(f"\n  Report written to: {report_path}")


def main():
    from src.models.utils import checkOpenCL
    checkOpenCL()

    all_pass = True
    summary  = []   # (name, params_tuple, binomial, results, case_pass)

    for case in TEST_CASES:
        name   = case[0]
        params = case[1:]   # (S0, K, r, sigma, T, opttype, nPath, nPeriod, nFish)
        results, binomial = run_case(name, *params)
        case_pass = all(_pass(p, binomial) == "PASS" for _, p, _ in results)
        all_pass  = all_pass and case_pass
        summary.append((name, params, binomial, results, case_pass))

    # ── Console summary ───────────────────────────────────────────────────────
    print(f"\n\n{'='*72}")
    print("  SUMMARY")
    print(f"{'='*72}")
    for name, _, binomial, results, ok in summary:
        status = "PASS" if ok else "FAIL"
        lsmc_prices = [p for lbl, p, _ in results if "LSMC" in lbl]
        pso_prices  = [p for lbl, p, _ in results if "PSO"  in lbl]
        avg_lsmc = np.mean(lsmc_prices) if lsmc_prices else float("nan")
        avg_pso  = np.mean(pso_prices)  if pso_prices  else float("nan")
        print(f"  [{status}]  {name:<40}  binomial={binomial:.4f}"
              f"  lsmc={avg_lsmc:.4f}  pso={avg_pso:.4f}")

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")
    print(f"{'='*72}\n")

    # ── Markdown report ───────────────────────────────────────────────────────
    write_report(summary, project_root / "test_report.md")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())