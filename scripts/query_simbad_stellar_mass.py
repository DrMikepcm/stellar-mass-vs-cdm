"""
lens_stellar_mass_sdss_query.py

Queries SDSS photometric data in tiled 20 arcmin radius fields around strong gravitational lenses 
from the lenscat catalog. Estimates stellar mass assuming SDSS 'type' classification and computes 
stellar mass surface density within the 20 arcmin radius.

This version excludes the unused low/medium/high density categories from earlier drafts.

Outputs:
- Incremental CSV progress saved locally (adjust SAVE_DIR path as needed)

Usage:
- Requires: lenscat, astroquery, astropy, pandas, numpy
- Run in any Python environment with internet access.
- For Google Colab users: mount your Google Drive and set SAVE_DIR accordingly.

Author: Michael Feldstein  
Date: 2025-07-26
"""

import os
import time
import numpy as np
import pandas as pd
from lenscat import catalog
from astroquery.sdss import SDSS
from astropy.coordinates import SkyCoord, Angle
from astropy.table import vstack, Table
import astropy.units as u
from astropy.cosmology import Planck18 as cosmo

# === USER CONFIGURATION ===
# Change this to your desired local or mounted directory path for saving results:
SAVE_DIR = './lens_stellar_mass_results'
os.makedirs(SAVE_DIR, exist_ok=True)
print(f"Results will be saved to: {SAVE_DIR}")

def query_sdss_tiled(center_coord, total_radius_deg=20/60, tile_radius_arcmin=3.0):
    """
    Query SDSS in tiled patches within total_radius_deg around center_coord.
    Tiles are square grid steps with tile_radius_arcmin radius circles overlapping.

    Returns astropy Table of combined photometric objects within total radius.
    """
    tile_radius_deg = tile_radius_arcmin / 60.0
    n_tiles_side = int(np.ceil((2 * total_radius_deg) / tile_radius_deg))
    all_results = []

    ra_offsets = np.linspace(-total_radius_deg, total_radius_deg, n_tiles_side)
    dec_offsets = np.linspace(-total_radius_deg, total_radius_deg, n_tiles_side)

    for ra_off in ra_offsets:
        for dec_off in dec_offsets:
            tile_center = SkyCoord(ra=center_coord.ra.deg + ra_off,
                                   dec=center_coord.dec.deg + dec_off,
                                   unit='deg')
            try:
                result = SDSS.query_region(
                    tile_center,
                    radius=Angle(tile_radius_arcmin, u.arcmin),
                    spectro=False,
                    photoobj_fields=['ra', 'dec', 'type']
                )
                if result is not None and len(result) > 0:
                    all_results.append(result)
            except Exception as e:
                print(f"Error querying tile at RA={tile_center.ra.deg:.4f}, DEC={tile_center.dec.deg:.4f}: {e}")
            time.sleep(0.5)  # polite delay to avoid hammering server

    if all_results:
        combined = vstack(all_results)
        coords_all = SkyCoord(ra=combined['ra'], dec=combined['dec'], unit='deg')
        mask = coords_all.separation(center_coord) <= Angle(total_radius_deg, u.deg)
        return combined[mask]
    else:
        # Return empty table with expected columns if no results
        return Table(names=['ra', 'dec', 'type'], dtype=[float, float, int])

def sdss_type_to_mass(sdss_type):
    """
    Convert SDSS photometric object 'type' to stellar mass estimate.
    Assumes type=6 (galaxy) has mass 5e10 Msun, else zero.
    """
    return 5e10 if sdss_type == 6 else 0

def surface_mass_density(total_mass, redshift, radius_arcmin=20):
    """
    Calculate stellar mass surface density in Msun/Mpc^2 within given radius_arcmin
    using angular diameter distance from redshift (Planck18 cosmology).
    Returns np.nan if redshift is invalid.
    """
    if redshift is None or np.isnan(redshift):
        return np.nan
    theta_rad = radius_arcmin * (np.pi / 180) / 60  # convert arcmin to radians
    d_a = cosmo.angular_diameter_distance(redshift).to(u.Mpc).value
    radius_mpc = theta_rad * d_a
    area = np.pi * radius_mpc**2
    return total_mass / area

# Load lens catalog and filter valid redshifts
cat = catalog
df = cat.to_pandas()
df['zlens'] = pd.to_numeric(df['zlens'], errors='coerce')
filtered_df = df.dropna(subset=['zlens']).reset_index(drop=True)

print(f"Total lenses in catalog: {len(df)}")
print(f"Lenses after filtering valid redshifts: {len(filtered_df)}")

results = []

for i, lens in filtered_df.iterrows():
    lens_id = lens['name']
    ra = lens['RA']
    dec = lens['DEC']
    z = lens['zlens']

    print(f"Processing lens {i+1}/{len(filtered_df)}: {lens_id} (RA={ra:.4f}, DEC={dec:.4f}, z={z:.3f})")

    center_coord = SkyCoord(ra=ra, dec=dec, unit='deg')
    galaxies = query_sdss_tiled(center_coord)

    total_mass = sum(sdss_type_to_mass(t) for t in galaxies['type']) if len(galaxies) else 0.0
    sigma = surface_mass_density(total_mass, z)

    results.append({
        'lens_id': lens_id,
        'ra': ra,
        'dec': dec,
        'redshift': z,
        'total_mass_Msun': total_mass,
        'mass_surface_density_Msun_per_Mpc2': sigma
    })

    # Save incremental results after each lens processed
    results_df = pd.DataFrame(results)
    save_path = os.path.join(SAVE_DIR, 'lens_stellar_mass_progress.csv')
    results_df.to_csv(save_path, index=False)

    if (i + 1) % 25 == 0 or (i + 1) == len(filtered_df):
        print(f"-- Progress: {i+1}/{len(filtered_df)} lenses --")
        print(f"Results saved to: {save_path}")

print("All done! Final results saved to:", save_path)
