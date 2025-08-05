# [Your Paper Title] - Stellar Mass Surface Density Analysis

## Project Overview

This repository contains the code and data supporting the analysis presented in the paper "[Your Paper Title]". The project investigates the differences in stellar mass surface density distributions between a sample of lens galaxies and a control sample of random sky galaxies.

## Contents

* `data/`: Contains the input data files (`lens_data.csv`, `random_data.csv`).
* `scripts/`: Python scripts for data loading, statistical analysis, and visualization.
    * `analyze_stellar_mass.py`: Performs the Kolmogorov-Smirnov (K-S) test, Mann-Whitney U test, and generates comparative plots (histograms, KDEs, and box plots).
* `figures/`: Output directory for generated plots.
* `requirements.txt`: Lists the Python dependencies required to run the scripts.
* `LICENSE`: Specifies the licensing for the code.

## Installation

To run the analysis, you'll need Python [e.g., 3.8+] installed.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)[YourGitHubUsername]/[your-repo-name].git
    cd [your-repo-name]
    ```
2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    # .\venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

After setting up the environment and installing dependencies:

1.  **Place your data files** (`lens_data.csv` and `random_data.csv`) into the `data/` directory. Ensure they contain a column named `stellar_mass_density` (or whatever your column is called).
2.  **Run the analysis script:**
    ```bash
    python scripts/analyze_stellar_mass.py
    ```
    This script will:
    * Load the data.
    * Perform the K-S and Mann-Whitney U tests, printing the results to the console.
    * Generate and save the comparative plots (histograms, KDEs, and box plots) into the `figures/` directory.

## Data

* `lens_data.csv`: Contains stellar mass surface density measurements for the lens galaxy sample.
* `random_data.csv`: Contains stellar mass surface density measurements for the random sky galaxy control sample.

Both files are expected to be CSV format with a column named `stellar_mass_density`.

## Results

The script will output the p-values from the K-S and Mann-Whitney U tests, which will indicate the statistical significance of the differences between the two distributions. Visualizations will be saved in the `figures/` directory, illustrating these differences.

## License

This project is licensed under the [e.g., MIT License] - see the `LICENSE` file for details.

## Contact

For any questions or issues, please open an issue on GitHub or contact [Your Name/Email].
