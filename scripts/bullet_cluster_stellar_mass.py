"""
bullet_cluster_stellar_mass.py

This script performs a focused stellar mass estimation near the Bullet Cluster
(1E 0657-558) by:

1. Querying SIMBAD for galaxy objects within a 0.5 arcminute radius.
2. Querying the WISE AllWISE catalog for infrared sources in the same region.

The output includes counts, positions, object types, and WISE magnitudes,
as well as a simple stellar mass estimate based on the number of galaxies found.

Requires:
- astroquery
- astropy
- pandas

Usage:
    python scripts/bullet_cluster_stellar_mass.py
"""

from astroquery.simbad import Simbad
from astroquery.irsa import Irsa
from astropy.coordinates import SkyCoord, Angle
import astropy.units as u
import pandas as pd

# Coordinates of the Bullet Cluster (J2000)
BULLET_CLUSTER_COORD = SkyCoord(ra=104.656, dec=-55.679, unit='deg')

def query_simbad_galaxies(center_coord, radius_arcmin=0.5):
    """
    Query SIMBAD database for galaxy-type objects within radius_arcmin of center_coord.

    Parameters:
    - center_coord : astropy.coordinates.SkyCoord
    - radius_arcmin : float, search radius in arcminutes

    Returns:
    - astropy Table of filtered galaxy objects or None if none found
    """
    custom_simbad = Simbad()
    custom_simbad.reset_votable_fields()
    custom_simbad.add_votable_fields('otype', 'ra', 'dec')

    radius_deg = radius_arcmin / 60.0
    result = custom_simbad.query_region(center_coord, radius=Angle(radius_deg, u.deg))
    if result is None or len(result) == 0:
        print("No SIMBAD objects found.")
        return None

    galaxy_types = ['G', 'Galaxy', 'GiC', 'Glx', 'AGN', 'LIN', 'BLL', 'SyG', 'QSO']
    otypes = [otype.decode('utf-8') if isinstance(otype, bytes) else otype for otype in result['otype']]
    mask = [otype in galaxy_types for otype in otypes]

    filtered = result[mask]
    return filtered

def query_wise_sources(center_coord, radius_arcmin=0.5):
    """
    Query WISE AllWISE catalog for sources within radius_arcmin of center_coord.

    Parameters:
    - center_coord : astropy.coordinates.SkyCoord
    - radius_arcmin : float, search radius in arcminutes

    Returns:
    - pandas DataFrame of WISE sources or None if none found
    """
    search_radius = radius_arcmin * u.arcmin
    result = Irsa.query_region(center_coord, catalog="allwise_p3as_psd", spatial='Cone', radius=search_radius)
    if len(result) == 0:
        print("No WISE sources found.")
        return None
    return result.to_pandas()

if __name__ == "__main__":
    print("=== Querying SIMBAD for galaxies near the Bullet Cluster ===")
    galaxies = query_simbad_galaxies(BULLET_CLUSTER_COORD, radius_arcmin=0.5)
    if galaxies is not None:
        print(f"Galaxies found within 0.5 arcmin: {len(galaxies)}")
        print(galaxies['ra', 'dec', 'otype'])
        estimated_mass = len(galaxies) * 5e10  # Approximate stellar mass per galaxy [M_sun]
        print(f"Estimated total stellar mass from SIMBAD galaxies: {estimated_mass:.2e} M☉")
    else:
        print("No galaxies found in SIMBAD query.")

    print("\n=== Querying WISE sources near the Bullet Cluster ===")
    wise_sources = query_wise_sources(BULLET_CLUSTER_COORD, radius_arcmin=0.5)
    if wise_sources is not None:
        print(f"WISE sources found within 0.5 arcmin: {len(wise_sources)}")
        display_cols = ['designation', 'ra', 'dec', 'w1mpro', 'w2mpro']
        print(wise_sources[display_cols].to_string(index=False))
    else:
        print("No WISE sources found in query.")
