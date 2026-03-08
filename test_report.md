# PSO & LSMC American Option Pricing — Test Report

**Run date:** 2026-03-07 21:25:25  
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
| nPath | 20000 |
| nPeriod | 150 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **32.0222** | — | — | 1.32% | — |
| *Market (impl_premium)* | *32.4512* | — | 1.34% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 31.7231 | 119.1 | 0.93% | 2.24% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 32.0942 | 3259.1 | 0.22% | 1.10% | ✅ |
| PSO GPU scalar | 32.0942 | 429.8 | 0.22% | 1.10% | ✅ |
| PSO GPU sc_fusion | 32.0942 | 430.7 | 0.22% | 1.10% | ✅ |
| PSO GPU vec(f8) | 32.0942 | 6084.2 | 0.22% | 1.10% | ✅ |
| PSO GPU vec_fusion | 32.0942 | 6110.5 | 0.22% | 1.10% | ✅ |

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
| nPath | 20000 |
| nPeriod | 150 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **30.1924** | — | — | 2.17% | — |
| *Market (impl_premium)* | *29.5502* | — | 2.13% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 29.8739 | 104.8 | 1.05% | 1.10% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 30.1004 | 2379.6 | 0.30% | 1.86% | ✅ |
| PSO GPU scalar | 30.1004 | 320.7 | 0.30% | 1.86% | ✅ |
| PSO GPU sc_fusion | 30.1004 | 319.5 | 0.30% | 1.86% | ✅ |
| PSO GPU vec(f8) | 30.1004 | 4551.5 | 0.30% | 1.86% | ✅ |
| PSO GPU vec_fusion | 30.1004 | 4528.4 | 0.30% | 1.86% | ✅ |

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
| nPath | 20000 |
| nPeriod | 150 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **34.1375** | — | — | 0.37% | — |
| *Market (impl_premium)* | *34.0100* | — | 0.37% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 33.9358 | 108.4 | 0.59% | 0.22% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 34.3223 | 2368.8 | 0.54% | 0.92% | ✅ |
| PSO GPU scalar | 34.3223 | 322.7 | 0.54% | 0.92% | ✅ |
| PSO GPU sc_fusion | 34.3223 | 323.3 | 0.54% | 0.92% | ✅ |
| PSO GPU vec(f8) | 34.3223 | 4580.7 | 0.54% | 0.92% | ✅ |
| PSO GPU vec_fusion | 34.3223 | 4575.6 | 0.54% | 0.92% | ✅ |

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
| nPath | 20000 |
| nPeriod | 150 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **35.3669** | — | — | 0.25% | — |
| *Market (impl_premium)* | *35.2800* | — | 0.25% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 35.2054 | 98.2 | 0.46% | 0.21% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 35.3297 | 2428.8 | 0.11% | 0.14% | ✅ |
| PSO GPU scalar | 35.3297 | 323.4 | 0.11% | 0.14% | ✅ |
| PSO GPU sc_fusion | 35.3297 | 324.3 | 0.11% | 0.14% | ✅ |
| PSO GPU vec(f8) | 35.3297 | 4586.3 | 0.11% | 0.14% | ✅ |
| PSO GPU vec_fusion | 35.3297 | 4590.8 | 0.11% | 0.14% | ✅ |

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
| nPath | 20000 |
| nPeriod | 150 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **16.8543** | — | — | 0.59% | — |
| *Market (impl_premium)* | *16.9545* | — | 0.59% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 17.0465 | 69.1 | 1.14% | 0.54% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 17.2211 | 3188.3 | 2.18% | 1.57% | ✅ |
| PSO GPU scalar | 17.2211 | 431.0 | 2.18% | 1.57% | ✅ |
| PSO GPU sc_fusion | 17.2211 | 425.5 | 2.18% | 1.57% | ✅ |
| PSO GPU vec(f8) | 17.2211 | 6100.1 | 2.18% | 1.57% | ✅ |
| PSO GPU vec_fusion | 17.2211 | 6111.5 | 2.18% | 1.57% | ✅ |

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
| nPath | 20000 |
| nPeriod | 150 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **14.2484** | — | — | 1.42% | — |
| *Market (impl_premium)* | *14.0483* | — | 1.40% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 14.0880 | 65.1 | 1.13% | 0.28% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 14.0640 | 2395.1 | 1.29% | 0.11% | ✅ |
| PSO GPU scalar | 14.0640 | 323.6 | 1.29% | 0.11% | ✅ |
| PSO GPU sc_fusion | 14.0640 | 323.7 | 1.29% | 0.11% | ✅ |
| PSO GPU vec(f8) | 14.0640 | 4588.8 | 1.29% | 0.11% | ✅ |
| PSO GPU vec_fusion | 14.0640 | 4584.6 | 1.29% | 0.11% | ✅ |

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
| nPath | 20000 |
| nPeriod | 150 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **87.6148** | — | — | 0.33% | — |
| *Market (impl_premium)* | *87.3300* | — | 0.33% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 87.5726 | 107.8 | 0.05% | 0.28% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 87.7903 | 2374.2 | 0.20% | 0.53% | ✅ |
| PSO GPU scalar | 87.7903 | 323.6 | 0.20% | 0.53% | ✅ |
| PSO GPU sc_fusion | 87.7903 | 321.7 | 0.20% | 0.53% | ✅ |
| PSO GPU vec(f8) | 87.7903 | 4565.4 | 0.20% | 0.53% | ✅ |
| PSO GPU vec_fusion | 87.7903 | 4573.1 | 0.20% | 0.53% | ✅ |

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
| nPath | 20000 |
| nPeriod | 150 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **86.3405** | — | — | 0.16% | — |
| *Market (impl_premium)* | *86.4800* | — | 0.16% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 85.5960 | 120.2 | 0.86% | 1.02% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 86.4436 | 2379.3 | 0.12% | 0.04% | ✅ |
| PSO GPU scalar | 86.4436 | 321.6 | 0.12% | 0.04% | ✅ |
| PSO GPU sc_fusion | 86.4436 | 322.8 | 0.12% | 0.04% | ✅ |
| PSO GPU vec(f8) | 86.4436 | 4575.6 | 0.12% | 0.04% | ✅ |
| PSO GPU vec_fusion | 86.4436 | 4571.1 | 0.12% | 0.04% | ✅ |

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
| nPath | 20000 |
| nPeriod | 150 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **79.6262** | — | — | 0.81% | — |
| *Market (impl_premium)* | *78.9833* | — | 0.81% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 79.5080 | 110.6 | 0.15% | 0.66% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 79.8569 | 2389.9 | 0.29% | 1.11% | ✅ |
| PSO GPU scalar | 79.8569 | 322.7 | 0.29% | 1.11% | ✅ |
| PSO GPU sc_fusion | 79.8569 | 320.3 | 0.29% | 1.11% | ✅ |
| PSO GPU vec(f8) | 79.8569 | 4565.3 | 0.29% | 1.11% | ✅ |
| PSO GPU vec_fusion | 79.8569 | 4535.3 | 0.29% | 1.11% | ✅ |

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
| nPath | 20000 |
| nPeriod | 150 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **84.6588** | — | — | 0.07% | — |
| *Market (impl_premium)* | *84.7200* | — | 0.07% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 83.9152 | 120.4 | 0.88% | 0.95% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 84.7527 | 2395.1 | 0.11% | 0.04% | ✅ |
| PSO GPU scalar | 84.7527 | 322.0 | 0.11% | 0.04% | ✅ |
| PSO GPU sc_fusion | 84.7527 | 322.1 | 0.11% | 0.04% | ✅ |
| PSO GPU vec(f8) | 84.7527 | 4549.6 | 0.11% | 0.04% | ✅ |
| PSO GPU vec_fusion | 84.7527 | 4539.9 | 0.11% | 0.04% | ✅ |

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
| nPath | 20000 |
| nPeriod | 150 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **10.6101** | — | — | 1.21% | — |
| *Market (impl_premium)* | *10.7400* | — | 1.22% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 10.9859 | 71.5 | 3.54% | 2.29% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 10.8516 | 2509.3 | 2.28% | 1.04% | ✅ |
| PSO GPU scalar | 10.8516 | 322.8 | 2.28% | 1.04% | ✅ |
| PSO GPU sc_fusion | 10.8516 | 320.1 | 2.28% | 1.04% | ✅ |
| PSO GPU vec(f8) | 10.8516 | 4522.2 | 2.28% | 1.04% | ✅ |
| PSO GPU vec_fusion | 10.8516 | 4562.8 | 2.28% | 1.04% | ✅ |

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
| nPath | 20000 |
| nPeriod | 150 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **9.6066** | — | — | 0.28% | — |
| *Market (impl_premium)* | *9.6337* | — | 0.28% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 9.6105 | 69.5 | 0.04% | 0.24% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 9.4765 | 2393.7 | 1.35% | 1.63% | ✅ |
| PSO GPU scalar | 9.4765 | 323.0 | 1.35% | 1.63% | ✅ |
| PSO GPU sc_fusion | 9.4765 | 321.0 | 1.35% | 1.63% | ✅ |
| PSO GPU vec(f8) | 9.4765 | 4582.8 | 1.35% | 1.63% | ✅ |
| PSO GPU vec_fusion | 9.4765 | 4578.9 | 1.35% | 1.63% | ✅ |

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
| nPath | 20000 |
| nPeriod | 150 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **4.0572** | — | — | 1.18% | — |
| *Market (impl_premium)* | *4.0100* | — | 1.16% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 4.2701 | 54.8 | 5.25% | 6.49% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 4.2660 | 2401.7 | 5.15% | 6.38% | ✅ |
| PSO GPU scalar | 4.2660 | 321.4 | 5.15% | 6.38% | ✅ |
| PSO GPU sc_fusion | 4.2660 | 322.8 | 5.15% | 6.38% | ✅ |
| PSO GPU vec(f8) | 4.2660 | 4587.6 | 5.15% | 6.38% | ✅ |
| PSO GPU vec_fusion | 4.2660 | 4585.7 | 5.15% | 6.38% | ✅ |

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
| nPath | 20000 |
| nPeriod | 150 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **3.0511** | — | — | 3.78% | — |
| *Market (impl_premium)* | *2.9400* | — | 3.64% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 3.0489 | 55.3 | 0.07% | 3.71% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 3.0188 | 2375.0 | 1.06% | 2.68% | ✅ |
| PSO GPU scalar | 3.0188 | 324.4 | 1.06% | 2.68% | ✅ |
| PSO GPU sc_fusion | 3.0188 | 322.4 | 1.06% | 2.68% | ✅ |
| PSO GPU vec(f8) | 3.0188 | 4567.1 | 1.06% | 2.68% | ✅ |
| PSO GPU vec_fusion | 3.0188 | 4577.6 | 1.06% | 2.68% | ✅ |

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
| nPath | 20000 |
| nPeriod | 150 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **113.5423** | — | — | 0.12% | — |
| *Market (impl_premium)* | *113.4100* | — | 0.12% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 113.4593 | 115.8 | 0.07% | 0.04% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 114.1195 | 2369.7 | 0.51% | 0.63% | ✅ |
| PSO GPU scalar | 114.1195 | 321.0 | 0.51% | 0.63% | ✅ |
| PSO GPU sc_fusion | 114.1195 | 322.0 | 0.51% | 0.63% | ✅ |
| PSO GPU vec(f8) | 114.1195 | 4579.5 | 0.51% | 0.63% | ✅ |
| PSO GPU vec_fusion | 114.1195 | 4585.1 | 0.51% | 0.63% | ✅ |

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
| nPath | 20000 |
| nPeriod | 150 |
| nFish | 256 |

