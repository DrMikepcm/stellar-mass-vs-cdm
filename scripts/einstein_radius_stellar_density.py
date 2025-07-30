"""
einstein_radius_stellar_density.py

Estimate the stellar surface mass density of the Bullet Cluster's core
using an assumed stellar mass and Einstein radius approximation.

This simple calculation assumes a circular lensing region defined by
the Einstein radius and computes the average stellar surface density
(Σ_* = M_* / area).

Author: Michael Feldstein
Date: 2025-07-30
"""

import numpy as np

def calculate_stellar_surface_density(stellar_mass, einstein_radius_kpc):
    """
    Calculate stellar surface mass density (M_sun/kpc^2)
    given stellar mass (M_sun) and Einstein radius (kpc).
    """
    area = np.pi * einstein_radius_kpc**2
    surface_density = stellar_mass / area
    return surface_density

if __name__ == "__main__":
    # Stellar mass estimate (from WISE photometry or other method)
    stellar_mass = 3.9e10  # solar masses

    # Typical Einstein radius for strong lens (kpc)
    einstein_radius_kpc = 5.0

    sigma_star = calculate_stellar_surface_density(stellar_mass, einstein_radius_kpc)

    print(f"Assumed stellar mass: {stellar_mass:.2e} M_sun")
    print(f"Einstein radius: {einstein_radius_kpc} kpc")
    print(f"Estimated stellar surface mass density: {sigma_star:.2e} M_sun/kpc^2")
