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
from src.models.longstaff import LSMC_OpenCL
from src.models.pso import (
    PSO_OpenCL_hybrid,
    PSO_OpenCL_scalar,
    PSO_OpenCL_scalar_fusion,
    PSO_OpenCL_vec,
    PSO_OpenCL_vec_fusion,
)

# ── Test cases ─────────────────────────────────────────────────────────────────
# S&P 500 index options, Sep 2008 (secid=108105, T=30 days for all cases)
# Columns: name, S0(close), K, r(_3_MO/100), sigma, T(days/365),
#          opttype, impl_premium, nPath, nPeriod, nFish
#
# Market regimes:
#   02SEP08 – pre-Lehman,  S0=1277.58, r=1.72%  (low vol, mild skew)
#   15SEP08 – Lehman day,  S0=1192.70, r=1.02%  (vol spike)
#   29SEP08 – TARP reject, S0=1106.42, r=0.94%  (max stress, steep skew)
#
# Moneyness guide (abs delta):  ≈10 → deep OTM | ≈25 → OTM | ≈50 → ATM
#                                ≈75 → ITM      | ≈90 → deep ITM
#
# (* marked) impl_premium computed from Black-Scholes with vol consistent
# with the surrounding market data; all others are real market premiums.
#
# Pairs are grouped: each moneyness bucket has one Put and one Call.
TEST_CASES = [
    # ── ATM pair — pre-Lehman (02SEP08) ──────────────────────────────────────
    ("ATM Put   (d=-50, 02SEP08)", 1277.58, 1280.749, 0.0172, 0.213411, 30/365, "P",  32.4512, 20000, 150, 256),
    ("ATM Call  (d=+50, 02SEP08)", 1277.58, 1280.343, 0.0172, 0.209699, 30/365, "C",  29.5502, 20000, 150, 256),

    # ── ATM pair — TARP rejection (29SEP08, high-vol ATM) ────────────────────
    ("ATM Put   (d=-50, 29SEP08)", 1106.42, 1106.000, 0.0094, 0.275000, 30/365, "P",  34.0100, 20000, 150, 256),  # *
    ("ATM Call  (d=+50, 29SEP08)", 1106.42, 1106.000, 0.0094, 0.275000, 30/365, "C",  35.2800, 20000, 150, 256),  # *

    # ── OTM pair — Lehman collapse (15SEP08) ─────────────────────────────────
    ("OTM Put   (d=-25, 15SEP08)", 1192.70, 1126.930, 0.0102, 0.317198, 30/365, "P",  16.9545, 20000, 150, 256),
    ("OTM Call  (d=+25, 15SEP08)", 1192.70, 1265.262, 0.0102, 0.286691, 30/365, "C",  14.0483, 20000, 150, 256),

    # ── ITM pair — Lehman collapse (15SEP08, vol spiking) ────────────────────
    ("ITM Put   (d=-75, 15SEP08)", 1192.70, 1267.000, 0.0102, 0.290000, 30/365, "P",  87.3300, 20000, 150, 256),  # *
    ("ITM Call  (d=+75, 15SEP08)", 1192.70, 1125.000, 0.0102, 0.330000, 30/365, "C",  86.4800, 20000, 150, 256),  # *

    # ── ITM pair — TARP rejection (29SEP08) ──────────────────────────────────
    ("ITM Put   (d=-75, 29SEP08)", 1106.42, 1174.136, 0.0094, 0.282437, 30/365, "P",  78.9833, 20000, 150, 256),
    ("ITM Call  (d=+75, 29SEP08)", 1106.42, 1040.000, 0.0094, 0.350000, 30/365, "C",  84.7200, 20000, 150, 256),  # *

    # ── Very-OTM pair — TARP rejection (29SEP08, steep skew) ─────────────────
    ("vOTM Put  (d=-15, 29SEP08)", 1106.42,  987.000, 0.0094, 0.410000, 30/365, "P",  10.7400, 20000, 150, 256),  # *
    ("vOTM Call (d=+15, 29SEP08)", 1106.42, 1260.221, 0.0094, 0.411432, 30/365, "C",   9.6337, 20000, 150, 256),

    # ── Deep-OTM pair — pre-Lehman (02SEP08) ─────────────────────────────────
    ("dOTM Put  (d=-10, 02SEP08)", 1277.58, 1155.000, 0.0172, 0.270000, 30/365, "P",   4.0100, 20000, 150, 256),  # *
    ("dOTM Call (d=+10, 02SEP08)", 1277.58, 1365.000, 0.0172, 0.175000, 30/365, "C",   2.9400, 20000, 150, 256),  # *

    # ── Deep-ITM pair — TARP rejection (29SEP08) ─────────────────────────────
    ("dITM Put  (d=-90, 29SEP08)", 1106.42, 1217.000, 0.0094, 0.250000, 30/365, "P", 113.4100, 20000, 150, 256),  # *
    ("dITM Call (d=+90, 29SEP08)", 1106.42,  966.000, 0.0094, 0.390000, 30/365, "C", 147.1600, 20000, 150, 256),  # *
]