| Method | Price | Time (ms) | vs Binomial | vs Market | Status |
|--------|------:|----------:|------------:|----------:|--------|
| **Binomial (ref)** | **147.3874** | — | — | 0.15% | — |
| *Market (impl_premium)* | *147.1600* | — | 0.15% | — | — |
| *LSMC GPU* | | | | | |
| LSMC GPU | 140.4756 | 109.0 | 4.69% | 4.54% | ✅ |
| *PSO GPU* | | | | | |
| PSO GPU hybrid | 147.4183 | 7113.9 | 0.02% | 0.18% | ✅ |
| PSO GPU scalar | 147.4183 | 961.1 | 0.02% | 0.18% | ✅ |
| PSO GPU sc_fusion | 147.4183 | 961.4 | 0.02% | 0.18% | ✅ |
| PSO GPU vec(f8) | 147.4183 | 13722.5 | 0.02% | 0.18% | ✅ |
| PSO GPU vec_fusion | 147.4183 | 13747.8 | 0.02% | 0.18% | ✅ |

---

## Summary

| Test Case | Binomial | Market | Avg LSMC GPU | Avg PSO GPU | Result |
|-----------|--------:|-------:|-------------:|------------:|--------|
| ATM Put   (d=-50, 02SEP08) | 32.0222 | 32.4512 | 31.7231 | 32.0942 | ✅ |
| ATM Call  (d=+50, 02SEP08) | 30.1924 | 29.5502 | 29.8739 | 30.1004 | ✅ |
| ATM Put   (d=-50, 29SEP08) | 34.1375 | 34.0100 | 33.9358 | 34.3223 | ✅ |
| ATM Call  (d=+50, 29SEP08) | 35.3669 | 35.2800 | 35.2054 | 35.3297 | ✅ |
| OTM Put   (d=-25, 15SEP08) | 16.8543 | 16.9545 | 17.0465 | 17.2211 | ✅ |
| OTM Call  (d=+25, 15SEP08) | 14.2484 | 14.0483 | 14.0880 | 14.0640 | ✅ |
| ITM Put   (d=-75, 15SEP08) | 87.6148 | 87.3300 | 87.5726 | 87.7903 | ✅ |
| ITM Call  (d=+75, 15SEP08) | 86.3405 | 86.4800 | 85.5960 | 86.4436 | ✅ |
| ITM Put   (d=-75, 29SEP08) | 79.6262 | 78.9833 | 79.5080 | 79.8569 | ✅ |
| ITM Call  (d=+75, 29SEP08) | 84.6588 | 84.7200 | 83.9152 | 84.7527 | ✅ |
| vOTM Put  (d=-15, 29SEP08) | 10.6101 | 10.7400 | 10.9859 | 10.8516 | ✅ |
| vOTM Call (d=+15, 29SEP08) | 9.6066 | 9.6337 | 9.6105 | 9.4765 | ✅ |
| dOTM Put  (d=-10, 02SEP08) | 4.0572 | 4.0100 | 4.2701 | 4.2660 | ✅ |
| dOTM Call (d=+10, 02SEP08) | 3.0511 | 2.9400 | 3.0489 | 3.0188 | ✅ |
| dITM Put  (d=-90, 29SEP08) | 113.5423 | 113.4100 | 113.4593 | 114.1195 | ✅ |
| dITM Call (d=+90, 29SEP08) | 147.3874 | 147.1600 | 140.4756 | 147.4183 | ✅ |

*Generated by `test_pso.py`*
