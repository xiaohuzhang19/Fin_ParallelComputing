# PSO & LSMC American Option Pricing — Test Report

**Run date:** 2026-03-08 22:35:12  
**Tolerance:** 15% relative error vs Binomial tree

## Overall result: ✅ ALL PASSED

---

## ✅ ATM Put   (d=-50, 02SEP08)

| Parameter | Value |
|-----------|-------|
| S0 (close) | 1277.58 |
| K (impl_strike) | 1280.749 |
| r (_3_MO/100) | 0.0172 |
| σ (impl_vol) | 0.213411 |
| T  | 0.0822 yr |
| Type | P |
| Market price (impl_premium) | 32.4512 |
| nPath | 10000 |
| nPeriod | 200 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **32.0196** | — | — | 1.33% | — |
| *Market (impl_premium)* | *32.4512* | — | 1.35% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 32.2106 | 254.3 | 0.60% | 0.74% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 32.4917 | 1612.8 | 1.47% | 0.12% | ✅ |
| PSO GPU scalar | 32.4917 | 211.7 | 1.47% | 0.12% | ✅ |
| PSO GPU sc_fusion | 32.4917 | 209.2 | 1.47% | 0.12% | ✅ |
| PSO GPU vec(f8) | 32.4917 | 93.4 | 1.47% | 0.12% | ✅ |
| PSO GPU vec_fusion | 32.4917 | 91.0 | 1.47% | 0.12% | ✅ |
| *PSO CPU (timing only, 5 iters)* | | | | | |
| PSO CPU numpy(*) | 32.4795 | 1722.9 | 1.44% | 0.09% | — |

---

## ✅ ATM Call  (d=+50, 02SEP08)

| Parameter | Value |
|-----------|-------|
| S0 (close) | 1277.58 |
| K (impl_strike) | 1280.343 |
| r (_3_MO/100) | 0.0172 |
| σ (impl_vol) | 0.209699 |
| T  | 0.0822 yr |
| Type | C |
| Market price (impl_premium) | 29.5502 |
| nPath | 10000 |
| nPeriod | 200 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **30.1932** | — | — | 2.18% | — |
| *Market (impl_premium)* | *29.5502* | — | 2.13% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 29.7015 | 95.5 | 1.63% | 0.51% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 29.9498 | 1608.5 | 0.81% | 1.35% | ✅ |
| PSO GPU scalar | 29.9498 | 209.9 | 0.81% | 1.35% | ✅ |
| PSO GPU sc_fusion | 29.9498 | 208.4 | 0.81% | 1.35% | ✅ |
| PSO GPU vec(f8) | 29.9498 | 81.9 | 0.81% | 1.35% | ✅ |
| PSO GPU vec_fusion | 29.9498 | 83.5 | 0.81% | 1.35% | ✅ |
| *PSO CPU (timing only, 5 iters)* | | | | | |
| PSO CPU numpy(*) | 29.9497 | 1724.9 | 0.81% | 1.35% | — |

---

## ✅ ATM Put   (d=-50, 29SEP08)

| Parameter | Value |
|-----------|-------|
| S0 (close) | 1106.42 |
| K (impl_strike) | 1106.0 |
| r (_3_MO/100) | 0.0094 |
| σ (impl_vol) | 0.275 |
| T  | 0.0822 yr |
| Type | P |
| Market price (impl_premium) | 34.0100 |
| nPath | 10000 |
| nPeriod | 200 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **34.1494** | — | — | 0.41% | — |
| *Market (impl_premium)* | *34.0100* | — | 0.41% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 34.3703 | 71.0 | 0.65% | 1.06% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 34.7118 | 1611.1 | 1.65% | 2.06% | ✅ |
| PSO GPU scalar | 34.7118 | 212.7 | 1.65% | 2.06% | ✅ |
| PSO GPU sc_fusion | 34.7118 | 210.6 | 1.65% | 2.06% | ✅ |
| PSO GPU vec(f8) | 34.7118 | 82.2 | 1.65% | 2.06% | ✅ |
| PSO GPU vec_fusion | 34.7118 | 81.0 | 1.65% | 2.06% | ✅ |
| *PSO CPU (timing only, 5 iters)* | | | | | |
| PSO CPU numpy(*) | 34.7499 | 2355.4 | 1.76% | 2.18% | — |

---

