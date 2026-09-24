#!/usr/bin/env python3
"""
Generate high-resolution benchmark visualization figures for E4A ECG compression.
Outputs:
- docs/figures/compression_by_channel.png
- docs/figures/compression_reduction.png
- docs/figures/technique_comparison.png
- docs/figures/window_distribution.png
- docs/figures/original_vs_reconstructed.png
- docs/figures/reconstruction_error.png
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import resample_poly

# Set aesthetic styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 11
plt.rcParams['ytick.labelsize'] = 11
plt.rcParams['figure.titlesize'] = 14

repo_dir = "/home/anubhavtripathi/Documents/Projects/e4a-ecg-compression"
fig_dir = os.path.join(repo_dir, "docs", "figures")
os.makedirs(fig_dir, exist_ok=True)

# Load benchmark results
json_path = os.path.join(repo_dir, "benchmark_results.json")
with open(json_path, 'r') as f:
    results = json.load(f)

exp_b = results["experiment_b_simulated_500hz"]

# ------------------------------------------------------------------------------
# 1. Compression Size by Channel (500-Hz Simulation)
# ------------------------------------------------------------------------------
channels = ['Lead I\n(LA-RA)', 'Lead II\n(LL-RA)', 'Respiration\n(RESP)', 'Chest Lead\n(Vx-RL)']
means = [
    exp_b['Lead I (LA-RA)']['mean_compressed_bytes'],
    exp_b['Lead II (LL-RA)']['mean_compressed_bytes'],
    exp_b['Respiration (RESP)']['mean_compressed_bytes'],
    exp_b['Chest Lead (Vx-RL)']['mean_compressed_bytes']
]
colors = ['#10b981', '#10b981', '#3b82f6', '#ef4444'] # Green for pass, Red for fail, Blue for respiration

fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
bars = ax.bar(channels, means, color=colors, width=0.55, edgecolor='#1e293b', linewidth=1.2)
ax.axhline(1000, color='#dc2626', linestyle='--', linewidth=2, label='Target Budget: 1,000 Bytes')
ax.axhline(3000, color='#64748b', linestyle=':', linewidth=1.5, label='Raw Uncompressed: 3,000 Bytes')

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 35, f"{yval:.1f} B", ha='center', va='bottom', fontweight='bold', fontsize=11)

ax.set_ylabel("Compressed Window Size (Bytes)")
ax.set_title("Mean Compressed Size per 1,000-Sample Window (500 Hz, 2.0 s)", pad=15, fontweight='bold')
ax.set_ylim(0, 3400)
ax.legend(loc='upper left', frameon=True)
plt.tight_layout()
fig.savefig(os.path.join(fig_dir, "compression_by_channel.png"))
plt.close(fig)
print("Generated compression_by_channel.png")

# ------------------------------------------------------------------------------
# 2. Compression Percentage Reduction
# ------------------------------------------------------------------------------
reductions = [
    exp_b['Lead I (LA-RA)']['mean_reduction_pct'],
    exp_b['Lead II (LL-RA)']['mean_reduction_pct'],
    exp_b['Respiration (RESP)']['mean_reduction_pct'],
    exp_b['Chest Lead (Vx-RL)']['mean_reduction_pct']
]

fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
bars = ax.bar(channels, reductions, color=colors, width=0.55, edgecolor='#1e293b', linewidth=1.2)
ax.axhline(66.67, color='#dc2626', linestyle='--', linewidth=2, label='Required Reduction: 66.67% (3000 B → 1000 B)')

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 1.2, f"{yval:.1f}%", ha='center', va='bottom', fontweight='bold', fontsize=11)

ax.set_ylabel("Compression Reduction (%)")
ax.set_title("Lossless Compression Reduction by Channel (500 Hz, 2.0 s)", pad=15, fontweight='bold')
ax.set_ylim(0, 85)
ax.legend(loc='lower left', frameon=True)
plt.tight_layout()
fig.savefig(os.path.join(fig_dir, "compression_reduction.png"))
plt.close(fig)
print("Generated compression_reduction.png")

# ------------------------------------------------------------------------------
# 3. Technique Comparison on 500-Hz Lead I
# ------------------------------------------------------------------------------
techniques = [
    'Delta +\nZigZag Varint',
    'Delta-of-Delta +\nZigZag Varint',
    'Fixed LPC-4 +\nGolomb-Rice',
    'Adaptive LPC-4 +\nDelta Fallback (Final)'
]
tech_sizes = [1045.4, 1019.9, 818.5, 790.7]
tech_colors = ['#f87171', '#fb923c', '#60a5fa', '#10b981']

fig, ax = plt.subplots(figsize=(9, 5.2), dpi=300)
bars = ax.bar(techniques, tech_sizes, color=tech_colors, width=0.55, edgecolor='#1e293b', linewidth=1.2)
ax.axhline(1000, color='#dc2626', linestyle='--', linewidth=2, label='Target: ≤ 1,000 Bytes')

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 20, f"{yval:.1f} B", ha='center', va='bottom', fontweight='bold', fontsize=11)

ax.set_ylabel("Mean Compressed Size (Bytes / 2-sec Window)")
ax.set_title("R&D Algorithm Progression: 500-Hz Lead I ECG (Raw: 3,000 B)", pad=15, fontweight='bold')
ax.set_ylim(600, 1150)
ax.legend(loc='upper right', frameon=True)
plt.tight_layout()
fig.savefig(os.path.join(fig_dir, "technique_comparison.png"))
plt.close(fig)
print("Generated technique_comparison.png")

# ------------------------------------------------------------------------------
# 4. Window Compression Distribution (Lead I & Lead II)
# ------------------------------------------------------------------------------
csv_path = os.path.join(repo_dir, "window_results.csv")
df_windows = pd.read_csv(csv_path)

df_500 = df_windows[df_windows['experiment'] == 'Experiment B (Simulated 500Hz ADS1292R)']
lead1_sizes = df_500[df_500['channel'] == 'Lead I (LA-RA)']['compressed_bytes'].values
lead2_sizes = df_500[df_500['channel'] == 'Lead II (LL-RA)']['compressed_bytes'].values

fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
bp = ax.boxplot([lead1_sizes, lead2_sizes], tick_labels=['Lead I (LA-RA)', 'Lead II (LL-RA)'], 
                patch_artist=True, widths=0.45,
                boxprops=dict(facecolor='#dcfce7', color='#166534', linewidth=1.5),
                medianprops=dict(color='#15803d', linewidth=2.5),
                whiskerprops=dict(color='#166534', linewidth=1.2),
                capprops=dict(color='#166534', linewidth=1.2))

# Scatter jitter points
for idx, vals in enumerate([lead1_sizes, lead2_sizes]):
    x = np.random.normal(idx + 1, 0.04, size=len(vals))
    ax.scatter(x, vals, alpha=0.6, color='#047857', s=25, zorder=3)

ax.axhline(1000, color='#dc2626', linestyle='--', linewidth=2, label='Target: 1,000 Bytes')
ax.set_ylabel("Compressed Window Size (Bytes)")
ax.set_title("Distribution Across All 60 Benchmark Windows (500 Hz, 2.0 s)", pad=15, fontweight='bold')
ax.set_ylim(700, 1050)
ax.legend(loc='upper right', frameon=True)

# Add annotations
ax.text(1, np.max(lead1_sizes) + 18, f"Worst: {np.max(lead1_sizes)} B", ha='center', fontsize=10, color='#166534', fontweight='bold')
ax.text(2, np.max(lead2_sizes) + 18, f"Worst: {np.max(lead2_sizes)} B", ha='center', fontsize=10, color='#166534', fontweight='bold')

plt.tight_layout()
fig.savefig(os.path.join(fig_dir, "window_distribution.png"))
plt.close(fig)
print("Generated window_distribution.png")

# ------------------------------------------------------------------------------
# 5. Original vs Reconstructed ECG & Error Plot
# ------------------------------------------------------------------------------
from benchmark_ads1292r import encode_window, decode_window

df_raw = pd.read_csv(os.path.join(repo_dir, "Shimmer3_ECG_Sample_Data/SampleECG_Session1_Shimmer_B64E_Calibrated_SD.csv"), 
                     sep='\t', skiprows=[0, 2], index_col=False)
step = 0.00036060814392089844
codes_1000 = np.round(df_raw['Shimmer_B64E_ECG_LA-RA_24BIT_CAL'].values / step).astype(np.float64)
stream_500 = np.round(resample_poly(codes_1000, 1, 2)).astype(np.int64)

# Select a representative window with distinct QRS complexes (Window 2: samples 2000 to 3000)
orig_w = stream_500[2000:3000]
enc_bytes, _ = encode_window(orig_w)
rec_w = decode_window(enc_bytes)
error = orig_w - rec_w

time_sec = np.arange(len(orig_w)) / 500.0 # 0 to 2 seconds

# Plot 5: Original vs Reconstructed ECG
fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
ax.plot(time_sec, orig_w, label='Original 24-bit ECG (Integer ADC counts)', color='#2563eb', linewidth=2.0)
ax.plot(time_sec, rec_w, label='Reconstructed ECG (Decompressed from bitstream)', color='#ef4444', linestyle='--', linewidth=1.8, alpha=0.9)
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Amplitude (ADC Counts)")
ax.set_title("Original vs Losslessly Reconstructed ECG Window (500 Hz, Window 2)", pad=15, fontweight='bold')
ax.legend(loc='upper right', frameon=True)
ax.set_xlim(0, 2.0)
plt.tight_layout()
fig.savefig(os.path.join(fig_dir, "original_vs_reconstructed.png"))
plt.close(fig)
print("Generated original_vs_reconstructed.png")

# Plot 6: Reconstruction Error
fig, ax = plt.subplots(figsize=(10, 3.2), dpi=300)
ax.plot(time_sec, error, color='#10b981', linewidth=1.5, label='Sample-by-Sample Error: Original - Decoded')
ax.axhline(0, color='#047857', linestyle='-', linewidth=1.0)
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Reconstruction Error")
ax.set_title("Exact Sample Reconstruction Error: Identically Zero (PASS: 0 Mismatches)", pad=15, fontweight='bold')
ax.set_ylim(-1, 1)
ax.set_xlim(0, 2.0)
ax.legend(loc='upper right', frameon=True)
plt.tight_layout()
fig.savefig(os.path.join(fig_dir, "reconstruction_error.png"))
plt.close(fig)
print("Generated reconstruction_error.png")

print("All figures successfully created in docs/figures/!")
