# Stellar Mass Surface Densities in Strong Gravitational Lenses 

## Overview

This repository analyzes stellar mass distributions in 912 strong gravitational lensing systems, revealing significant tension with standard Cold Dark Matter (ΛCDM) model predictions.

Assuming a typical stellar baryon fraction = 0.03, most lenses have stellar mass surface densities implying total masses well above the canonical ΛCDM strong lensing threshold of 1 × 10⁸ M⊙/kpc². Even with conservative reductions in stellar mass, these lenses exceed the expected limits, suggesting stellar baryons may play a larger role in lensing mass budgets than commonly assumed.

A detailed case study of the Bullet Cluster (1E 0657–56) reinforces this, with its core stellar mass density nearly two orders of magnitude above the standard threshold.

---

### Running the Analysis

To reproduce the main analysis and figures:

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

## 2. Methods

We developed a pipeline to estimate the total stellar mass in the environment surrounding strong gravitational lenses using Sloan Digital Sky Survey (SDSS) photometric data accessed via `Astroquery`, and compare these to theoretical CDM strong lensing thresholds.

### 2.1. Sample and Data Acquisition

Our analysis utilizes a sample of 912 strong lens systems [ref 1] from a publicly available strong lens catalog imported via the `lenscat` Python package, which provides lens coordinates (RA, DEC), lens redshifts, and identifiers.

### 2.2. Environmental Stellar Mass Estimation Pipeline

For each lens with a valid redshift, we query the SDSS photometric catalog to retrieve sources within a 20 arcminute radius of the lens position, tiling the search region with overlapping circular tiles for efficiency.

* **Stellar Mass Assignment:** Objects classified as galaxies (SDSS type code 6) are assigned a nominal stellar mass of $5 \times 10^{10} \; M_\odot$, representing a typical stellar mass for SDSS galaxies. Non-galaxy objects are assigned zero mass. Total stellar mass within the 20' aperture is computed by summing these galaxy masses.
* **Surface Mass Density Calculation:** Using the lens redshift and Planck 2018 cosmological parameters, the angular aperture radius (20 arcminutes) is converted into a physical radius in megaparsecs (Mpc). The physical area is then computed, enabling conversion of the total stellar mass into a projected stellar surface mass density ($\Sigma_*$) with units $M_\odot/\text{Mpc}^2$, subsequently converted to $M_\odot/\text{kpc}^2$ by dividing by $10^6$.
* **Density Classification and Tracking:** Based on $\Sigma_*$, lens environments are classified into low, medium, and high stellar mass surface density bins using predefined thresholds. Lenses with no detected galaxies or zero/undefined stellar surface densities were excluded from further analysis. Results are saved incrementally, allowing session resumption.

### 2.3. Stellar Mass Fraction and CDM Threshold Comparison

To evaluate consistency with Cold Dark Matter (CDM) halo models, we calculated the stellar mass fraction $f_* = M_* / M_{\text{lens}}$. Assuming a range of stellar baryon fractions $f_*=0.01−0.20$, we infer total projected mass densities by dividing the stellar surface mass density by the stellar baryon fraction:

$$
\Sigma_{\text{total}} = \Sigma_* / f_*
$$

These inferred total densities are then compared to the canonical CDM strong lensing threshold of $\Sigma_{\text{threshold}} = 1 \times 10^8 \; M_\odot / \text{kpc}^2$.



## Key Findings

### 1. Prevalence of High-Density Lenses

Only 4.6% of the 912 strong lenses studied have an inferred total mass density below the ΛCDM threshold of 1 × 10⁸ M⊙/kpc², assuming a stellar baryon fraction of f★ = 0.03.

| f★   | Lenses Below CDM Threshold | Total Lenses | Percentage Below Threshold (%) |
|------|----------------------------|--------------|--------------------------------|
| 0.01 | 6                          | 912          | 0.7                            |
| 0.03 | 42                         | 912          | 4.6                            |
| 0.05 | 180                        | 912          | 19.7                           |
| 0.06 | 282                        | 912          | 30.9                           |
| 0.07 | 414                        | 912          | 45.4                           |
| 0.08 | 468                        | 912          | 51.3                           |
| 0.09 | 501                        | 912          | 54.9                           |
| 0.10 | 561                        | 912          | 61.5                           |
| 0.20 | 738                        | 912          | 80.9                           |

These results suggest that the stellar component accounts for a significantly larger fraction of the lensing mass than predicted by ΛCDM in most systems. This deviation may indicate systematic environmental differences in strong lenses or a breakdown of standard dark matter assumptions.

**Figure 1: Sensitivity to Assumed Stellar Mass**

![Consistency plot](results/consistency_plot.png)


---

