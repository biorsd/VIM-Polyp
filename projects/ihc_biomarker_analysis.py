#!/usr/bin/env python3
"""Project 2 — Statistical analysis of IHC biomarkers across polyp types.

A ready-to-run analysis that answers: *do the IHC biomarkers differ between
polyp types?* For each numeric biomarker (Ki67, VEGF, CD34, CD34skor, p53, age)
it runs a Kruskal–Wallis test across polyp ``type`` groups (a non-parametric
ANOVA that does not assume normality — appropriate here, matching the
Shapiro–Wilk checks in notebooks/ihc-part.ipynb), and produces:

  * ``ihc_kruskal_results.csv`` — H statistic, p-value, and significance flag
    per biomarker;
  * ``ihc_boxplots_by_type.png`` — one boxplot panel per biomarker;
  * ``ihc_correlation_heatmap.png`` — Spearman correlations between biomarkers.

Only ``ihc_data.xlsx`` is required.

Run from the repo root:
    python projects/ihc_biomarker_analysis.py
    python projects/ihc_biomarker_analysis.py --group subtype
"""

from __future__ import annotations

import argparse
import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats

from common import NUMERIC_MARKERS, OUTPUT_DIR, load_ihc

ALPHA = 0.05


def kruskal_by_group(df: pd.DataFrame, group: str, markers: list[str]) -> pd.DataFrame:
    rows = []
    for marker in markers:
        sub = df[[group, marker]].dropna()
        groups = [g[marker].values for _, g in sub.groupby(group) if len(g) >= 3]
        if len(groups) < 2:
            rows.append({"biomarker": marker, "n_groups": len(groups),
                         "H": math.nan, "p_value": math.nan, "significant": False})
            continue
        h, p = stats.kruskal(*groups)
        rows.append({"biomarker": marker, "n_groups": len(groups),
                     "H": round(h, 3), "p_value": p, "significant": bool(p < ALPHA)})
    return pd.DataFrame(rows).sort_values("p_value", na_position="last")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--group", default="type", help="Grouping column: type or subtype (default: type)")
    args = parser.parse_args()

    df = load_ihc()
    if args.group not in df.columns:
        raise SystemExit(f"Group column '{args.group}' not found. Available: {list(df.columns)}")

    markers = [c for c in NUMERIC_MARKERS if c in df.columns and c != "age"] or \
              [c for c in NUMERIC_MARKERS if c in df.columns]
    if not markers:
        raise SystemExit(f"None of the biomarker columns {NUMERIC_MARKERS} are present.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1) Kruskal–Wallis tests.
    results = kruskal_by_group(df, args.group, markers)
    csv_path = OUTPUT_DIR / "ihc_kruskal_results.csv"
    results.to_csv(csv_path, index=False)
    print(f"=== Kruskal–Wallis across '{args.group}' groups (alpha={ALPHA}) ===")
    print(results.to_string(index=False))

    # 2) Boxplot grid, one biomarker per panel.
    n = len(markers)
    ncols = min(3, n)
    nrows = math.ceil(n / ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4 * nrows), squeeze=False)
    order = sorted(df[args.group].dropna().unique())
    for ax, marker in zip(axes.flat, markers):
        sub = df[[args.group, marker]].dropna()
        sns.boxplot(data=sub, x=args.group, y=marker, order=order, ax=ax)
        sns.stripplot(data=sub, x=args.group, y=marker, order=order, ax=ax,
                      color="black", alpha=0.35, size=3)
        prow = results.loc[results["biomarker"] == marker, "p_value"]
        p = prow.iloc[0] if len(prow) else math.nan
        star = " *" if (pd.notna(p) and p < ALPHA) else ""
        ax.set_title(f"{marker} (p={p:.3g}{star})" if pd.notna(p) else marker)
        ax.tick_params(axis="x", rotation=45)
    for ax in axes.flat[n:]:
        ax.set_visible(False)
    fig.suptitle(f"IHC biomarkers by polyp {args.group}", y=1.02, fontsize=14)
    fig.tight_layout()
    box_path = OUTPUT_DIR / "ihc_boxplots_by_type.png"
    fig.savefig(box_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    # 3) Spearman correlation heatmap between biomarkers.
    corr = df[markers].corr(method="spearman")
    fig, ax = plt.subplots(figsize=(1.2 * len(markers) + 2, 1.0 * len(markers) + 2))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="vlag", center=0, vmin=-1, vmax=1,
                square=True, cbar_kws={"shrink": 0.8}, ax=ax)
    ax.set_title("Spearman correlation between IHC biomarkers")
    fig.tight_layout()
    corr_path = OUTPUT_DIR / "ihc_correlation_heatmap.png"
    fig.savefig(corr_path, dpi=150)
    plt.close(fig)

    print(f"\nSaved: {csv_path}\n       {box_path}\n       {corr_path}")


if __name__ == "__main__":
    main()