TOLERANCE = 0.15   # allow up to 15% relative error vs binomial (MC variance at these path counts)

# ── Helpers ───────────────────────────────────────────────────────────────────
def _rel_err(price, ref):
    return abs(price - ref) / ref if ref > 1e-8 else abs(price - ref)

def _pass(price, ref):
    return "PASS" if _rel_err(price, ref) <= TOLERANCE else "FAIL"

def run_case(name, S0, K, r, sigma, T, opttype, impl_premium, nPath, nPeriod, nFish):
    print(f"\n{'='*72}")
    print(f"  {name}")
    print(f"  S0={S0:.4f}  K={K:.4f}  r={r:.4f}  sigma={sigma:.4f}  "
          f"T={T:.4f}y  nPath={nPath}  nPeriod={nPeriod}  nFish={nFish}")
    print(f"  Market price (impl_premium): {impl_premium:.4f}")
    print(f"{'='*72}")

    # ── Reference ─────────────────────────────────────────────────────────────
    binomial, t_bin = bm.binomialAmericanOption(S0, K, r, sigma, nPeriod, T, opttype)

    # ── Monte Carlo setup ─────────────────────────────────────────────────────
    mc = hybridMonteCarlo(S0, r, sigma, T, nPath, nPeriod, K, opttype, nFish)

    lsmc_results = []
    pso_results  = []

    # ── LSMC GPU ──────────────────────────────────────────────────────────────
    lsmc_cl = LSMC_OpenCL(mc, preCalc="optimized")
    p_lsmc_cl, t_lsmc_cl = lsmc_cl.longstaff_schwartz_itm_path_fast_hybrid()
    lsmc_results.append(("LSMC GPU",      float(p_lsmc_cl), t_lsmc_cl))

    # ── PSO GPU ───────────────────────────────────────────────────────────────
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
    print(f"\n  {'Method':<24} {'Price':>9}  {'Time':>10}  {'vs Bin':>7}  {'vs Mkt':>7}  Status")
    print(f"  {'-'*W}")
    print(f"  {'Binomial (ref)':<24} {binomial:>9.4f}  {t_bin:>9.1f} ms")
    print(f"  {'Market (impl_prem)':<24} {impl_premium:>9.4f}")
    print(f"  {'-'*W}")
    for group_label, group in [("── LSMC GPU", lsmc_results), ("── PSO GPU", pso_results)]:
        print(f"  {group_label}")
        for label, price, elapsed_ms in group:
            err_bin = _rel_err(price, binomial)
            err_mkt = _rel_err(price, impl_premium)
            status = _pass(price, binomial)
            print(f"  {label:<24} {price:>9.4f}  {elapsed_ms:>9.1f} ms  {err_bin:>6.2%}  {err_mkt:>6.2%}  {status}")

    all_results = lsmc_results + pso_results
    return all_results, float(binomial), float(impl_premium)