## ✅ ATM Call  (d=+50, 29SEP08)

| Parameter | Value |
|-----------|-------|
| S0 (close) | 1106.42 |
| K (impl_strike) | 1106.0 |
| r (_3_MO/100) | 0.0094 |
| σ (impl_vol) | 0.275 |
| T  | 0.0822 yr |
| Type | C |
| Market price (impl_premium) | 35.2800 |
| nPath | 10000 |
| nPeriod | 200 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **35.3795** | — | — | 0.28% | — |
| *Market (impl_premium)* | *35.2800* | — | 0.28% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 34.9635 | 68.8 | 1.18% | 0.90% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 35.1512 | 1609.4 | 0.65% | 0.37% | ✅ |
| PSO GPU scalar | 35.1512 | 211.0 | 0.65% | 0.37% | ✅ |
| PSO GPU sc_fusion | 35.1512 | 209.3 | 0.65% | 0.37% | ✅ |
| PSO GPU vec(f8) | 35.1512 | 81.8 | 0.65% | 0.37% | ✅ |
| PSO GPU vec_fusion | 35.1512 | 80.2 | 0.65% | 0.37% | ✅ |
| *PSO CPU (timing only, 5 iters)* | | | | | |
| PSO CPU numpy(*) | 35.1511 | 1816.2 | 0.65% | 0.37% | — |

---

## ✅ OTM Put   (d=-25, 15SEP08)

| Parameter | Value |
|-----------|-------|
| S0 (close) | 1192.7 |
| K (impl_strike) | 1126.93 |
| r (_3_MO/100) | 0.0102 |
| σ (impl_vol) | 0.317198 |
| T  | 0.0822 yr |
| Type | P |
| Market price (impl_premium) | 16.9545 |
| nPath | 10000 |
| nPeriod | 200 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **16.8825** | — | — | 0.42% | — |
| *Market (impl_premium)* | *16.9545* | — | 0.43% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 17.1960 | 79.6 | 1.86% | 1.42% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 17.3036 | 1643.3 | 2.49% | 2.06% | ✅ |
| PSO GPU scalar | 17.3036 | 211.0 | 2.49% | 2.06% | ✅ |
| PSO GPU sc_fusion | 17.3036 | 210.7 | 2.49% | 2.06% | ✅ |
| PSO GPU vec(f8) | 17.3036 | 82.1 | 2.49% | 2.06% | ✅ |
| PSO GPU vec_fusion | 17.3036 | 81.4 | 2.49% | 2.06% | ✅ |
| *PSO CPU (timing only, 5 iters)* | | | | | |
| PSO CPU numpy(*) | 17.2132 | 1857.7 | 1.96% | 1.53% | — |

---

## ✅ OTM Call  (d=+25, 15SEP08)

| Parameter | Value |
|-----------|-------|
| S0 (close) | 1192.7 |
| K (impl_strike) | 1265.262 |
| r (_3_MO/100) | 0.0102 |
| σ (impl_vol) | 0.286691 |
| T  | 0.0822 yr |
| Type | C |
| Market price (impl_premium) | 14.0483 |
| nPath | 10000 |
| nPeriod | 200 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **14.1869** | — | — | 0.99% | — |
| *Market (impl_premium)* | *14.0483* | — | 0.98% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 14.1459 | 46.5 | 0.29% | 0.69% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 14.1690 | 1634.9 | 0.13% | 0.86% | ✅ |
| PSO GPU scalar | 14.1690 | 210.2 | 0.13% | 0.86% | ✅ |
| PSO GPU sc_fusion | 14.1690 | 208.1 | 0.13% | 0.86% | ✅ |
| PSO GPU vec(f8) | 14.1690 | 80.8 | 0.13% | 0.86% | ✅ |
| PSO GPU vec_fusion | 14.1690 | 80.4 | 0.13% | 0.86% | ✅ |
| *PSO CPU (timing only, 5 iters)* | | | | | |
| PSO CPU numpy(*) | 14.1690 | 1941.5 | 0.13% | 0.86% | — |

---

## ✅ ITM Put   (d=-75, 15SEP08)

