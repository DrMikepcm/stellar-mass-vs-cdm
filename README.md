# Stellar Mass Surface Densities in Strong Gravitational Lenses

## Overview
This repository analyzes stellar mass distributions in 912 strong gravitational lensing systems, revealing a significant tension with standard Cold Dark Matter (LambdaCDM) model predictions.

Assuming a typical stellar baryon fraction, most lenses have stellar mass surface densities that imply a total mass well above the canonical LambdaCDM strong lensing threshold. This suggests that the stellar component may play a larger role in the lensing mass budget than commonly assumed.

## Key Findings
- **High-Density Environments:** Only 4.6% of the 912 lenses have an inferred total mass density below the LambdaCDM threshold (assuming a stellar baryon fraction of f_\* = 0.03).
- **Lenses vs. Random Fields:** The mean stellar mass surface density of the lens sample is ~10 times higher than that of a random sky sample, indicating that lenses are preferentially located in high-density environments.
- **Bullet Cluster Case Study:** A localized analysis of the Bullet Cluster's core shows a stellar mass density nearly two orders of magnitude above the standard LambdaCDM strong lensing threshold.

## Repository Contents
- `notebooks/`: Jupyter notebooks for interactive data exploration and visualization.
- `results/`:  Raw data files, including the lens sample and random sky control fields/Plots and data outputs, including mass density comparisons.
- `scripts/`: Python scripts to reproduce the full analysis from data acquisition to final figures.

## Getting Started
To reproduce the full analysis, follow these steps:

**Query Data**: Use lenscat and astroquery to retrieve data and compute stellar mass densities.
   ```bash
   python scripts/query_simbad_stellar_mass.py

1.  **Query Stellar Mass Environments:**
    This script uses `lenscat` and `astroquery` to query the SIMBAD database for stellar-like objects within 20 arcminutes of each strong lens, computing a projected stellar mass surface density.

    ```bash
    python scripts/query_simbad_stellar_mass.py
    ```

2.  **Analyze Stellar Mass Distributions:**
    This script performs statistical comparisons between the lens sample and random sky fields, generating plots like `Box_plots.png`, `Kernel_Density.png`, and `Overlaid_historgram_radom_versus_lens.png`.

    ```bash
    python scripts/analyze_stellar_mass.py
    ```

3.  **Perform CDM Threshold Analysis:**
    This script compares estimated stellar surface densities to $\Lambda$CDM expectations based on a fiducial stellar baryon fraction (e.g., $f_\star = 0.05$). It outputs percentile tables and the `consistency_plot.png`.

    ```bash
    python scripts/stellar_mass_cdm_threshold_analysis.py
    ```

### Bullet Cluster Case Study Scripts

These scripts provide independent methods to estimate the stellar mass surface density in the Bullet Cluster field:

* **WISE W1-band Estimation:** Uses WISE W1-band infrared flux measurements (within a 0.5′ aperture) to estimate stellar mass via luminosity-to-mass conversions.

    ```bash
    python scripts/bullet_cluster_stellar_mass.py
    ```

* **Einstein Radius Approximation:** Estimates lensing mass from a circular Einstein radius approximation (~5 kpc), converting the angular radius to enclosed mass using standard lensing equations.

    ```bash
    python scripts/einstein_radius_stellar_density.py
    ```

* **SED-based Stellar Mass:** Retrieves and integrates catalog-based SED stellar masses from SIMBAD/VizieR for galaxies in the Bullet Cluster region to derive a total projected stellar mass.

    ```bash
    python scripts/bullet_cluster_stellar_mass_sed.py

---

 ## Data

All raw results are contained in [`data/1486combined_lens_stellar_mass_all_2025Jul.csv`](data/1486combined_lens_stellar_mass_all_2025Jul.csv), which includes:

* Lens ID, RA, DEC, redshift
* All nearby SIMBAD stellar mass tracers
* Surface density calculations (per arcmin²)

The random sky control sample data is in [`data/stellar_density_random_fields.csv`](data/stellar_density_random_fields.csv).
 
Plots: Random field versus lenses stellar mass dentsity commparisons including box plots, Kernel Density, and overlap historgram are also avaialble in the`results/` directory.

---



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- Thanks to the teams behind [Astroquery](https://astroquery.readthedocs.io/), [Lenscat](https://github.com/username/lenscat), [SIMBAD](http://simbad.u-strasbg.fr/simbad/), and other open-source tools used in this analysis.

- Based on data from the Sloan Digital Sky Survey (SDSS) and WISE.
-Code and manuscript were prepared with the assistance of a large language model.

---


---

## Citation

If you use this code or results, please cite this GitHub repository 

---

## License

This repository is licensed under the [MIT License](LICENSE).

##  Contact

For questions or collaborations, please contact [Michael Feldstien](mailto:mjay10016@gmail.com).


