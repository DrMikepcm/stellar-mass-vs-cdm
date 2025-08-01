"""
stellar_mass_fraction_distribution.py

Generates a histogram of stellar mass fractions (f⋆ = M_star / M_lens) for a sample of strong gravitational lenses.

Features:
- Histogram of f⋆ distribution for 912 lenses.
- Vertical lines showing ΛCDM expectation (f⋆=0.03) and thresholds (0.05, 0.10, 0.20) capped at 0.042 for visualization.
- Sensitivity bands showing effect of ±25% variation in stellar mass assumptions.
- Optional breakdown of distribution by redshift bins.
- Clear labels, legend, and grid for easy interpretation.

Usage:
- Replace the `load_lens_data()` function with your actual data loading code.
- Run the script: `python stellar_mass_fraction_distribution.py`
- Requires: numpy, matplotlib

Author: Your Name
Date: 2025-08-01
"""

import numpy as np
import matplotlib.pyplot as plt

def load_lens_data():
    """
    Placeholder function to load lens data.
    Replace with your actual data loading logic.

    Returns:
        M_star (np.ndarray): Stellar mass array.
        M_lens (np.ndarray): Total lens mass array.
        z (np.ndarray): Redshift array (optional).
    """
    np.random.seed(0)
    N = 912
    M_star = 5e10 * np.random.lognormal(mean=0, sigma=0.5, size=N)  # example stellar masses
    M_lens = 1e12 * np.random.lognormal(mean=0, sigma=0.3, size=N)  # example lens masses
    z = np.random.uniform(0.1, 1.0, size=N)  # example redshifts
    return M_star, M_lens, z

def compute_fstar(M_star, M_lens):
    """Compute stellar mass fraction."""
    return M_star / M_lens

def plot_fstar_distribution(fstar, fstar_plus25, fstar_minus25, z=None):
    plt.figure(figsize=(10, 6))

    # Cap x-axis at 0.042 for better visual balance (not cramped)
    xmax = 0.042
    bins = np.linspace(0, xmax, 50)

    # Plot histogram of original fstar
    plt.hist(fstar, bins=bins, alpha=0.6, label='Observed f*', color='blue', density=True)

    # Plot histograms for sensitivity ±25%
    plt.hist(fstar_plus25, bins=bins, alpha=0.3, label=r'Observed f* (+25%)', color='green', density=True)
    plt.hist(fstar_minus25, bins=bins, alpha=0.3, label=r'Observed f* (-25%)', color='red', density=True)

    # Vertical lines for CDM expectation and thresholds
    cdm_threshold = 0.03
    thresholds = [0.05, 0.10, 0.20]
    plt.axvline(cdm_threshold, color='black', linestyle='--', linewidth=2, label=r'ΛCDM expectation (f* = 0.03)')
    # Only show thresholds up to xmax visually
    for thresh in thresholds:
        if thresh <= xmax:
            plt.axvline(thresh, color='gray', linestyle=':', linewidth=1)
    # Optionally add a note for thresholds beyond xmax
    if any(t > xmax for t in thresholds):
        plt.text(xmax*0.7, plt.gca().get_ylim()[1]*0.9, 'Other thresholds > 0.042 not shown', 
                 fontsize=9, color='gray')

    plt.xlabel(r'Stellar Mass Fraction $f_\star = M_\star / M_{\mathrm{lens}}$')
    plt.ylabel('Normalized Number of Lenses')
    plt.title('Stellar Mass Fraction Distribution for 912 Strong Lenses\n(Upper x-axis capped at 0.042 for clarity)')
    plt.legend()
    plt.xlim(0, xmax)
    plt.grid(True, alpha=0.3)

    # Optional redshift bin breakdown inset
    if z is not None:
        bins_z = [0.1, 0.4, 0.7, 1.0]
        plt.figure(figsize=(10, 6))
        for i in range(len(bins_z)-1):
            mask = (z >= bins_z[i]) & (z < bins_z[i+1])
            fstar_bin = fstar[mask]
            if len(fstar_bin) > 0:
                plt.hist(fstar_bin, bins=bins, alpha=0.6, label=f'z = {bins_z[i]:.2f}-{bins_z[i+1]:.2f}', density=True)
        plt.axvline(cdm_threshold, color='black', linestyle='--', linewidth=2)
        plt.xlabel(r'Stellar Mass Fraction $f_\star$')
        plt.ylabel('Normalized Number of Lenses')
        plt.title('f* Distribution by Redshift Bin\n(Upper x-axis capped at 0.042)')
        plt.legend()
        plt.xlim(0, xmax)
        plt.grid(True, alpha=0.3)
        plt.show()

    plt.show()

def main():
    M_star, M_lens, z = load_lens_data()
    fstar = compute_fstar(M_star, M_lens)
    fstar_plus25 = compute_fstar(M_star * 1.25, M_lens)
    fstar_minus25 = compute_fstar(M_star * 0.75, M_lens)
    plot_fstar_distribution(fstar, fstar_plus25, fstar_minus25, z)

if __name__ == "__main__":
    main()
