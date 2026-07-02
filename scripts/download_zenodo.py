#!/usr/bin/env python3
"""Download the VIM-Polyp dataset files from Zenodo into ``data/``.

Usage
-----
    python scripts/download_zenodo.py
    python scripts/download_zenodo.py --doi 10.5281/zenodo.15388073 --dest data/
    python scripts/download_zenodo.py --files ihc_data.xlsx colonVideosWithLabels.xlsx

The script talks to the public Zenodo REST API (no API key required for public
records), lists every file attached to the record, and downloads it with a
resumable streaming request. Re-running the script skips files that already
exist locally with the expected size.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import requests

DEFAULT_DOI = "10.5281/zenodo.15388073"
ZENODO_API = "https://zenodo.org/api/records/{record_id}"
CHUNK_SIZE = 1024 * 1024  # 1 MiB


def record_id_from_doi(doi: str) -> str:
    match = re.search(r"zenodo\.(\d+)", doi)
    if not match:
        raise ValueError(f"Could not extract a Zenodo record id from DOI: {doi!r}")
    return match.group(1)


def fetch_record_metadata(record_id: str) -> dict:
    url = ZENODO_API.format(record_id=record_id)
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def download_file(url: str, dest: Path, expected_size: int | None) -> None:
    if dest.exists() and expected_size is not None and dest.stat().st_size == expected_size:
        print(f"  [skip] {dest.name} already downloaded ({expected_size} bytes)")
        return

    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"  [get]  {dest.name}")
    with requests.get(url, stream=True, timeout=60) as response:
        response.raise_for_status()
        with open(dest, "wb") as fh:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    fh.write(chunk)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--doi", default=DEFAULT_DOI, help=f"Zenodo DOI of the dataset record (default: {DEFAULT_DOI})")
    parser.add_argument("--dest", default="data", help="Destination directory (default: data/)")
    parser.add_argument("--files", nargs="*", default=None, help="Only download these specific file names (default: all files in the record)")
    args = parser.parse_args()

    record_id = record_id_from_doi(args.doi)
    print(f"Fetching Zenodo record metadata for record {record_id} (DOI {args.doi})...")
    metadata = fetch_record_metadata(record_id)

    files = metadata.get("files", [])
    if not files:
        print("No files found on this Zenodo record.", file=sys.stderr)
        return 1

    if args.files:
        wanted = set(args.files)
        files = [f for f in files if f["key"] in wanted]
        missing = wanted - {f["key"] for f in files}
        if missing:
            print(f"Warning: requested files not found in record: {sorted(missing)}", file=sys.stderr)

    dest_dir = Path(args.dest)
    print(f"Downloading {len(files)} file(s) into {dest_dir.resolve()}")
    for entry in files:
        download_file(
            url=entry["links"]["self"],
            dest=dest_dir / entry["key"],
            expected_size=entry.get("size"),
        )

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
