# Stellar Mass Surface Densities in Strong Gravitational Lenses

## Overview

This repository analyzes stellar mass distributions in 912 strong gravitational lensing systems, revealing significant tension with standard Cold Dark Matter ($\Lambda$CDM) model predictions.

Assuming a typical stellar baryon fraction, most lenses have stellar mass surface densities implying a total mass well above the canonical $\Lambda$CDM strong lensing threshold. This suggests that the stellar component may play a larger role in the lensing mass budget than commonly assumed.


---

## Key Findings
* **High-Density Environments:** Only **4.6%** of the 912 lenses have an inferred total mass density below the $\\Lambda$CDM threshold (assuming a stellar baryon fraction of $f_* = 0.03$).
* **Lenses vs. Random Fields:** The mean stellar mass surface density of the lens sample is **~10 times higher** than that of a random sky sample, indicating that lenses are preferentially located in high-density environments.
* **Bullet Cluster Case Study:** A localized analysis of the Bullet Cluster's core shows a stellar mass density nearly **two orders of magnitude** above the standard $\\Lambda$CDM strong lensing threshold.

---

## Repository Contents
* `notebooks/`: Jupyter notebooks for interactive data exploration and visualization.
* `results/`: Plots comparing inferred mass densities to $\\Lambda$CDM expectations.
* `scripts/`: Python scripts to reproduce the full analysis from data acquisition to final figures.
* `data/`: Raw data and control samples, including `1486combined_lens_stellar_mass_all_2025Jul.csv` and `stellar_density_random_fields.csv`.

---

## Scripts to Reproduce the Analysis
To reproduce the main analysis and figures, follow these steps:

1.  **Query Stellar Mass Environments:**
    This script uses `lenscat` and `astroquery` to query the SIMBAD database for stellar-like objects within 20 arcminutes of each strong lens.
    ```bash
    python scripts/query_simbad_stellar_mass.py
    ```

2.  **Analyze Stellar Mass Distributions:**
    This script performs statistical comparisons between the lens sample and random sky fields, generating plots like `Box_plots.png`, `Kernel_Density.png`, and `Overlaid_historgram_radom_versus_lens.png`.
    ```bash
    python scripts/analyze_stellar_mass.py
    ```

3.  **Perform CDM Threshold Analysis:**
    This script compares estimated stellar surface densities to $\\Lambda$CDM expectations based on a fiducial stellar baryon fraction.
    ```bash
    python scripts/stellar_mass_cdm_threshold_analysis.py
    ```

### Bullet Cluster Case Study Scripts
These scripts provide independent methods to estimate the stellar mass surface density in the Bullet Cluster field:

* **WISE W1-band Estimation:** Estimates stellar mass from WISE W1-band infrared flux measurements.
    ```bash
    python scripts/bullet_cluster_stellar_mass.py
    ```
* **Einstein Radius Approximation:** Estimates lensing mass from a circular Einstein radius approximation.
    ```bash
    python scripts/einstein_radius_stellar_density.py
    ```
* **SED-based Stellar Mass:** Retrieves and integrates catalog-based SED stellar masses.
    ```bash
    python scripts/bullet_cluster_stellar_mass_sed.py
    ```

---

## Citation & License
If you use this code or results, please cite this GitHub repository and the forthcoming publication:

**"Observed Stellar Mass Environments Around Gravitational Lenses Challenge CDM Threshold Predictions"**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements
Thanks to the teams behind [Astroquery](https://astroquery.readthedocs.io/), [Lenscat](https://github.com/username/lenscat), [SIMBAD](http://simbad.u-strasbg.fr/simbad/), and the Sloan Digital Sky Survey (SDSS). 
The code and manuscript were prepared with the assistance of a large language model.

---

## Contact
For questions or collaborations, please contact [Michael Feldstien](mailto:mjay10016@gmail.com).
