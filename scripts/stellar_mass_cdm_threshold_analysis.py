import pandas as pd
import numpy as np

# Path to the saved query results CSV (adjust if needed)
progress_file = 'lens_stellar_mass_progress.csv'

# Load data
df = pd.read_csv(progress_file)

# Convert surface density units: M_sun/Mpc^2 to M_sun/kpc^2
df['mass_surface_density_kpc2'] = df['mass_surface_density_Msun_per_Mpc2'] / 1e6

# Filter for valid redshift and positive surface density
df_filtered = df[(df['mass_surface_density_kpc2'] > 0) & (df['redshift'] > 0)].copy()

total_lenses = len(df_filtered)

print(f"Total lenses with valid redshift and non-zero stellar surface density: {total_lenses}\n")

# CDM threshold (in M_sun/kpc^2)
cdm_threshold = 1e8

# List of stellar mass fraction (f_star) values to test
f_star_values = [0.01, 0.03, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.20]

print(f"{'f_star':>7} | {'Below Threshold':>15} | {'Total Lenses':>12} | {'Percent Below Threshold':>23}")
print("-" * 65)

for f_star in f_star_values:
    # Infer total mass by dividing stellar surface density by f_star
    inferred_total = df_filtered['mass_surface_density_kpc2'] / f_star

    # Count how many lenses fall below the CDM threshold
    below_threshold = (inferred_total < cdm_threshold)
    n_below = below_threshold.sum()
    pct_below = n_below / total_lenses * 100

    print(f"{f_star:7.2f} | {n_below:15d} | {total_lenses:12d} | {pct_below:23.1f}%")
