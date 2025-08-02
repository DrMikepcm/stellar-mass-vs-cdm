"""
plot_threshold_analysis_results.py

This script generates a line plot visualizing the consistency of strong gravitational lenses
with the Cold Dark Matter (CDM) total mass threshold. It shows the percentage of lenses
whose inferred total mass surface density falls below the canonical CDM threshold,
as a function of an assumed stellar baryon fraction (f_star).

The plot includes Poisson statistical uncertainties as error bars.

Inputs:
- CSV file named 'stellar_mass_thresholds_results.csv' in the same directory or specified path.
  This file is expected to have the following columns:
    - 'f_star': Assumed stellar baryon fraction.
    - 'lenses_below_threshold': Count of lenses below the CDM threshold for that f_star.
    - 'percent_below_threshold': Percentage of lenses below the CDM threshold for that f_star.

Outputs:
- Displays a matplotlib plot.

Usage:
- Ensure you have 'pandas', 'numpy', and 'matplotlib' installed.
- Place 'stellar_mass_thresholds_results.csv' in the specified input_csv_path.
- If running in Google Colab, remember to mount your Google Drive first.

Author: Michael Feldstein
Date: 2025-08-02
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def plot_threshold_analysis_results(input_csv_path):
    """
    Generates a line plot showing the percentage of lenses below the CDM threshold
    for different assumed stellar baryon fractions (f_star), with Poisson error bars.

    Args:
        input_csv_path (str): The path to the CSV file containing the threshold analysis results.
                              This file is expected to have 'f_star', 'lenses_below_threshold',
                              and 'percent_below_threshold' columns.
    """
    if not os.path.exists(input_csv_path):
        print(f"Error: Input CSV file not found at '{input_csv_path}'.")
        print("Please ensure the file is correctly downloaded or located in your mounted Google Drive.")
        return

    try:
        df_results = pd.read_csv(input_csv_path)
    except Exception as e:
        print(f"Error loading data from '{input_csv_path}': {e}")
        print("Please check the file path and its contents.")
        return

    # Ensure required columns are present
    required_cols = ['f_star', 'lenses_below_threshold', 'percent_below_threshold']
    if not all(col in df_results.columns for col in required_cols):
        print(f"Error: Required columns {required_cols} not found in '{input_csv_path}'.")
        print("Please ensure the CSV file is correctly formatted from the threshold analysis.")
        return

    # Calculate total number of lenses (assuming it's constant across f_star values)
    # This assumes 'lenses_below_threshold' is a count, and 0.01 f_star might have 0 lenses below threshold.
    # We need the total number of valid lenses from the original analysis.
    # For the provided data, total_lenses = 912.
    total_lenses = 912 # Based on previous context of 912 lenses in your sample

    # Calculate Poisson errors for the percentage
    # Error on count N is sqrt(N)
    # Error on percentage = (sqrt(N) / Total) * 100
    df_results['error_percent'] = (np.sqrt(df_results['lenses_below_threshold']) / total_lenses) * 100
    # Handle cases where count_below is 0, sqrt(0) is 0, which is correct.

    # Create the plot
    plt.figure(figsize=(10, 6))

    plt.errorbar(df_results['f_star'], df_results['percent_below_threshold'],
                 yerr=df_results['error_percent'],
                 marker='o', linestyle='-', color='indigo', linewidth=2, markersize=6,
                 capsize=4, label='Percentage of Lenses Below CDM Threshold')

    # Add labels and title
    plt.xlabel(r'Assumed Stellar Baryon Fraction ($f_\star$)', fontsize=12)
    plt.ylabel('Percentage of Lenses Below CDM Threshold (%)', fontsize=12)
    plt.title('Consistency of Lenses with CDM Threshold vs. Assumed Stellar Baryon Fraction', fontsize=14)

    # Add a horizontal line at 100% for context
    plt.axhline(100, color='gray', linestyle=':', linewidth=1, label='100% of Lenses')

    # Highlight the 0.03 CDM expectation for f_star on the x-axis
    f_star_0_03_row = df_results[df_results['f_star'] == 0.03]
    if not f_star_0_03_row.empty:
        percent_at_0_03 = f_star_0_03_row['percent_below_threshold'].iloc[0]
        plt.axvline(0.03, color='red', linestyle='--', linewidth=1.5,
                    label=f'CDM f* expectation (0.03): {percent_at_0_03:.1f}% below threshold')
        plt.plot(0.03, percent_at_0_03, 'o', color='red', markersize=8) # Mark the point

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.show()

# --- How to run the plotting function ---
if __name__ == "__main__":
    # 1. Ensure your Google Drive is mounted in a separate cell at the top of your notebook:
    #    from google.colab import drive
    #    drive.mount('/content/drive')

    # 2. The correct path to your 'stellar_mass_thresholds_results.csv' is:
    input_csv_path_from_drive = '/content/drive/MyDrive/lens_stellar_mass_results/stellar_mass_thresholds_results.csv'

    # Call the plotting function with the path from your mounted Drive
    plot_threshold_analysis_results(input_csv_path=input_csv_path_from_drive)