### 2. Lenses vs. Random Fields

The stellar mass surface density of the strong lens sample is significantly higher and more widely distributed than that of a random sky sample.

| Statistic             | Lens Sample Value (M⊙/kpc²) | Random Sample Value (M⊙/kpc²) |
|-----------------------|-----------------------------|--------------------------------|
| Mean Σ★               | 9.97 × 10⁶                  | 1.03 × 10⁶                     |
| Median Σ★             | 4.79 × 10⁶                  | 8.60 × 10⁵                     |
| Standard Deviation Σ★ | 3.26 × 10⁷                  | 9.76 × 10⁴                     |

Number of samples: 912 for both lenses and random sky points.

The mean stellar mass surface density of the lens sample is about 9.68 times higher than that of the random sky sample. This nearly order-of-magnitude difference underscores that strong gravitational lenses are preferentially located in regions with much higher stellar mass concentration than typical sky fields.

---

### 3. Bullet Cluster Study


To complement the statistical trends, we performed a direct analysis of the Bullet Cluster (1E 0657–558) using WISE W1-band photometry. Localized Stellar Mass and Surface Density Estimation

We conducted a focused search for galaxies within a 0.5 arcminute radius around the Bullet Cluster center (RA = 104.6458°, DEC = -55.6748°), isolating the region responsible for strong lensing and minimizing contamination. Using the SIMBAD database, a single dominant galaxy was identified.

Stellar mass estimation proceeded as follows:
* **Luminosity Distance:** Using the galaxy redshift $z = 0.296$, luminosity distance was computed with Planck18 cosmology.
* **Absolute Magnitude & Luminosity:** Converted from WISE W1 apparent magnitude ($\sim$16.685) to absolute magnitude ($M_{W1}$) and then to luminosity in solar units ($L_{W1}$), using the Sun’s absolute W1 magnitude $M_{\odot,W1} \approx 3.24$.
* **Stellar Mass:** Applying a mass-to-light ratio $(M/L)_{W1} = 0.6 \, M_{\odot} / L_{\odot}$, typical for old stellar populations, yielded a stellar mass estimate of approximately $6.3 \times 10^{10} \, M_{\odot}$ for the localized galaxy.

Alternatively, using the WISE W1 magnitude within the same 0.5′ aperture and an assumed Einstein radius $R_E = 5\, \mathrm{kpc}$, we derived a stellar surface mass density:

$$
\Sigma_* = \frac{M_*}{\pi R_E^2} \approx 4.9 \times 10^{8} \, M_{\odot}/\mathrm{kpc}^2
$$

Assuming a typical cosmic baryon fraction $f_* = 0.05$, the implied total mass surface density is:

$$
\Sigma_{\mathrm{total}} = \frac{\Sigma_*}{f_*} \approx 9.8 \times 10^{9} \, M_{\odot}/\mathrm{kpc}^2,
$$

which significantly exceeds the canonical CDM strong lensing threshold of $1 \times 10^{8} \, M_{\odot}/\mathrm{kpc}^2$. This case study illustrates that the Bullet Cluster's strong lensing region contains substantial stellar mass, sufficient to account for the observed lensing effects without invoking large dark matter halos.
The Bullet Cluster (1E 0657–56) shows a core stellar mass surface density implying a total mass density nearly two orders of magnitude above the standard ΛCDM strong lensing threshold.


| Quantity                           | Value                                         | Notes                                    |
|------------------------------------|-----------------------------------------------|------------------------------------------|
| Redshift (z)                       | 0.296                                         | Bullet Cluster system                    |
| Radius                              | 0.5′                                          | Circular aperture centered on core       |
| Central Galaxy Coordinates          | RA: 104.6458°, Dec: –55.6748°                 | Dominant lensing galaxy                  |
| WISE W1 Luminosity                  | 1.05 × 10¹¹ L⊙                                | From 3.4 µm flux                         |
| M/L Ratio (W1)                      | 0.6 M⊙/L⊙                                    | Standard for old stellar populations     |
| Refined Stellar Mass                | 6.3 × 10¹⁰ M⊙                                 | From WISE W1 and M/L = 0.6                |
| Assumed Einstein Radius             | 5 kpc                                         | Typical lensing scale                    |
| Stellar Surface Density (Σ★)        | 8.0 × 10⁸ M⊙/kpc²                             | Within aperture                          |
| SED-Based Total Stellar Mass        | ~3.0 × 10¹¹ M⊙                                | From public catalogs (SED fitting)       |
| Total Σ★ Over Full Extent           | 2.06 × 10⁹ M⊙/kpc²                            | Using total mass and effective radius    |
| Implied Total Mass Surface Density  | 1.6 × 10¹⁰ M⊙/kpc²                            | From Σ★ and f★ = 0.05                    |
| CDM Halo Threshold                  | ~10⁸ M⊙/kpc²                                  | Canonical value (Donato et al. 2009)     |