| Parameter | Value |
|-----------|-------|
| S0 (close) | 1192.7 |
| K (impl_strike) | 1267.0 |
| r (_3_MO/100) | 0.0102 |
| σ (impl_vol) | 0.29 |
| T  | 0.0822 yr |
| Type | P |
| Market price (impl_premium) | 87.3300 |
| nPath | 10000 |
| nPeriod | 200 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **87.5646** | — | — | 0.27% | — |
| *Market (impl_premium)* | *87.3300* | — | 0.27% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 87.3798 | 82.9 | 0.21% | 0.06% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 88.4193 | 1612.9 | 0.98% | 1.25% | ✅ |
| PSO GPU scalar | 88.4193 | 211.0 | 0.98% | 1.25% | ✅ |
| PSO GPU sc_fusion | 88.4193 | 208.0 | 0.98% | 1.25% | ✅ |
| PSO GPU vec(f8) | 88.4193 | 82.6 | 0.98% | 1.25% | ✅ |
| PSO GPU vec_fusion | 88.4193 | 80.9 | 0.98% | 1.25% | ✅ |
| *PSO CPU (timing only, 5 iters)* | | | | | |
| PSO CPU numpy(*) | 88.4766 | 2484.4 | 1.04% | 1.31% | — |

---

## ✅ ITM Call  (d=+75, 15SEP08)

| Parameter | Value |
|-----------|-------|
| S0 (close) | 1192.7 |
| K (impl_strike) | 1125.0 |
| r (_3_MO/100) | 0.0102 |
| σ (impl_vol) | 0.33 |
| T  | 0.0822 yr |
| Type | C |
| Market price (impl_premium) | 86.4800 |
| nPath | 10000 |
| nPeriod | 200 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **86.3571** | — | — | 0.14% | — |
| *Market (impl_premium)* | *86.4800* | — | 0.14% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 85.1825 | 75.4 | 1.36% | 1.50% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 85.8176 | 3748.9 | 0.62% | 0.77% | ✅ |
| PSO GPU scalar | 85.8176 | 494.1 | 0.62% | 0.77% | ✅ |
| PSO GPU sc_fusion | 85.8176 | 489.1 | 0.62% | 0.77% | ✅ |
| PSO GPU vec(f8) | 85.8176 | 192.2 | 0.62% | 0.77% | ✅ |
| PSO GPU vec_fusion | 85.8176 | 189.8 | 0.62% | 0.77% | ✅ |
| *PSO CPU (timing only, 5 iters)* | | | | | |
| PSO CPU numpy(*) | 85.8178 | 3240.2 | 0.62% | 0.77% | — |

---

## ✅ ITM Put   (d=-75, 29SEP08)

| Parameter | Value |
|-----------|-------|
| S0 (close) | 1106.42 |
| K (impl_strike) | 1174.136 |
| r (_3_MO/100) | 0.0094 |
| σ (impl_vol) | 0.282437 |
| T  | 0.0822 yr |
| Type | P |
| Market price (impl_premium) | 78.9833 |
| nPath | 10000 |
| nPeriod | 200 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **79.5887** | — | — | 0.77% | — |
| *Market (impl_premium)* | *78.9833* | — | 0.76% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 79.3593 | 81.0 | 0.29% | 0.48% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 80.3861 | 1601.8 | 1.00% | 1.78% | ✅ |
| PSO GPU scalar | 80.3861 | 211.5 | 1.00% | 1.78% | ✅ |
| PSO GPU sc_fusion | 80.3861 | 210.4 | 1.00% | 1.78% | ✅ |
| PSO GPU vec(f8) | 80.3861 | 83.9 | 1.00% | 1.78% | ✅ |
| PSO GPU vec_fusion | 80.3861 | 81.5 | 1.00% | 1.78% | ✅ |
| *PSO CPU (timing only, 5 iters)* | | | | | |
| PSO CPU numpy(*) | 80.3906 | 1935.8 | 1.01% | 1.78% | — |

---

## ✅ ITM Call  (d=+75, 29SEP08)

