# analyze_stellar_mass.py
#
# Part of: Stellar Mass Contributions in Strong Lenses: Indications of Tension with ΛCDM Baryon Fractions
#
# This script performs a comparative statistical analysis of stellar mass surface
# density distributions between a sample of strong gravitational lens galaxies
# and a control sample of random sky galaxies. It utilizes synthetic data
# generated based on provided summary statistics for demonstration.
#
# Key Features:
# - Estimates log-normal distribution parameters from mean and standard deviation.
# - Generates synthetic stellar mass surface density data for both lens and random samples.
# - Conducts non-parametric statistical tests:
#   - Kolmogorov-Smirnov (K-S) test to compare distribution shapes.
#   - Mann-Whitney U test (Wilcoxon Rank-Sum Test) to compare medians.
# - Generates visual representations of the distributions:
#   - Overlaid histograms (with logarithmic x-axis).
#   - Kernel Density Estimates (KDEs) on a logarithmic scale.
#   - Box plots for quick visual comparison of central tendency and spread.
#
# The results of this analysis aim to determine if there are statistically
# significant differences in the stellar mass environments of lens galaxies
# compared to typical sky regions.
#
# Author: Michael Feldstein, Independent Researcher
# Date: August 5, 2025
# License: MIT License

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import lognorm # Stellar mass distributions are often log-normal
import os # Import os for path operations

# --- 1. Define the Known Summary Statistics (from your provided data) ---
# These statistics are used to generate synthetic data for demonstration purposes.
# In a real analysis, you would load your actual data from files.

# Lens Sample Stellar Mass Surface Density (Sigma_star in Msun/kpc^2)
# Mean: 9.97e6
# Median: 4.79e6
# Std Dev: 3.26e7
# Count: 912

# Random Sky Sample Stellar Mass Surface Density (Sigma_star in Msun/kpc^2)
# Mean: 1.03e6 (derived from 86.07 mean galaxy count)
# Median: 8.60e5 (derived from 86.07 mean galaxy count, assuming similar distribution)
# Std Dev: 9.76e4 (derived from 9.76 std dev of galaxy count, assuming similar distribution)
# Note: The median for randoms was 1.00e4 in a previous summary you provided,
# but the 8.60e5 is derived consistently with the 1.03e6 mean from the 86.07 galaxy count.
# We will use the 1.03e6 mean and 8.60e5 median for consistency with the derived mean.
# If you have an exact median value for the 1.03e6 mean, please provide it.

# For generating synthetic data, we need to estimate parameters for a log-normal distribution.
# A log-normal distribution is often a good fit for astronomical quantities like mass.
# Parameters for log-normal distribution: s (shape), loc (location/shift), scale (scale)
# Mean = exp(mu + sigma^2/2)
# Median = exp(mu)
# Variance = (exp(sigma^2) - 1) * exp(2*mu + sigma^2)

# Function to estimate log-normal parameters from mean and std dev
def estimate_lognorm_params(mean, std_dev):
    """
    Estimates the shape (s) and scale (scale) parameters for a log-normal distribution
    given its arithmetic mean and standard deviation.
    The location (loc) parameter is assumed to be 0.
    """
    # Handle cases where mean is non-positive or std_dev is negative, which would lead to errors
    if mean <= 0 or std_dev < 0:
        print(f"Warning: Invalid input for log-normal parameter estimation (mean={mean}, std_dev={std_dev}). "
              "Returning default parameters.")
        return 1.0, 0.0, 1.0 # Default values, or raise an error depending on desired strictness

    # Calculate variance
    variance = std_dev**2

    # Estimate mu and sigma for the underlying normal distribution
    # sigma_sq = ln(1 + (std_dev/mean)^2)
    # mu = ln(mean) - sigma_sq/2
    sigma_sq = np.log(1 + (variance / (mean**2)))
    mu = np.log(mean) - sigma_sq / 2

    s = np.sqrt(sigma_sq)  # Shape parameter for scipy.stats.lognorm
    scale = np.exp(mu)     # Scale parameter for scipy.stats.lognorm (which is exp(mu))
    return s, 0, scale # loc (shift) is typically 0 for the standard log-normal in scipy

