"""Shared data/output path resolution for every VIM-Polyp notebook and script.

All notebooks import ``DATA_DIR`` and ``OUTPUT_DIR`` from this module instead of
hard-coding platform-specific paths (``/kaggle/input/...``, ``/content/Kaggle/...``).
This makes the same notebook run unmodified on Kaggle, Google Colab, and a local
clone of the repository.

Resolution order for DATA_DIR:
    1. ``VIMPOLYP_DATA_DIR`` environment variable, if set.
    2. Kaggle's mounted dataset path (``/kaggle/input/colonpolyp``), if it exists.
    3. Google Colab's conventional download location (``/content/Kaggle``), if it exists.
    4. ``<repo_root>/data`` (the location ``scripts/download_zenodo.py`` and
       ``scripts/download_kaggle.py`` write to by default).

Resolution order for OUTPUT_DIR:
    1. ``VIMPOLYP_OUTPUT_DIR`` environment variable, if set.
    2. Kaggle's writable working directory (``/kaggle/working``), if it exists.
    3. ``<repo_root>/outputs`` (created automatically).
"""

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _detect_data_dir() -> Path:
    env = os.environ.get("VIMPOLYP_DATA_DIR")
    if env:
        return Path(env).expanduser()

    kaggle_dir = Path("/kaggle/input/colonpolyp")
    if kaggle_dir.exists():
        return kaggle_dir

    colab_dir = Path("/content/Kaggle")
    if colab_dir.exists():
        return colab_dir

    return REPO_ROOT / "data"


def _detect_output_dir() -> Path:
    env = os.environ.get("VIMPOLYP_OUTPUT_DIR")
    if env:
        out = Path(env).expanduser()
    elif Path("/kaggle/working").exists():
        out = Path("/kaggle/working")
    else:
        out = REPO_ROOT / "outputs"

    out.mkdir(parents=True, exist_ok=True)
    return out


DATA_DIR = _detect_data_dir()
OUTPUT_DIR = _detect_output_dir()


if __name__ == "__main__":
    print(f"DATA_DIR:   {DATA_DIR}")
    print(f"OUTPUT_DIR: {OUTPUT_DIR}")
