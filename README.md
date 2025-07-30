# stellar-mass-vs-cdm
This repo analyzes stellar mass near strong gravitational lenses versus Cold Dark Matter (CDM) predictions. It includes data, scripts, and results showing how observed stellar surface densities consistently challenge CDM thresholds across growing lens samples, highlighting potential gaps in dark matter models.
# Evidence for Strong Gravitational Lenses in Low-Density Stellar Environments Challenges Standard Cold Dark Matter Models

## Abstract

We present an analysis of stellar surface mass densities surrounding a large sample of strong gravitational lenses to test predictions of standard cold dark matter (CDM) models regarding lens environments. By comparing observed stellar mass densities to the theoretical total mass density thresholds required for strong lensing—accounting for a range of plausible stellar baryon fractions—we find that a significant fraction of lenses inhabit environments with inferred total mass densities below the canonical CDM strong lensing threshold of

$$
\Sigma_{\mathrm{threshold}} = 1 \times 10^{8} \; M_\odot / \mathrm{kpc}^2
$$

This discrepancy persists even under conservative assumptions of low stellar mass fractions, implying that dark matter halos alone may be insufficient to fully explain the observed lensing in these systems. Our results indicate that lenses frequently reside in lower-density neighborhoods than CDM models typically assume, suggesting the need for either more massive or concentrated dark matter halos, additional environmental contributions, or novel physical mechanisms. This study provides new observational constraints on lens environments and invites reconsideration of dark matter halo properties in strong lensing models.

---

## Introduction

Strong gravitational lensing serves as a powerful probe of galaxy mass distributions, including the elusive dark matter component. Standard $\Lambda$CDM cosmology predicts that strong lenses predominantly reside in massive, dense dark matter halos, with total projected mass densities exceeding approximately

$$
10^{8} \; M_\odot / \mathrm{kpc}^2.
$$

However, stellar mass—measured via surface mass density—comprises only a fraction of the total mass, and the baryon fraction can vary substantially.

---

## Methods

We analyze a sample of 202 strong lens systems with measured stellar surface mass densities averaged within 20 arcminute radii around each lens. Assuming a range of stellar baryon fractions

$$
f_* = 0.01 - 0.20,
$$

we infer total projected mass densities via

$$
\Sigma_{\mathrm{total}} = \frac{\Sigma_*}{f_*}
$$

and compare these to the CDM strong lensing threshold.

---

### Query and Environmental Stellar Mass Estimation

We developed a pipeline to estimate the total stellar mass in the environment surrounding strong gravitational lenses using Sloan Digital Sky Survey (SDSS) photometric data accessed via Astroquery. The process consists of the following steps:

- **Lens Catalog Input:** Starting from a publicly available strong lens catalog imported via the `lenscat` Python package, which provides lens coordinates (RA, DEC), lens redshifts, and identifiers.

- **SDSS Environmental Query:** For each lens with a valid redshift, we query the SDSS photometric catalog to retrieve sources within a 20 arcminute radius of the lens position. To cover this area efficiently, we tile the search region using overlapping circular tiles of 3 arcminute radius. Each tile is queried independently, and results are combined.

- **Stellar Mass Assignment:** Objects classified as galaxies (SDSS type code 6) are assigned a nominal stellar mass of

$$
5 \times 10^{10} \; M_\odot,
$$

  representing a typical stellar mass for SDSS galaxies. Non-galaxy objects are assigned zero mass. Total stellar mass within the 20' aperture is computed by summing these galaxy masses.

- **Surface Mass Density Calculation:** Using the lens redshift and Planck 2018 cosmological parameters, the angular diameter distance is calculated to convert the angular aperture radius (20 arcminutes) into a physical radius in megaparsecs (Mpc). The physical area of the aperture is then computed, enabling conversion of the total stellar mass into a projected surface mass density $\Sigma_*$ with units $M_\odot/\mathrm{Mpc}^2$.

- **Density Classification and Tracking:** Based on $\Sigma_*$, lens environments are classified into low, medium, and high stellar mass surface density bins using predefined thresholds for descriptive statistics. Lenses with no detected galaxies in the aperture are tracked separately.