num_samples = 912 # Number of synthetic data points to generate for each sample

# Estimate parameters for Lens data
s_lens, loc_lens, scale_lens = estimate_lognorm_params(9.97e6, 3.26e7)
# Generate synthetic lens data
# Robustness check for log-normal parameters to prevent non-finite values or errors
if not np.isfinite([s_lens, scale_lens]).all() or s_lens <= 0 or scale_lens <= 0:
    print("Warning: Lens log-normal parameter estimation resulted in problematic values. Using fallback for data generation.")
    # Fallback to a reasonable log-normal distribution if estimation fails
    lens_data = np.random.lognormal(mean=np.log(9.97e6), sigma=1.0, size=num_samples)
else:
    lens_data = lognorm.rvs(s=s_lens, loc=loc_lens, scale=scale_lens, size=num_samples)

# Estimate parameters for Random data
s_random, loc_random, scale_random = estimate_lognorm_params(1.03e6, 9.76e4)
# Generate synthetic random data
if not np.isfinite([s_random, scale_random]).all() or s_random <= 0 or scale_random <= 0:
    print("Warning: Random log-normal parameter estimation resulted in problematic values. Using fallback for data generation.")
    # Fallback to a reasonable log-normal distribution if estimation fails
    random_data = np.random.lognormal(mean=np.log(1.03e6), sigma=0.5, size=num_samples)
else:
    random_data = lognorm.rvs(s=s_random, loc=loc_random, scale=scale_random, size=num_samples)

# Ensure no zeros or negative values in generated data (important for log-scale plots)
# Replace non-positive values with a very small positive number (machine epsilon)
lens_data[lens_data <= 0] = np.finfo(float).eps
random_data[random_data <= 0] = np.finfo(float).eps

print("--- Synthetic Data Generated ---")
print(f"Synthetic Lens Data (N={len(lens_data)}): Mean={np.mean(lens_data):.2e}, Median={np.median(lens_data):.2e}, Std Dev={np.std(lens_data):.2e}")
print(f"Synthetic Random Data (N={len(random_data)}): Mean={np.mean(random_data):.2e}, Median={np.median(random_data):.2e}, Std Dev={np.std(random_data):.2e}")

print("\n--- 2. Non-Parametric Statistical Tests ---")

# --- Kolmogorov-Smirnov (K-S) Test ---
# The K-S test determines if two samples are drawn from the same continuous distribution.
# Null Hypothesis (H0): The two samples are drawn from the same distribution.
# Alternative Hypothesis (H1): The two samples are drawn from different distributions.
ks_statistic, ks_p_value = stats.ks_2samp(lens_data, random_data)
print(f"Kolmogorov-Smirnov (K-S) Test:")
print(f"  Statistic: {ks_statistic:.3f}")
print(f"  P-value: {ks_p_value:.3e}")
if ks_p_value < 0.05:
    print("  Conclusion: The distributions of stellar mass surface density for lens and random samples are statistically different (p < 0.05).")
else:
    print("  Conclusion: No significant difference found in the distributions (p >= 0.05).")

# --- Mann-Whitney U Test (Wilcoxon Rank-Sum Test) ---
# This is a non-parametric alternative to the independent samples t-test.
# It tests if two independent samples are from populations with the same median (or distribution shapes).
# Null Hypothesis (H0): The medians of the two populations are equal.
# Alternative Hypothesis (H1): The medians of the two populations are not equal.
mw_statistic, mw_p_value = stats.mannwhitneyu(lens_data, random_data, alternative='two-sided')
print(f"\nMann-Whitney U Test:")
print(f"  Statistic: {mw_statistic:.3f}")
print(f"  P-value: {mw_p_value:.3e}")
if mw_p_value < 0.05:
    print("  Conclusion: The median stellar mass surface densities for lens and random samples are statistically different (p < 0.05).")
else:
    print("  Conclusion: No significant difference found in the medians (p >= 0.05).")

print("\n--- 3. Visual Representations ---")

# Ensure the 'figures' directory exists for saving plots
if not os.path.exists('figures'):
    os.makedirs('figures')

