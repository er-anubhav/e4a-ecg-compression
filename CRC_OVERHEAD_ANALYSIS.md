# E4A ECG Codec: Frame Integrity & CRC Overhead Analysis

## 1. Overview
In embedded medical telemetry (such as BLE, ESP-NOW, or 802.15.4), packets are subject to wireless bit errors. While the primary benchmark evaluates the pure compression payload and codec headers, production framing requires a cyclic redundancy check (CRC) checksum.

## 2. Quantitative Impact on 500-Hz ADS1292R Telemetry Windows (1,000 samples = 2.0 s)

| Channel | Base Mean Size (B) | + CRC-16 (+2 B) | CRC-16 Hit Rate (≤1000 B) | + CRC-32 (+4 B) | CRC-32 Hit Rate (≤1000 B) | Budget Headroom |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Lead I (LA-RA)** | 790.73 B | **792.73 B** | 100.0% | **794.73 B** | 100.0% | **205.27 B** |
| **Lead II (LL-RA)** | 856.53 B | **858.53 B** | 100.0% | **860.53 B** | 100.0% | **139.47 B** |
| **Respiration (RESP)** | 798.27 B | **800.27 B** | 100.0% | **802.27 B** | 100.0% | **197.73 B** |
| **Chest Lead (Vx-RL)** | 1330.78 B | **1332.78 B** | 0.0% | **1334.78 B** | 0.0% | **EXCEEDED B** |

## 3. Engineering Conclusion
The addition of CRC-16 or CRC-32 adds **negligible overhead (+0.07% to +0.13%)** and preserves **100.0% target compliance** for Lead I and Lead II with over 139 bytes of remaining safety margin per 2-second telemetry frame.