| Parameter | Value |
|-----------|-------|
| S0 (close) | 1106.42 |
| K (impl_strike) | 1040.0 |
| r (_3_MO/100) | 0.0094 |
| σ (impl_vol) | 0.35 |
| T  | 0.0822 yr |
| Type | C |
| Market price (impl_premium) | 84.7200 |
| nPath | 10000 |
| nPeriod | 200 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **84.6735** | — | — | 0.05% | — |
| *Market (impl_premium)* | *84.7200* | — | 0.05% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 83.5500 | 83.3 | 1.33% | 1.38% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 84.0862 | 1620.1 | 0.69% | 0.75% | ✅ |
| PSO GPU scalar | 84.0862 | 212.4 | 0.69% | 0.75% | ✅ |
| PSO GPU sc_fusion | 84.0862 | 209.2 | 0.69% | 0.75% | ✅ |
| PSO GPU vec(f8) | 84.0862 | 81.9 | 0.69% | 0.75% | ✅ |
| PSO GPU vec_fusion | 84.0862 | 81.0 | 0.69% | 0.75% | ✅ |
| *PSO CPU (timing only, 5 iters)* | | | | | |
| PSO CPU numpy(*) | 84.1437 | 3112.6 | 0.63% | 0.68% | — |

---

## ✅ vOTM Put  (d=-15, 29SEP08)

| Parameter | Value |
|-----------|-------|
| S0 (close) | 1106.42 |
| K (impl_strike) | 987.0 |
| r (_3_MO/100) | 0.0094 |
| σ (impl_vol) | 0.41 |
| T  | 0.0822 yr |
| Type | P |
| Market price (impl_premium) | 10.7400 |
| nPath | 10000 |
| nPeriod | 200 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **10.6414** | — | — | 0.92% | — |
| *Market (impl_premium)* | *10.7400* | — | 0.93% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 11.1253 | 43.5 | 4.55% | 3.59% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 11.1260 | 2678.6 | 4.55% | 3.59% | ✅ |
| PSO GPU scalar | 11.1260 | 353.2 | 4.55% | 3.59% | ✅ |
| PSO GPU sc_fusion | 11.1260 | 349.2 | 4.55% | 3.59% | ✅ |
| PSO GPU vec(f8) | 11.1260 | 136.3 | 4.55% | 3.59% | ✅ |
| PSO GPU vec_fusion | 11.1260 | 135.1 | 4.55% | 3.59% | ✅ |
| *PSO CPU (timing only, 5 iters)* | | | | | |
| PSO CPU numpy(*) | 10.7193 | 3094.7 | 0.73% | 0.19% | — |

---

## ✅ vOTM Call (d=+15, 29SEP08)

| Parameter | Value |
|-----------|-------|
| S0 (close) | 1106.42 |
| K (impl_strike) | 1260.221 |
| r (_3_MO/100) | 0.0094 |
| σ (impl_vol) | 0.411432 |
| T  | 0.0822 yr |
| Type | C |
| Market price (impl_premium) | 9.6337 |
| nPath | 10000 |
| nPeriod | 200 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **9.5974** | — | — | 0.38% | — |
| *Market (impl_premium)* | *9.6337* | — | 0.38% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 9.4927 | 45.4 | 1.09% | 1.46% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 9.4911 | 1624.0 | 1.11% | 1.48% | ✅ |
| PSO GPU scalar | 9.4911 | 211.6 | 1.11% | 1.48% | ✅ |
| PSO GPU sc_fusion | 9.4911 | 209.9 | 1.11% | 1.48% | ✅ |
| PSO GPU vec(f8) | 9.4911 | 81.5 | 1.11% | 1.48% | ✅ |
| PSO GPU vec_fusion | 9.4911 | 80.2 | 1.11% | 1.48% | ✅ |
| *PSO CPU (timing only, 5 iters)* | | | | | |
| PSO CPU numpy(*) | 9.4911 | 2510.8 | 1.11% | 1.48% | — |

---

## ✅ dOTM Put  (d=-10, 02SEP08)

| Parameter | Value |
|-----------|-------|
| S0 (close) | 1277.58 |
| K (impl_strike) | 1155.0 |
| r (_3_MO/100) | 0.0172 |
| σ (impl_vol) | 0.27 |
| T  | 0.0822 yr |
| Type | P |
| Market price (impl_premium) | 4.0100 |
| nPath | 10000 |
| nPeriod | 200 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **4.0871** | — | — | 1.92% | — |
| *Market (impl_premium)* | *4.0100* | — | 1.89% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 4.2906 | 41.2 | 4.98% | 7.00% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 4.1853 | 2144.0 | 2.40% | 4.37% | ✅ |
| PSO GPU scalar | 4.1853 | 282.5 | 2.40% | 4.37% | ✅ |
| PSO GPU sc_fusion | 4.1853 | 280.0 | 2.40% | 4.37% | ✅ |
| PSO GPU vec(f8) | 4.1853 | 109.2 | 2.40% | 4.37% | ✅ |
| PSO GPU vec_fusion | 4.1853 | 107.6 | 2.40% | 4.37% | ✅ |
| *PSO CPU (timing only, 5 iters)* | | | | | |
| PSO CPU numpy(*) | 4.2485 | 3107.5 | 3.95% | 5.95% | — |

