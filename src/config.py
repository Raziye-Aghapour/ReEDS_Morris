"""
config.py
Central configuration for all paths, constants, and settings.

Import this module in any notebook instead of hardcoding paths or URLs.
Compatible with both local execution and Google Colab.
"""

from pathlib import Path
import os

# ── Environment Detection ─────────────────────────────────────────────────────
try:
    import google.colab  # noqa: F401
    COLAB_MODE = True
except ImportError:
    COLAB_MODE = False

# ── Root Paths ────────────────────────────────────────────────────────────────
if COLAB_MODE:
    ROOT_DIR = Path("/content/IISE_ReEDS_Morris")
else:
    ROOT_DIR = Path(__file__).parent.parent  # one level up from src/

DATA_RAW_DIR     = ROOT_DIR / "data" / "raw"
DATA_OUT_DIR     = ROOT_DIR / "data" / "outputs"
NOTEBOOKS_DIR    = ROOT_DIR / "notebooks"
VISUALS_DIR      = ROOT_DIR / "visuals"
SRC_DIR          = ROOT_DIR / "src"

# ── Output CSV Files (ReEDS curtailment runs) ─────────────────────────────────
# Pattern: data/outputs/curt_ann_Sc_Run{N}.csv
def curtailment_csv(run_number: int) -> Path:
    """Return the path for a specific ReEDS curtailment run CSV."""
    return DATA_OUT_DIR / f"curt_ann_Sc_Run{run_number}.csv"

# ── Remote Data Sources (GitHub raw URLs) ─────────────────────────────────────
REEDS_GITHUB_BASE = "https://raw.githubusercontent.com/NREL/ReEDS-2.0/refs/heads/main"
MORRIS_GITHUB_BASE = "https://raw.githubusercontent.com/Raziye-Aghapour/ReEDS_Morris/refs/heads/main"

# Morris bounds file
URL_BOUNDS = f"{MORRIS_GITHUB_BASE}/all_multiplier_bounds.csv"

# ATB 2024 Technology Cost URLs
ATB_BASE = f"{REEDS_GITHUB_BASE}/inputs/plant_characteristics"
URL_ATB = {
    "battery":   {s: f"{ATB_BASE}/battery_ATB_2024_{s}.csv" for s in ["advanced", "moderate", "conservative"]},
    "coal":      {s: f"{ATB_BASE}/coal_ATB_2024_{s}.csv"    for s in ["advanced", "moderate", "conservative"]},
    "gas":       {s: f"{ATB_BASE}/gas-cc_ATB_2024_{s}.csv"  for s in ["advanced", "moderate", "conservative"]},
    "nuclear":   {s: f"{ATB_BASE}/nuclear_ATB_2024_{s}.csv" for s in ["advanced", "moderate", "conservative"]},
    "upv":       {s: f"{ATB_BASE}/upv_ATB_2024_{s}.csv"     for s in ["advanced", "moderate", "conservative"]},
    "ons_wind":  {s: f"{ATB_BASE}/wind-ons_ATB_2024_{s}.csv" for s in ["advanced", "moderate", "conservative"]},
    "ofs_wind":  {s: f"{ATB_BASE}/wind-ofs_ATB_2024_{s}.csv" for s in ["advanced", "moderate", "conservative"]},
}

# ── Morris Sampling Settings ─────────────────────────────────────────────────
RANDOM_SEED  = 42       # Seed for reproducibility
R_TRAJECTORIES = 5      # Number of Morris trajectories
MORRIS_LEVELS  = 4      # Number of levels in Morris grid

# ── ReEDS Run Settings ───────────────────────────────────────────────────────
N_RUNS = 26             # Total number of ReEDS scenario runs (Run1..Run26)

# ── Utility ──────────────────────────────────────────────────────────────────
def ensure_output_dirs():
    """Create output directories if they do not exist."""
    for d in [DATA_RAW_DIR, DATA_OUT_DIR, VISUALS_DIR]:
        d.mkdir(parents=True, exist_ok=True)