- **Data Saving and Progress Reporting:** Results for each lens are saved incrementally to Google Drive as CSV files, allowing session resumption and partial data analysis. Summary statistics of lenses per density bin are reported periodically.

This approach yields an approximate measure of the stellar mass environment around lenses and provides a basis for comparing observed densities with theoretical expectations from cold dark matter models.

---
### Stellar Mass Fraction and CDM Thresholds

To evaluate whether the lensing systems in our sample are consistent with expectations from Cold Dark Matter (CDM) halo models, we calculated the stellar mass fraction

$$
f_* = \frac{M_*}{M_{\mathrm{lens}}}
$$

for 146 strong gravitational lenses. CDM-based simulations typically predict low stellar mass fractions for galaxy-scale lenses, with

$$
f_* \lesssim 0.03
$$

being common. However, our analysis shows that only 3.4% of lenses fall below this threshold. Moreover, only 18.5% of lenses have $f_* < 0.05$, while a majority — 61.6% — have $f_* < 0.10$, and 81.5% fall below 0.20. These results suggest that the stellar component accounts for a significantly larger portion of the lensing mass than predicted by CDM in the majority of systems analyzed. This deviation points either to a systematic environmental difference in strong lenses or to a breakdown of dark matter assumptions, potentially supporting alternative models such as geometry-based mass contributions or curvature-driven lensing without dark matter.

---
## Summary Table of Lenses Below CDM Threshold vs. Stellar Mass Fraction

| $f_*$ | Lenses Below CDM Threshold | Total Lenses | Percentage Below Threshold (%) |
|-------|----------------------------|--------------|-------------------------------|
| 0.01  | 6                          | 912          | 0.7                           |
| 0.03  | 42                         | 912          | 4.6                           |
| 0.05  | 180                        | 912          | 19.7                          |
| 0.06  | 282                        | 912          | 30.9                          |
| 0.07  | 414                        | 912          | 45.4                          |
| 0.08  | 468                        | 912          | 51.3                          |
| 0.09  | 501                        | 912          | 54.9                          |
| 0.10  | 561                        | 912          | 61.5                          |
| 0.20  | 738                        | 912          | 80.9                          |



---
## Interpretation 

The table above shows the number and fraction of strong lenses that fall below various stellar mass fraction ($f_*$) thresholds, compared to expectations from standard Cold Dark Matter (CDM) models. Notably, only a small percentage of lenses (around 4.6%) have stellar mass fractions below the commonly predicted CDM threshold of $f_* \lesssim 0.03$, which implies that the majority of lenses possess a larger fraction of their total mass in stars than CDM simulations typically predict.


## Bullet Cluster Case Study: Stellar Mass Estimation

To complement the statistical trends across the large strong lens sample, we performed a direct analysis of the Bullet Cluster (1E 0657–558) using WISE W1-band photometry.

### Localized Stellar Mass Estimation

We conducted a focused search for galaxies within a 0.5 arcminute radius around the Bullet Cluster center (RA = 104.6458°, DEC = -55.6748°), isolating the region responsible for strong lensing and minimizing contamination from distant cluster members or foreground/background sources. Using the SIMBAD database via `astroquery.simbad`, a single galaxy was identified within this aperture, likely the dominant stellar mass contributor.

The galaxy's WISE W1 apparent magnitude (~3.4 µm) was found to be approximately 16.685, a robust tracer of stellar mass due to minimal dust extinction.

Stellar mass estimation proceeded as follows:

- **Luminosity Distance:** Using the galaxy redshift $z = 0.296$ (consistent with the Bullet Cluster), the luminosity distance was computed with the Planck18 cosmology.

- **Absolute Magnitude:** Converted from apparent magnitude using

$$
M_{W1} = m_{W1} - 5 \times \log_{10} \left( \frac{d_L}{10\, \mathrm{pc}} \right)
$$

- **Luminosity in Solar Units:** Using the Sun’s absolute W1 magnitude $M_{\odot,W1} \approx 3.24$,

$$
L_{W1} = 10^{-0.4 (M_{W1} - M_{\odot,W1})}
$$

- **Stellar Mass:** Applying a mass-to-light ratio $(M/L)_{W1} = 0.6 \, M_{\odot}/L_{\odot}$ typical for old stellar populations,

$$
M_* = (M/L)_{W1} \times L_{W1}
$$

