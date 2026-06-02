# IISE ReEDS Morris Sensitivity Analysis

## Project Overview

This project applies **Morris Method global sensitivity analysis** to the **ReEDS (Regional Energy Deployment System)** energy system optimization model to identify which input parameters most influence curtailment outcomes. It is the companion code to the IISE published paper included in this repository.

The Morris Method is a computationally efficient screening technique that estimates each parameter's overall influence (μ\*) and nonlinearity/interaction effects (σ) by evaluating elementary effects across the input space — without requiring a full factorial design.

**Analysis pipeline:**

```
1. Define Parameter Ranges          (notebooks/01_define_ranges/)
   ├── Technology costs  ← ATB 2024 (NREL GitHub)
   ├── Fuel prices       ← AEO 2025 natural gas data
   └── Demand            ← Historic & EER baseline hourly load

2. Morris Sampling                  (notebooks/02_sampling/)
   └── Generate R=5 trajectories × (k+1) runs using SALib

3. Run ReEDS                        (external — GAMS/ReEDS)
   └── Produces curtailment CSVs    (data/outputs/curt_ann_Sc_Run{N}.csv)

4. Morris Screening & Analysis      (notebooks/03_screening/)
   └── Compute μ*, σ, rank parameters by importance
```

## Directory Structure

```
IISE_ReEDS_Morris/
│
├── data/
│   ├── raw/          # Downloaded source data (gitignored — fetched at runtime).
│   └── outputs/      # ReEDS curtailment CSVs: curt_ann_Sc_Run1..Run26.csv
│
├── notebooks/
│   ├── 01_define_ranges/
│   │   ├── technology_cost/   # ATB 2024 cost bounds per technology
│   │   ├── fuel_price/        # Natural gas AEO 2025 multiplier bounds
│   │   └── demand/            # Historic & EER baseline load bounds
│   ├── 02_sampling/
│   │   └── Morris_Sampling.ipynb       # Generate Morris design matrix
│   ├── 03_screening/
│   │   └── Morris_Screening.ipynb      # Analyse curtailment outputs
│   ├── additional_reeds_inputs/        # Dollar-year conversion & NG prep
│   ├── MorrisToyExample.ipynb          # Self-contained toy demo
│   └── Tutorial.ipynb                  # GSA workshop tutorial
│
├── src/
│   ├── __init__.py
│   └── config.py     # All paths, URLs, and model settings — edit here first.
│
├── visuals/          # Workflow diagrams and exported figures.
│
├── IISE Published paper/
│   └── IISE_ReEDs_Morris_V2.pdf
│
├── requirements.txt
├── .gitignore        # Excludes gamslice.txt, data/raw/, .DS_Store, etc.
└── README.md
```

## Requirements

- **Python** 3.10+
- **GAMS** with a valid licence + GAMS Python API (for running ReEDS itself)
- See `requirements.txt` for all Python dependencies

## How to Run

### Step 0 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 1 — Define parameter ranges

Open each notebook under `notebooks/01_define_ranges/` to inspect and update the lower/upper bounds for technology costs, fuel prices, and demand multipliers. These notebooks pull data directly from the NREL ReEDS GitHub and AEO sources.

### Step 2 — Generate the Morris sample

Open `notebooks/02_sampling/Morris_Sampling.ipynb`. This fetches the bounds CSV from GitHub and generates the Morris design matrix (R trajectories × k+1 runs). The design is saved to `data/outputs/`.

Key settings (edit in `src/config.py`):

| Parameter | Default | Description |
|-----------|---------|-------------|
| `R_TRAJECTORIES` | 5 | Number of Morris trajectories |
| `MORRIS_LEVELS` | 4 | Grid levels per parameter |
| `RANDOM_SEED` | 42 | Reproducibility seed |

### Step 3 — Run ReEDS

Feed the generated scenarios into ReEDS (GAMS). Outputs should be saved as:
```
data/outputs/curt_ann_Sc_Run1.csv
data/outputs/curt_ann_Sc_Run2.csv
...
data/outputs/curt_ann_Sc_Run26.csv
```

### Step 4 — Morris Screening

Open `notebooks/03_screening/Morris_Screening.ipynb` to compute elementary effects (μ\*, σ) and rank parameters by their influence on total curtailment.

### Google Colab

1. Zip and upload the repository to Google Drive.
2. In Colab, mount Drive and unzip:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   !unzip /content/drive/MyDrive/IISE_ReEDS_Morris.zip -d /content/
   ```
3. Install dependencies:
   ```python
   !pip install -r /content/IISE_ReEDS_Morris/requirements.txt
   ```
4. Run notebooks in order (Steps 1 → 4 above).

## Configuration

All paths and settings are in `src/config.py`. Key entries:

| Setting | Value | Description |
|---------|-------|-------------|
| `URL_BOUNDS` | GitHub URL | Morris parameter bounds CSV |
| `R_TRAJECTORIES` | 5 | Morris trajectories |
| `RANDOM_SEED` | 42 | Global reproducibility seed |
| `N_RUNS` | 26 | Number of ReEDS scenario runs |

## Reference

Aghapour, R. et al. *Global sensitivity analysis to enhance the transparency and rigour of energy system optimisation modelling.* IISE Transactions (see `IISE Published paper/` folder).

Saltelli, A. et al. (2008). *Global Sensitivity Analysis: The Primer.* Wiley.

Herman, J. & Usher, W. (2017). SALib: An open-source Python library for sensitivity analysis. *Journal of Open Source Software*, 2(9), 97.
