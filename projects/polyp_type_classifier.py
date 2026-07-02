#!/usr/bin/env python3
"""Project 1 — Predict polyp type from IHC biomarkers.

A self-contained, ready-to-run machine-learning project on the VIM-Polyp IHC
table. It trains a Random Forest to classify a polyp's ``type`` (e.g.
neoplastic / nonneoplastic / normal / carcinoma) from its immunohistochemistry
biomarker profile (age, Ki67, VEGF, CD34, CD34skor, p53), reports
cross-validated performance, and writes a confusion matrix and a
feature-importance chart to ``outputs/``.

Only ``ihc_data.xlsx`` is required — no images, videos, or GPU.

Run from the repo root:
    python projects/polyp_type_classifier.py
    python projects/polyp_type_classifier.py --target subtype --min-class-size 10
"""

from __future__ import annotations

import argparse

import matplotlib

matplotlib.use("Agg")  # headless: save figures without a display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import ConfusionMatrixDisplay, classification_report
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline

from common import NUMERIC_MARKERS, OUTPUT_DIR, load_ihc


def build_dataset(target: str, min_class_size: int) -> tuple[pd.DataFrame, pd.Series, list[str]]:
    df = load_ihc()
    if target not in df.columns:
        raise SystemExit(f"Target column '{target}' not found. Available: {list(df.columns)}")

    features = [c for c in NUMERIC_MARKERS if c in df.columns]
    if not features:
        raise SystemExit(f"None of the expected biomarker columns {NUMERIC_MARKERS} are present.")

    data = df[features + [target]].copy()
    data = data.dropna(subset=[target])
    data[target] = data[target].astype(str).str.strip()

    # Drop classes too small to train/evaluate on.
    counts = data[target].value_counts()
    keep = counts[counts >= min_class_size].index
    dropped = counts[counts < min_class_size]
    if len(dropped):
        print(f"Dropping {len(dropped)} rare class(es) with < {min_class_size} samples: "
              f"{dict(dropped)}")
    data = data[data[target].isin(keep)]

    if data[target].nunique() < 2:
        raise SystemExit("Fewer than 2 usable classes remain — lower --min-class-size or check the data.")

    X = data[features]
    y = data[target]
    print(f"Dataset: {len(X)} samples, {len(features)} features, "
          f"{y.nunique()} classes -> {dict(y.value_counts())}")
    return X, y, features


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--target", default="type", help="Column to predict (default: type)")
    parser.add_argument("--min-class-size", type=int, default=8,
                        help="Drop classes with fewer than this many samples (default: 8)")
    parser.add_argument("--folds", type=int, default=5, help="Cross-validation folds (default: 5)")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    X, y, features = build_dataset(args.target, args.min_class_size)

    model = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("rf", RandomForestClassifier(
            n_estimators=400, class_weight="balanced", random_state=args.seed, n_jobs=-1)),
    ])

    # Honest performance estimate via stratified cross-validation.
    n_folds = min(args.folds, int(y.value_counts().min()))
    if n_folds < 2:
        raise SystemExit("Smallest class has <2 samples; cannot cross-validate.")
    cv = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=args.seed)
    y_pred = cross_val_predict(model, X, y, cv=cv, n_jobs=-1)

    print(f"\n=== {n_folds}-fold cross-validated classification report "
          f"(predicting '{args.target}') ===")
    print(classification_report(y, y_pred, zero_division=0))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Confusion matrix figure.
    labels = sorted(y.unique())
    fig, ax = plt.subplots(figsize=(6, 5))
    ConfusionMatrixDisplay.from_predictions(y, y_pred, labels=labels, ax=ax, xticks_rotation=45, colorbar=False)
    ax.set_title(f"Polyp {args.target} — CV confusion matrix")
    fig.tight_layout()
    cm_path = OUTPUT_DIR / f"polyp_{args.target}_confusion_matrix.png"
    fig.savefig(cm_path, dpi=150)
    plt.close(fig)

    # Feature importance: fit on the full data for an interpretable ranking.
    model.fit(X, y)
    importances = model.named_steps["rf"].feature_importances_
    order = np.argsort(importances)[::-1]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh([features[i] for i in order][::-1], importances[order][::-1], color="#4C72B0")
    ax.set_xlabel("Gini importance")
    ax.set_title(f"Biomarker importance for predicting {args.target}")
    fig.tight_layout()
    fi_path = OUTPUT_DIR / f"polyp_{args.target}_feature_importance.png"
    fig.savefig(fi_path, dpi=150)
    plt.close(fig)

    print("\nRanked biomarker importance:")
    for i in order:
        print(f"  {features[i]:10s} {importances[i]:.3f}")
    print(f"\nSaved: {cm_path}\n       {fi_path}")


if __name__ == "__main__":
    main()