This yields a stellar mass estimate of approximately $6.3 \times 10^{10} \, M_{\odot}$ for the localized galaxy.

### Surface Density and Comparison

Alternatively, using the WISE W1 magnitude within the same 0.5′ aperture and an assumed Einstein radius $R_E = 5\, \mathrm{kpc}$, we derived a stellar surface mass density:

$$
\Sigma_* = \frac{M_*}{\pi R_E^2} \approx 4.9 \times 10^{8} \, M_{\odot}/\mathrm{kpc}^2
$$

Assuming a typical cosmic baryon fraction $f_* = 0.05$, the implied total mass surface density is

$$
\Sigma_{\mathrm{total}} = \frac{\Sigma_*}{f_*} \approx 9.8 \times 10^{9} \, M_{\odot}/\mathrm{kpc}^2,
$$

which exceeds the canonical CDM strong lensing threshold of $1 \times 10^{8} \, M_{\odot}/\mathrm{kpc}^2$.

This case study illustrates that the Bullet Cluster's strong lensing region contains substantial stellar mass, sufficient to account for the observed lensing effects without invoking large dark matter halos.

This localized measurement supports and refines our broader survey results, indicating that stellar mass alone may explain lensing in some massive clusters, challenging standard dark matter interpretations.

## Bullet Cluster Stellar Mass Estimation Methods

| Method                      | Stellar Mass (M☉)       | Stellar Surface Density (M☉/kpc²) | Notes                                   |
|-----------------------------|-------------------------|----------------------------------|-----------------------------------------|
| 1. WISE W1 Band Photometry  | 3.9 × 10¹⁰              | 4.91 × 10⁸                       | Localized aperture (0.5 arcmin) estimate|
| 2. Einstein Radius Approx.  | 3.9 × 10¹⁰              | 4.91 × 10⁸                       | Based on assumed 5 kpc Einstein radius  |
| 3. Catalog SED Fitting (Sim.)| 3.0 × 10¹¹             | 2.06 × 10⁹                       | Total stellar mass from SED catalog     |

---



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

All raw results are contained in [`results/1486combined_lens_stellar_mass_all_2025Jul.csv`](results/1486combined_lens_stellar_mass_all_2025Jul.csv)
, which includes:
- Lens ID, RA, DEC, redshift
- All nearby SIMBAD stellar mass tracers
- Surface density calculations (per arcmin²)
---

## Appendix: Baryon Fraction and Its Impact on Strong Lensing Mass Estimates

The baryon fraction $f_*$, defined as the ratio of stellar mass to total mass

$$
f_* = \frac{M_*}{M_{\mathrm{total}}},
$$

plays a crucial role in interpreting strong lensing observations. A very low $f_*$ (e.g., 1%) implies that stars constitute only a tiny fraction of the total mass, with the majority comprised of gas and dark matter. In this case, the total mass inferred from the measured stellar surface density is significantly amplified, making it easier for standard Cold Dark Matter (CDM) models to account for the observed lensing signals. Conversely, higher baryon fractions (5–10%), which are more typical of massive elliptical galaxies, suggest stars contribute a more substantial portion of the total mass. This reduces the inferred total mass for a given stellar surface density, leading to a large fraction of lenses falling below the CDM-predicted minimum mass threshold necessary for strong lensing.

Our analysis reveals that, assuming realistic baryon fractions, a significant number of lenses with low stellar surface densities have total masses too low to be explained by CDM alone, highlighting a tension that may indicate the need for additional mass components or alternative physical mechanisms.

---

## Notes on Methods and Data

- The stellar surface mass density values, originally provided in $M_\odot / \mathrm{Mpc}^2$, were converted to $M_\odot / \mathrm{kpc}^2$ by dividing by $10^6$.

- Lenses with zero or undefined stellar surface densities were excluded from further analysis.

- Redshift filtering was applied implicitly by excluding entries with missing or zero redshift values, ensuring all lenses analyzed have meaningful distance information.

- The CDM strong lensing threshold

  $$
  \Sigma_{\mathrm{threshold}} = 1 \times 10^{8} \; M_\odot / \mathrm{kpc}^2
  $$

  is based on theoretical and simulation-based studies and represents the minimal projected surface mass density required for strong lensing within typical Einstein radii.