---

## ✅ dOTM Call (d=+10, 02SEP08)

| Parameter | Value |
|-----------|-------|
| S0 (close) | 1277.58 |
| K (impl_strike) | 1365.0 |
| r (_3_MO/100) | 0.0172 |
| σ (impl_vol) | 0.175 |
| T  | 0.0822 yr |
| Type | C |
| Market price (impl_premium) | 2.9400 |
| nPath | 10000 |
| nPeriod | 200 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **3.0732** | — | — | 4.53% | — |
| *Market (impl_premium)* | *2.9400* | — | 4.33% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 3.0271 | 44.3 | 1.50% | 2.96% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 3.0438 | 1613.8 | 0.96% | 3.53% | ✅ |
| PSO GPU scalar | 3.0438 | 210.4 | 0.96% | 3.53% | ✅ |
| PSO GPU sc_fusion | 3.0438 | 208.3 | 0.96% | 3.53% | ✅ |
| PSO GPU vec(f8) | 3.0438 | 80.8 | 0.96% | 3.53% | ✅ |
| PSO GPU vec_fusion | 3.0438 | 80.2 | 0.96% | 3.53% | ✅ |
| *PSO CPU (timing only, 5 iters)* | | | | | |
| PSO CPU numpy(*) | 3.0438 | 1848.7 | 0.96% | 3.53% | — |

---

## ✅ dITM Put  (d=-90, 29SEP08)

| Parameter | Value |
|-----------|-------|
| S0 (close) | 1106.42 |
| K (impl_strike) | 1217.0 |
| r (_3_MO/100) | 0.0094 |
| σ (impl_vol) | 0.25 |
| T  | 0.0822 yr |
| Type | P |
| Market price (impl_premium) | 113.4100 |
| nPath | 10000 |
| nPeriod | 150 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **113.5423** | — | — | 0.12% | — |
| *Market (impl_premium)* | *113.4100* | — | 0.12% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 110.5426 | 67.7 | 2.64% | 2.53% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 114.3797 | 1244.2 | 0.74% | 0.86% | ✅ |
| PSO GPU scalar | 114.3797 | 170.5 | 0.74% | 0.86% | ✅ |
| PSO GPU sc_fusion | 114.3797 | 169.7 | 0.74% | 0.86% | ✅ |
| PSO GPU vec(f8) | 114.3797 | 2292.1 | 0.74% | 0.86% | ✅ |
| PSO GPU vec_fusion | 114.3797 | 2268.2 | 0.74% | 0.86% | ✅ |
| *PSO CPU (timing only, 5 iters)* | | | | | |
| PSO CPU numpy(*) | 114.4601 | 1364.5 | 0.81% | 0.93% | — |

---

## ✅ dITM Call (d=+90, 29SEP08)

| Parameter | Value |
|-----------|-------|
| S0 (close) | 1106.42 |
| K (impl_strike) | 966.0 |
| r (_3_MO/100) | 0.0094 |
| σ (impl_vol) | 0.39 |
| T  | 0.0822 yr |
| Type | C |
| Market price (impl_premium) | 147.1600 |
| nPath | 10000 |
| nPeriod | 150 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **147.3874** | — | — | 0.15% | — |
| *Market (impl_premium)* | *147.1600* | — | 0.15% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 146.4455 | 65.3 | 0.64% | 0.49% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 146.4754 | 2838.4 | 0.62% | 0.47% | ✅ |
| PSO GPU scalar | 146.4754 | 382.7 | 0.62% | 0.47% | ✅ |
| PSO GPU sc_fusion | 146.4754 | 378.7 | 0.62% | 0.47% | ✅ |
| PSO GPU vec(f8) | 146.4754 | 5295.0 | 0.62% | 0.47% | ✅ |
| PSO GPU vec_fusion | 146.4754 | 5253.9 | 0.62% | 0.47% | ✅ |
| *PSO CPU (timing only, 5 iters)* | | | | | |
| PSO CPU numpy(*) | 146.4002 | 2220.4 | 0.67% | 0.52% | — |

