"""
Analyze stellar mass surface densities near strong gravitational lenses,
comparing them against a Cold Dark Matter (CDM) mass surface density threshold.

Inputs:
  - CSV file containing lens stellar mass data with columns including:
      * 'mass_surface_density_Msun_per_Mpc2' (stellar surface density)
      * 'redshift' (optional, for filtering valid lenses)

Outputs:
  - Prints summary of fraction of lenses below CDM threshold for a range of stellar baryon fractions (f_star)
  - Saves a CSV file 'results/lens_threshold_summary.csv' with threshold results for reproducibility

Usage:
  - Update the INPUT_CSV path to your local data file or relative path
  - Run the script in an environment with pandas and numpy installed

Author: Michael Feldstein
Date: 2025-07-26
"""

import pandas as pd
import numpy as np
import os

# === CONFIG ===
INPUT_CSV = 'results/lens_stellar_mass_data.csv'  # replace with your CSV relative path
OUTPUT_CSV = 'results/lens_threshold_summary.csv'
CDM_THRESHOLD = 1e8  # Msun/kpc^2

# === LOAD DATA ===
df = pd.read_csv(INPUT_CSV)
print(f"Loaded {len(df)} lenses from {INPUT_CSV}")

# Convert surface density from Msun/Mpc^2 to Msun/kpc^2 (1 Mpc^2 = 1,000,000 kpc^2)
df['mass_surface_density_Msun_per_kpc2'] = df['mass_surface_density_Msun_per_Mpc2'] / 1e6

# Optional filtering for valid positive surface density and redshift if available
if 'redshift' in df.columns:
    df_filtered = df[(df['mass_surface_density_Msun_per_kpc2'] > 0) & (df['redshift'] > 0)].copy()
else:
    df_filtered = df[df['mass_surface_density_Msun_per_kpc2'] > 0].copy()

total_lenses = len(df_filtered)
print(f"Lenses with valid redshift and positive stellar surface density: {total_lenses}")

# Stellar baryon fractions (f_star) to test
f_star_values = np.arange(0.01, 0.21, 0.01)  # 0.01 to 0.20 step 0.01

# Calculate how many lenses fall below the CDM threshold at each f_star
results = []
for f_star in f_star_values:
    # Inferred total mass surface density = stellar surface density / f_star
    inferred_total_mass = df_filtered['mass_surface_density_Msun_per_kpc2'] / f_star
    below_threshold_count = (inferred_total_mass < CDM_THRESHOLD).sum()
    percent_below = 100 * below_threshold_count / total_lenses
    results.append({
        'f_star': round(f_star, 3),
        'lenses_below_threshold': below_threshold_count,
        'percent_below_threshold': round(percent_below, 2)
    })

# Save results to CSV
results_df = pd.DataFrame(results)
os.makedirs('results', exist_ok=True)
results_df.to_csv(OUTPUT_CSV, index=False)
print(f"\nSaved threshold summary to {OUTPUT_CSV}")

# Print summary table
print("\nSummary of lenses below CDM threshold:")
print(results_df.to_string(index=False))