# --- Overlaid Histograms ---
plt.figure(figsize=(12, 7))
# Create logarithmically spaced bins for the histogram due to the wide range of stellar mass densities
bins = np.logspace(np.log10(min(lens_data.min(), random_data.min())),
                   np.log10(max(lens_data.max(), random_data.max())), 50)
plt.hist(lens_data, bins=bins, alpha=0.6, label='Lens Sample', color='salmon', edgecolor='black', density=True)
plt.hist(random_data, bins=bins, alpha=0.6, label='Random Sky Sample', color='skyblue', edgecolor='black', density=True)
plt.xscale('log') # Set x-axis to logarithmic scale
plt.xlabel("Stellar Mass Surface Density (M$_{\\odot}$/kpc$^2$)", fontsize=12) # Using LaTeX for Msun
plt.ylabel("Normalized Frequency", fontsize=12)
plt.title("Overlaid Histograms of Stellar Mass Surface Density", fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout() # Adjust layout to prevent labels from overlapping
plot_filename_hist = 'stellar_mass_histograms.png'
plt.savefig(os.path.join('figures', plot_filename_hist), dpi=300)
print(f"Histogram saved to figures/{plot_filename_hist}")
plt.show()

# --- Kernel Density Estimates (KDEs) ---
plt.figure(figsize=(12, 7))
# For highly skewed data like stellar mass, it's often better to perform KDE on log-transformed data
log_lens_data = np.log10(lens_data)
log_random_data = np.log10(random_data)

# Define a common range for the KDE x-axis based on the min/max of log-transformed data
x_min_kde = min(log_lens_data.min(), log_random_data.min())
x_max_kde = max(log_lens_data.max(), log_random_data.max())
x_vals_kde = np.linspace(x_min_kde, x_max_kde, 500)

# Compute KDEs for both samples
kde_lens = stats.gaussian_kde(log_lens_data)
kde_random = stats.gaussian_kde(log_random_data)

# Plot KDEs, converting x-axis back to linear scale for interpretation
plt.plot(10**x_vals_kde, kde_lens(x_vals_kde), label='Lens Sample (KDE)', color='red', linewidth=2)
plt.plot(10**x_vals_kde, kde_random(x_vals_kde), label='Random Sky Sample (KDE)', color='blue', linewidth=2)
plt.xscale('log') # Set x-axis to logarithmic scale
plt.xlabel("Stellar Mass Surface Density (M$_{\\odot}$/kpc$^2$)", fontsize=12)
plt.ylabel("Density", fontsize=12)
plt.title("Kernel Density Estimates of Stellar Mass Surface Density", fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plot_filename_kde = 'stellar_mass_kdes.png'
plt.savefig(os.path.join('figures', plot_filename_kde), dpi=300)
print(f"KDE plot saved to figures/{plot_filename_kde}")
plt.show()

# --- Box Plots ---
plt.figure(figsize=(8, 6))
data_to_plot = [lens_data, random_data]
labels = ['Lens Sample', 'Random Sky Sample']
plt.boxplot(data_to_plot, labels=labels, sym='o', vert=True, patch_artist=True,
            boxprops=dict(facecolor='#ADD8E6', edgecolor='blue'), # Light blue box
            medianprops=dict(color='red', linewidth=2), # Red median line
            whiskerprops=dict(color='blue'),
            capprops=dict(color='blue'),
            flierprops=dict(marker='o', markerfacecolor='purple', markersize=6, alpha=0.6)) # Outlier properties
plt.ylabel("Stellar Mass Surface Density (M$_{\\odot}$/kpc$^2$)", fontsize=12)
plt.title("Box Plots of Stellar Mass Surface Density", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7, axis='y') # Grid only on y-axis for cleaner look
plt.tight_layout()
plot_filename_box = 'stellar_mass_box_plots.png'
plt.savefig(os.path.join('figures', plot_filename_box), dpi=300)
print(f"Box plot saved to figures/{plot_filename_box}")
plt.show()

print("\nScript execution complete. Statistical test results and plots generated.")
print("The plots are saved in the 'figures/' directory.")