---

## ✅ OTM Put   (S0=100,K=110,T=1y)

| Parameter | Value |
|-----------|-------|
| S0 (close) | 100.0 |
| K (impl_strike) | 110.0 |
| r (_3_MO/100) | 0.03 |
| σ (impl_vol) | 0.3 |
| T  | 1.0000 yr |
| Type | P |
| Market price (impl_premium) | 16.5100 |
| nPath | 20000 |
| nPeriod | 200 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **16.5112** | — | — | 0.01% | — |
| *Market (impl_premium)* | *16.5100* | — | 0.01% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 16.4756 | 148.4 | 0.22% | 0.21% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 16.5441 | 5890.3 | 0.20% | 0.21% | ✅ |
| PSO GPU scalar | 16.5441 | 693.9 | 0.20% | 0.21% | ✅ |
| PSO GPU sc_fusion | 16.5441 | 691.9 | 0.20% | 0.21% | ✅ |
| PSO GPU vec(f8) | 16.5441 | 267.7 | 0.20% | 0.21% | ✅ |
| PSO GPU vec_fusion | 16.5441 | 266.3 | 0.20% | 0.21% | ✅ |
| *PSO CPU (timing only, 5 iters)* | | | | | |
| PSO CPU numpy(*) | 16.5561 | 6424.6 | 0.27% | 0.28% | — |

---

## ✅ ATM Put   (S0=22.7,K=22.7,T=60d)

| Parameter | Value |
|-----------|-------|
| S0 (close) | 22.7389 |
| K (impl_strike) | 22.7389 |
| r (_3_MO/100) | 0.0102 |
| σ (impl_vol) | 0.502026 |
| T  | 0.1644 yr |
| Type | P |
| Market price (impl_premium) | 1.8200 |
| nPath | 10000 |
| nPeriod | 250 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **1.8230** | — | — | 0.17% | — |
| *Market (impl_premium)* | *1.8200* | — | 0.17% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 1.7995 | 90.9 | 1.29% | 1.12% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 1.8287 | 8639.7 | 0.31% | 0.48% | ✅ |
| PSO GPU scalar | 1.8287 | 968.0 | 0.31% | 0.48% | ✅ |
| PSO GPU sc_fusion | 1.8287 | 959.6 | 0.31% | 0.48% | ✅ |
| PSO GPU vec(f8) | 1.8287 | 14900.7 | 0.31% | 0.48% | ✅ |
| PSO GPU vec_fusion | 1.8287 | 14664.5 | 0.31% | 0.48% | ✅ |
| *PSO CPU (timing only, 5 iters)* | | | | | |
| PSO CPU numpy(*) | 1.8056 | 4391.8 | 0.95% | 0.79% | — |

---

## ✅ ITM Put   (S0=100,K=105,T=1y)

| Parameter | Value |
|-----------|-------|
| S0 (close) | 100.0 |
| K (impl_strike) | 105.0 |
| r (_3_MO/100) | 0.03 |
| σ (impl_vol) | 0.2 |
| T  | 1.0000 yr |
| Type | P |
| Market price (impl_premium) | 9.4800 |
| nPath | 20000 |
| nPeriod | 200 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **9.4825** | — | — | 0.03% | — |
| *Market (impl_premium)* | *9.4800* | — | 0.03% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 9.4512 | 167.8 | 0.33% | 0.30% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 9.4538 | 3511.9 | 0.30% | 0.28% | ✅ |
| PSO GPU scalar | 9.4538 | 419.3 | 0.30% | 0.28% | ✅ |
| PSO GPU sc_fusion | 9.4538 | 415.9 | 0.30% | 0.28% | ✅ |
| PSO GPU vec(f8) | 9.4538 | 157.0 | 0.30% | 0.28% | ✅ |
| PSO GPU vec_fusion | 9.4538 | 155.2 | 0.30% | 0.28% | ✅ |
| *PSO CPU (timing only, 5 iters)* | | | | | |
| PSO CPU numpy(*) | 9.4512 | 5203.3 | 0.33% | 0.30% | — |

---

## ✅ OTM Call  (S0=100,K=105,T=1y)