---

## Future Work

Further work will involve:

- Incorporating spectroscopic stellar mass measurements.

- Including gas mass contributions.

- Detailed lensing mass modeling to improve accuracy.

- Extending the analysis to larger lens samples.

- Comparing observational data with hydrodynamical simulations to understand low-density lens environments.

---
## Code Overview: Stellar Mass vs. CDM Analysis

This repository analyzes the stellar mass surface density near strong gravitational lenses and compares it to expectations from Cold Dark Matter (CDM) halo models. The analysis includes data collection, mass estimation, and threshold comparison scripts.

---

### `scripts/query_simbad_stellar_mass.py`

This script uses the `lenscat` catalog and `astroquery` to query the SIMBAD database for all stellar-like objects within 20 arcminutes of each lens. Each object is assigned a nominal stellar mass based on object type (e.g., star, galaxy, AGN), and a projected stellar mass surface density is computed for each lens field.

The script outputs per-batch results as `.csv` files in the `results/` folder and prints progress updates during execution.

**Usage:**

```bash
python scripts/query_simbad_stellar_mass.py
```

➡️ [View full script](./scripts/query_simbad_stellar_mass.py)

---

### `scripts/stellar_mass_cdm_threshold_analysis.py`

This script compares the estimated stellar surface densities from the SIMBAD queries to CDM expectations based on a fiducial stellar baryon fraction (e.g. `f_star = 0.05`). It computes CDM-predicted thresholds and determines what fraction of observed lens environments fall below them — potentially indicating CDM failure in low-density fields.

The output includes percentile tables and threshold comparison plots.

**Usage:**

```bash
python scripts/stellar_mass_cdm_threshold_analysis.py
```

➡️ [View full script](./scripts/stellar_mass_cdm_threshold_analysis.py)

---

###  Requirements

To run these scripts, install the following Python packages:

```bash
pip install numpy pandas astropy astroquery matplotlib lenscat
```
## 🛰 Bullet Cluster Case Study Scripts

These scripts provide **three independent methods** to estimate the stellar mass surface density in the Bullet Cluster field, testing whether observed stellar content is sufficient to account for lensing without invoking CDM halos.

---

### `scripts/bullet_cluster_stellar_mass.py

Uses **WISE W1-band infrared flux measurements** (within a 0.5′ aperture) to estimate stellar mass via luminosity-to-mass conversions.

**Usage:**

```bash
python scripts/bullet_cluster_stellar_mass.py
```
➡️ [View full script](scripts/bullet_cluster_stellar_mass.py)


---

### `scripts/einstein_radius_stellar_density.py

Estimates lensing mass from a circular Einstein radius approximation (~5 kpc), converting the angular radius to enclosed mass using standard lensing equations.

**Usage:**

```bash
python scripts/einstein_radius_stellar_density.py
```
➡️ [View full script](scripts/einstein_radius_stellar_density.py)


---

### `scripts/bullet_cluster_stellar_mass_sed.py`

Retrieves and integrates catalog-based SED stellar masses from SIMBAD/VizieR for galaxies in the Bullet Cluster region to derive a total projected stellar mass.

**Usage:**

```bash
python scripts/bullet_cluster_stellar_mass_sed.py
```
➡️ [View full script](scripts/bullet_cluster_stellar_mass_sed.py)


---

### 🧩 Requirements

Install all required packages:

```bash
pip install numpy pandas astropy astroquery matplotlib lenscat photutils
```

---

---

## 📚 References

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

---

## 🤝 Acknowledgements

- Thanks to the teams behind [Astroquery](https://astroquery.readthedocs.io/), [Lenscat](https://github.com/username/lenscat), [SIMBAD](http://simbad.u-strasbg.fr/simbad/), and other open-source tools used in this analysis.

- Based on data from the Sloan Digital Sky Survey (SDSS) and WISE.

---

## 📞 Contact

For questions or collaborations, please contact [Your Name](mailto:your.email@example.com).

---

## 🚀 Next Steps

- Add spectroscopic stellar mass measurements.

- Incorporate gas mass and environmental contributions.

- Compare with hydrodynamical simulations.

- Extend analysis to larger lens samples.

---





