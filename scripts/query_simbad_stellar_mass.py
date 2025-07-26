"""
Script 1: Collect stellar mass environments around strong lenses.

Queries SDSS in a 20 arcmin radius around each lens from the lenscat catalog,
estimates stellar mass based on SDSS 'type', and computes surface mass density.

This cleaned version excludes unused early classifications (e.g., low/medium/high density).
"""

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

import os, time
import numpy as np
import pandas as pd
from lenscat import catalog
from astroquery.sdss import SDSS
from astropy.coordinates import SkyCoord, Angle
from astropy.table import vstack, Table
import astropy.units as u
from astropy.cosmology import Planck18 as cosmo

# Save location
SAVE_DIR = '/content/drive/MyDrive/lens_stellar_mass_results'
os.makedirs(SAVE_DIR, exist_ok=True)
print(f"Results will be saved to: {SAVE_DIR}")

# SDSS query helper
def query_sdss_tiled(center_coord, total_radius_deg=20/60, tile_radius_arcmin=3.0):
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
            time.sleep(0.5)

    if all_results:
        combined = vstack(all_results)
        coords_all = SkyCoord(ra=combined['ra'], dec=combined['dec'], unit='deg')
        mask = coords_all.separation(center_coord) <= Angle(total_radius_deg, u.deg)
        return combined[mask]
    else:
        return Table(names=['ra', 'dec', 'type'], dtype=[float, float, int])

# Estimate stellar mass
def sdss_type_to_mass(sdss_type):
    return 5e10 if sdss_type == 6 else 0  # SDSS type 6 = galaxy

# Convert to surface density
def surface_mass_density(total_mass, redshift, radius_arcmin=20):
    if redshift is None or np.isnan(redshift):
        return np.nan
    theta_rad = radius_arcmin * (np.pi / 180) / 60
    d_a = cosmo.angular_diameter_distance(redshift).to(u.Mpc).value
    radius_mpc = theta_rad * d_a
    area = np.pi * radius_mpc**2
    return total_mass / area

# Load and filter lens catalog
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

    results_df = pd.DataFrame(results)
    save_path = os.path.join(SAVE_DIR, 'lens_stellar_mass_progress.csv')
    results_df.to_csv(save_path, index=False)

    if (i + 1) % 25 == 0 or (i + 1) == len(filtered_df):
        print(f"-- Progress: {i+1}/{len(filtered_df)} lenses --")
        print(f"Results saved to: {save_path}")

print("All done! Final results saved to:", save_path)