def write_report(summary, report_path):
    from datetime import datetime
    lines = []
    lines.append("# PSO & LSMC American Option Pricing — Test Report")
    lines.append(f"\n**Run date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ")
    lines.append(f"**Tolerance:** {TOLERANCE*100:.0f}% relative error vs Binomial tree\n")

    overall = all(ok for _, _, _, _, _, ok in summary)
    lines.append(f"## Overall result: {'✅ ALL PASSED' if overall else '❌ SOME FAILED'}\n")

    # ── Per-case sections ──────────────────────────────────────────────────
    for name, (S0, K, r, sigma, T, opttype, _, nPath, nPeriod, nFish), binomial, mkt, results, ok in summary:
        status_icon = "✅" if ok else "❌"
        lines.append(f"---\n")
        lines.append(f"## {status_icon} {name}\n")
        lines.append(f"| Parameter | Value |")
        lines.append(f"|-----------|-------|")
        lines.append(f"| S0 (close) | {S0} |")
        lines.append(f"| K (impl_strike) | {K} |")
        lines.append(f"| r (_3_MO/100) | {r} |")
        lines.append(f"| σ (impl_vol) | {sigma} |")
        lines.append(f"| T  | {T:.4f} yr |")
        lines.append(f"| Type | {opttype} |")
        lines.append(f"| Market price (impl_premium) | {mkt:.4f} |")
        lines.append(f"| nPath | {nPath} |")
        lines.append(f"| nPeriod | {nPeriod} |")
        lines.append(f"| nFish | {nFish} |")
        lines.append("")
        lines.append(f"| Method | Price | Time (ms) | vs Binomial | vs Market | Status |")
        lines.append(f"|--------|------:|----------:|------------:|----------:|--------|")
        lines.append(f"| **Binomial (ref)** | **{binomial:.4f}** | — | — | {_rel_err(binomial, mkt):.2%} | — |")
        lines.append(f"| *Market (impl_premium)* | *{mkt:.4f}* | — | {_rel_err(mkt, binomial):.2%} | — | — |")

        prev_group = None
        for label, price, elapsed_ms in results:
            group = "LSMC" if "LSMC" in label else "PSO"
            if group != prev_group:
                lines.append(f"| *{group} GPU* | | | | | |")
                prev_group = group
            err_bin = _rel_err(price, binomial)
            err_mkt = _rel_err(price, mkt)
            icon = "✅" if _pass(price, binomial) == "PASS" else "❌"
            lines.append(f"| {label} | {price:.4f} | {elapsed_ms:.1f} | {err_bin:.2%} | {err_mkt:.2%} | {icon} |")
        lines.append("")

    # ── Summary table ──────────────────────────────────────────────────────
    lines.append("---\n")
    lines.append("## Summary\n")
    lines.append("| Test Case | Binomial | Market | Avg LSMC GPU | Avg PSO GPU | Result |")
    lines.append("|-----------|--------:|-------:|-------------:|------------:|--------|")
    for name, _, binomial, mkt, results, ok in summary:
        icon = "✅" if ok else "❌"
        lsmc_p = [p for lbl, p, _ in results if "LSMC" in lbl]
        pso_p  = [p for lbl, p, _ in results if "PSO"  in lbl]
        avg_lsmc = f"{np.mean(lsmc_p):.4f}" if lsmc_p else "—"
        avg_pso  = f"{np.mean(pso_p):.4f}"  if pso_p  else "—"
        lines.append(f"| {name} | {binomial:.4f} | {mkt:.4f} | {avg_lsmc} | {avg_pso} | {icon} |")

    lines.append(f"\n*Generated by `test_pso.py`*\n")

    report_path.write_text("\n".join(lines))
    print(f"\n  Report written to: {report_path}")


def main():
    from src.models.utils import checkOpenCL
    checkOpenCL()

    all_pass = True
    summary  = []   # (name, params_tuple, binomial, mkt, results, case_pass)

    for case in TEST_CASES:
        name   = case[0]
        params = case[1:]   # (S0, K, r, sigma, T, opttype, impl_premium, nPath, nPeriod, nFish)
        results, binomial, mkt = run_case(name, *params)
        case_pass = all(_pass(p, binomial) == "PASS" for _, p, _ in results)
        all_pass  = all_pass and case_pass
        summary.append((name, params, binomial, mkt, results, case_pass))

    # ── Console summary ───────────────────────────────────────────────────────
    print(f"\n\n{'='*72}")
    print("  SUMMARY")
    print(f"{'='*72}")
    for name, _, binomial, mkt, results, ok in summary:
        status = "PASS" if ok else "FAIL"
        lsmc_prices = [p for lbl, p, _ in results if "LSMC" in lbl]
        pso_prices  = [p for lbl, p, _ in results if "PSO"  in lbl]
        avg_lsmc = np.mean(lsmc_prices) if lsmc_prices else float("nan")
        avg_pso  = np.mean(pso_prices)  if pso_prices  else float("nan")
        print(f"  [{status}]  {name:<40}  binomial={binomial:.4f}  mkt={mkt:.4f}"
              f"  lsmc={avg_lsmc:.4f}  pso={avg_pso:.4f}")

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")
    print(f"{'='*72}\n")

    # ── Markdown report ───────────────────────────────────────────────────────
    write_report(summary, project_root / "test_report.md")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())