| Parameter | Value |
|-----------|-------|
| S0 (close) | 100.0 |
| K (impl_strike) | 105.0 |
| r (_3_MO/100) | 0.05 |
| σ (impl_vol) | 0.25 |
| T  | 1.0000 yr |
| Type | C |
| Market price (impl_premium) | 10.0100 |
| nPath | 20000 |
| nPeriod | 200 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **10.0121** | — | — | 0.02% | — |
| *Market (impl_premium)* | *10.0100* | — | 0.02% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 10.0155 | 116.3 | 0.03% | 0.05% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 10.0064 | 13857.4 | 0.06% | 0.04% | ✅ |
| PSO GPU scalar | 10.0064 | 1671.9 | 0.06% | 0.04% | ✅ |
| PSO GPU sc_fusion | 10.0064 | 1656.5 | 0.06% | 0.04% | ✅ |
| PSO GPU vec(f8) | 10.0064 | 639.6 | 0.06% | 0.04% | ✅ |
| PSO GPU vec_fusion | 10.0064 | 636.2 | 0.06% | 0.04% | ✅ |
| *PSO CPU (timing only, 5 iters)* | | | | | |
| PSO CPU numpy(*) | 9.8987 | 6408.5 | 1.13% | 1.11% | — |

---

## Summary

| Test Case | Binomial | Market | Avg LSMC GPU | Avg PSO GPU | Result |
|-----------|--------:|-------:|-------------:|------------:|--------|
| ATM Put   (d=-50, 02SEP08) | 32.0196 | 32.4512 | 32.2106 | 32.4917 | ✅ |
| ATM Call  (d=+50, 02SEP08) | 30.1932 | 29.5502 | 29.7015 | 29.9498 | ✅ |
| ATM Put   (d=-50, 29SEP08) | 34.1494 | 34.0100 | 34.3703 | 34.7118 | ✅ |
| ATM Call  (d=+50, 29SEP08) | 35.3795 | 35.2800 | 34.9635 | 35.1512 | ✅ |
| OTM Put   (d=-25, 15SEP08) | 16.8825 | 16.9545 | 17.1960 | 17.3036 | ✅ |
| OTM Call  (d=+25, 15SEP08) | 14.1869 | 14.0483 | 14.1459 | 14.1690 | ✅ |
| ITM Put   (d=-75, 15SEP08) | 87.5646 | 87.3300 | 87.3798 | 88.4193 | ✅ |
| ITM Call  (d=+75, 15SEP08) | 86.3571 | 86.4800 | 85.1825 | 85.8176 | ✅ |
| ITM Put   (d=-75, 29SEP08) | 79.5887 | 78.9833 | 79.3593 | 80.3861 | ✅ |
| ITM Call  (d=+75, 29SEP08) | 84.6735 | 84.7200 | 83.5500 | 84.0862 | ✅ |
| vOTM Put  (d=-15, 29SEP08) | 10.6414 | 10.7400 | 11.1253 | 11.1260 | ✅ |
| vOTM Call (d=+15, 29SEP08) | 9.5974 | 9.6337 | 9.4927 | 9.4911 | ✅ |
| dOTM Put  (d=-10, 02SEP08) | 4.0871 | 4.0100 | 4.2906 | 4.1853 | ✅ |
| dOTM Call (d=+10, 02SEP08) | 3.0732 | 2.9400 | 3.0271 | 3.0438 | ✅ |
| dITM Put  (d=-90, 29SEP08) | 113.5423 | 113.4100 | 110.5426 | 114.3797 | ✅ |
| dITM Call (d=+90, 29SEP08) | 147.3874 | 147.1600 | 146.4455 | 146.4754 | ✅ |
| OTM Put   (S0=100,K=110,T=1y) | 16.5112 | 16.5100 | 16.4756 | 16.5441 | ✅ |
| ATM Put   (S0=22.7,K=22.7,T=60d) | 1.8230 | 1.8200 | 1.7995 | 1.8287 | ✅ |
| ITM Put   (S0=100,K=105,T=1y) | 9.4825 | 9.4800 | 9.4512 | 9.4538 | ✅ |
| OTM Call  (S0=100,K=105,T=1y) | 10.0121 | 10.0100 | 10.0155 | 10.0064 | ✅ |

*Generated by `test_pso.py`*
