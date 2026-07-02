#!/usr/bin/env python3
"""Download the VIM-Polyp dataset from Kaggle into ``data/``.

Requires a Kaggle API token (``~/.kaggle/kaggle.json``) - see
https://www.kaggle.com/docs/api for how to generate one.

Usage
-----
    python scripts/download_kaggle.py
    python scripts/download_kaggle.py --dataset refikasultandogan/colonpolyp --dest data/
"""

from __future__ import annotations

import argparse
from pathlib import Path

DEFAULT_DATASET = "refikasultandogan/colonpolyp"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dataset", default=DEFAULT_DATASET, help=f"Kaggle dataset slug (default: {DEFAULT_DATASET})")
    parser.add_argument("--dest", default="data", help="Destination directory (default: data/)")
    args = parser.parse_args()

    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
    except ImportError:
        raise SystemExit(
            "The 'kaggle' package is not installed. Run `pip install kaggle` "
            "(already included in requirements.txt) and configure "
            "~/.kaggle/kaggle.json before retrying."
        )

    dest_dir = Path(args.dest)
    dest_dir.mkdir(parents=True, exist_ok=True)

    api = KaggleApi()
    api.authenticate()

    print(f"Downloading Kaggle dataset '{args.dataset}' into {dest_dir.resolve()} ...")
    api.dataset_download_files(args.dataset, path=str(dest_dir), unzip=True, quiet=False)
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
