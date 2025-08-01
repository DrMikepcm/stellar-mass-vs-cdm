"""
stellar_mass_fraction_histogram.py

Generates a histogram of stellar mass fractions (f⋆ = M_star / M_lens) for a sample of strong gravitational lenses.

Features:
- Histogram of f⋆ distribution for 912 lenses.
- Vertical lines showing ΛCDM expectation (f⋆=0.03) and thresholds (0.05, 0.10, 0.20) capped at 0.042 for visualization.
- Sensitivity bands showing effect of ±25%, ±50%, and ±75% variation in stellar mass assumptions.
- Clear labels, legend, and grid for easy interpretation.

Usage:
- Replace the `load_lens_data()` function with your actual data loading code.
- Run the script: `python stellar_mass_fraction_histogram.py`
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
    """
    np.random.seed(0)
    N = 912
    M_star = 5e10 * np.random.lognormal(mean=0, sigma=0.5, size=N)
    M_lens = 1e12 * np.random.lognormal(mean=0, sigma=0.3, size=N)
    return M_star, M_lens

def compute_fstar(M_star, M_lens):
    """Compute stellar mass fraction."""
    return M_star / M_lens

def plot_fstar_distribution(fstar, fstar_variants):
    plt.figure(figsize=(10, 6))

    xmax = 0.042
    bins = np.linspace(0, xmax, 50)

    # Plot original fstar histogram
    plt.hist(fstar, bins=bins, alpha=0.6, label='Observed f*', color='blue', density=True)

    # Colors and labels for sensitivity variants
    colors = ['green', 'orange', 'red']
    alphas = [0.3, 0.25, 0.2]
    labels = [r'Observed f* (+25%)', r'Observed f* (+50%)', r'Observed f* (+75%)']

    # Plot positive sensitivity bands
    for i, scale in enumerate([1.25, 1.5, 1.75]):
        plt.hist(fstar * scale, bins=bins, alpha=alphas[i], color=colors[i], label=labels[i], density=True)

    # Plot negative sensitivity bands
    neg_colors = ['lightgreen', 'peachpuff', 'lightcoral']
    neg_labels = [r'Observed f* (-25%)', r'Observed f* (-50%)', r'Observed f* (-75%)']
    neg_alphas = [0.3, 0.25, 0.2]

    for i, scale in enumerate([0.75, 0.5, 0.25]):
        plt.hist(fstar * scale, bins=bins, alpha=neg_alphas[i], color=neg_colors[i], label=neg_labels[i], density=True)

    # Vertical lines for CDM expectation and thresholds
    cdm_threshold = 0.03
    thresholds = [0.05, 0.10, 0.20]

    plt.axvline(cdm_threshold, color='black', linestyle='--', linewidth=2, label=r'ΛCDM expectation (f* = 0.03)')
    for thresh in thresholds:
        if thresh <= xmax:
            plt.axvline(thresh, color='gray', linestyle=':', linewidth=1)

    # Note for thresholds beyond xmax
    if any(t > xmax for t in thresholds):
        plt.text(xmax*0.7, plt.gca().get_ylim()[1]*0.9, 'Other thresholds > 0.042 not shown', 
                 fontsize=9, color='gray')

    plt.xlabel(r'Stellar Mass Fraction $f_\star = M_\star / M_{\mathrm{lens}}$')
    plt.ylabel('Normalized Number of Lenses')
    plt.title('Stellar Mass Fract
