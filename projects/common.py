"""Shared data-loading helpers for the VIM-Polyp example projects.

Every project script imports from here so that:
  * the dataset location is resolved once, via ``src/vimpolyp_paths.py``
    (works on Kaggle, Colab, and a local clone -- see that module);
  * the messy raw column names and the type/subtype spelling variants that the
    exploratory notebooks clean up by hand are normalised in a single place.

Nothing here downloads data. If the required ``.xlsx`` file is missing, the
loaders raise a clear ``FileNotFoundError`` telling you which download script to
run first.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

# Make ``src/vimpolyp_paths.py`` importable no matter where the script is run from.
_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT / "src"))
from vimpolyp_paths import DATA_DIR, OUTPUT_DIR  # noqa: E402  (re-exported for projects)

__all__ = ["DATA_DIR", "OUTPUT_DIR", "load_ihc", "load_patho_metadata", "NUMERIC_MARKERS", "CATEGORICAL_MARKERS"]

# Clean IHC biomarker column names (after the rename applied below).
NUMERIC_MARKERS = ["age", "Ki67", "VEGF", "CD34", "CD34skor", "p53"]
CATEGORICAL_MARKERS = ["gender", "location", "BRAF", "PDL1epith", "PDL1lymph"]

# Raw -> clean column names, matching notebooks/ihc-part.ipynb.
_IHC_RENAME = {
    "Ki-67(clone30-9)": "Ki67",
    "BRAF(cloneV600E)": "BRAF",
    "PD-L1epithelium(clone SP142)": "PDL1epith",
    "PD-L1lymphocyte(clone SP142)": "PDL1lymph",
    "VEGF(clone SP125)": "VEGF",
    "CD34(cloneQBend/10)": "CD34",
    "CD34(cloneQBend/10)skor": "CD34skor",
    "p53(clonebp53-11)": "p53",
}

# Spelling / language variants collapsed to a single canonical label, gathered
# from the manual df.loc[...] fixes scattered across the notebooks.
_TYPE_FIXES = {"carcinom": "carcinoma"}
_SUBTYPE_FIXES = {
    "carcinom": "carcinoma",
    "inflamatuar": "inflammatory",
    "inflammation": "inflammatory",
    "serrated": "hyperplastic",
    "nonspesific": "hyperplastic",
    "tubuvillous": "tubulovillous",
}


def _resolve(filename: str) -> Path:
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(
            f"Could not find {path}.\n"
            f"Download the dataset first, e.g. from the repo root:\n"
            f"    python scripts/download_zenodo.py     # or download_kaggle.py\n"
            f"or point VIMPOLYP_DATA_DIR at an existing copy."
        )
    return path


def load_ihc(filename: str = "ihc_data.xlsx", sheet_name: str | int = 0) -> pd.DataFrame:
    """Load the IHC biomarker table with clean column names and canonical labels.

    Returns a DataFrame with (where present) the columns in ``NUMERIC_MARKERS``
    coerced to numeric, plus normalised ``type`` / ``subtype`` string columns.
    """
    df = pd.read_excel(_resolve(filename), sheet_name=sheet_name)
    # Strip stray newlines/whitespace from headers, then apply the known renames.
    df.columns = df.columns.astype(str).str.replace(r"\s+", " ", regex=True).str.strip()
    df = df.rename(columns=_IHC_RENAME)

    for col in NUMERIC_MARKERS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = _normalise_labels(df)
    return df


def load_patho_metadata(
    filename: str = "pathoImagesWithLabels.xlsx", sheet_name: str | int = "Sheet1"
) -> pd.DataFrame:
    """Load the histopathology patch metadata table with canonical type/subtype."""
    df = pd.read_excel(_resolve(filename), sheet_name=sheet_name)
    return _normalise_labels(df)


def _normalise_labels(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "type" in df.columns:
        df["type"] = df["type"].astype("string").str.strip().replace(_TYPE_FIXES)
    if "subtype" in df.columns:
        df["subtype"] = df["subtype"].astype("string").str.strip().replace(_SUBTYPE_FIXES)
    return df