This localized measurement aligns with and strengthens the broader survey results, suggesting that in some massive clusters, stellar mass alone may be sufficient to explain lensing, posing a challenge to standard dark matter interpretations.

## Discussion

These findings suggest that either dark matter halos in lens systems are systematically more massive or concentrated than predicted, or that additional factors—such as environmental contributions, external shear, or alternative physics—play a critical role in producing observed strong lensing. Our work thus challenges standard assumptions about lens environments within the CDM paradigm.

This project began as an attempt to identify gravitational lenses in low-density environments, initially focusing on gas mass. When reliable gas data proved difficult to obtain, we pivoted to stellar mass surface density as a practical tracer. Surprisingly, this simple approach revealed that a significant fraction of known strong lenses lie in regions where stellar mass alone may account for the observed lensing, raising new questions about the necessity of dark matter in these systems.

Our findings revealed something unexpected: a significant fraction of strong lenses reside in environments with relatively high stellar mass, and yet CDM models—when calibrated to reasonable baryon fractions—often overpredict the total lensing mass. In these cases, the dark matter contribution inferred by CDM exceeds what is needed to explain the observed lensing, given the high stellar mass already present. This leads to a clear tension: if the halos are as massive as CDM predicts, the light bending should be stronger than observed.

In other words, many lenses appear to require weaker or less massive halos than CDM would assign based on their stellar content. This suggests that:

- CDM may overestimate halo mass or concentration in such fields, or

- An alternative explanation (e.g., geometric effects from compact objects like black holes) may account for the lensing without invoking large unseen mass.

These results challenge a key assumption of the CDM framework—that dark matter halos dominate lensing mass—and indicate that high stellar mass alone can often explain observed lensing, even in the absence of strong dark matter halos.

This opens a path for new models of cosmic structure that do not rely on massive halos, and it strengthens the case for considering geometric or non-halo-based mechanisms behind gravitational lensing.

---

## 5. Conclusions

The presence of strong gravitational lenses in low-density stellar environments underscores the need to revisit dark matter halo modeling and environmental effects in lensing studies. Future work with larger samples and detailed environment characterization will further elucidate the interplay between baryons and dark matter in shaping strong lensing phenomena.

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

## Citation

If you use this work, please cite the associated preprint (to be added after arXiv upload).

---
## Acknowledgements

- Thanks to the teams behind [Astroquery](https://astroquery.readthedocs.io/), [Lenscat](https://github.com/username/lenscat), [SIMBAD](http://simbad.u-strasbg.fr/simbad/), and other open-source tools used in this analysis.

- Based on data from the Sloan Digital Sky Survey (SDSS) and WISE.
-Code and manuscript were prepared with the assistance of a large language model.
---

##  Contact

For questions or collaborations, please contact [Your Name](mailto:your.email@example.com).

---

## Next Steps

- Add spectroscopic stellar mass measurements.

- Incorporate gas mass and environmental contributions.

- Compare with hydrodynamical simulations.

- Extend analysis to larger lens samples.






## Repository Contents

- `data/`: Lens data and random field control samples
- `scripts/`: Python code for querying, filtering, and analyzing galaxy environments
- `figures/`: Plots comparing inferred mass densities to ΛCDM expectations
- `notebooks/`: (Optional) Jupyter notebooks for interactive analysis

---

## References

1. Planck Collaboration et al., 2018, *Planck 2018 results. VI. Cosmological parameters*, [arXiv:1807.06209](https://arxiv.org/abs/1807.06209)

2. SDSS Collaboration, York et al., 2000, *The Sloan Digital Sky Survey: Technical Summary*, AJ, 120, 1579, [SDSS website](https://www.sdss.org/)

3. Wright, E. L., 2006, *A Cosmology Calculator for the World Wide Web*, PASP, 118, 1711, [arXiv:astro-ph/0609593](https://arxiv.org/abs/astro-ph/0609593)

4. Cutri et al., 2012, *WISE All-Sky Data Release*, [WISE data archive](https://wise2.ipac.caltech.edu/docs/release/allsky/)

5. Wenger et al., 2000, *The SIMBAD astronomical database*, A&AS, 143, 9, [SIMBAD](http://simbad.u-strasbg.fr/simbad/)

---

## 📖 Citation

If you use this code or results, please cite this GitHub repository and/or the forthcoming publication:

**"Observed Stellar Mass Environments Around Gravitational Lenses Challenge CDM Threshold Predictions"**

---

## 🧩 License

This repository is licensed under the [MIT License](LICENSE).

