# Example Projects

Three self-contained, runnable projects built on the VIM-Polyp dataset. Each
one resolves the data location through [`src/vimpolyp_paths.py`](../src/vimpolyp_paths.py)
(auto-detects Kaggle / Colab / local `./data`; override with `VIMPOLYP_DATA_DIR`)
and writes its figures/models into `OUTPUT_DIR` (`./outputs` locally). Shared
data loading and label normalisation live in [`common.py`](common.py).

Run everything from the **repo root** after installing dependencies and
downloading the data:

```bash
pip install -r requirements.txt
python scripts/download_zenodo.py          # or download_kaggle.py
```

| # | Project | Script | Needs | Output |
|---|---------|--------|-------|--------|
| 1 | Polyp type from IHC biomarkers | [`polyp_type_classifier.py`](polyp_type_classifier.py) | `ihc_data.xlsx` | cross-validated report, confusion matrix, feature-importance chart |
| 2 | IHC biomarker statistics | [`ihc_biomarker_analysis.py`](ihc_biomarker_analysis.py) | `ihc_data.xlsx` | Kruskal–Wallis CSV, boxplots by type, correlation heatmap |
| 3 | Histopathology image classifier | [`histopathology_cnn.py`](histopathology_cnn.py) | `10x/10x/` patches + `pathoImagesWithLabels.xlsx` | trained ResNet18, confusion matrix |

## 1 — Polyp type classifier (tabular ML)

Trains a class-balanced Random Forest to predict a polyp's `type` from its IHC
biomarker profile, evaluated with stratified k-fold cross-validation (an honest
estimate on this small, imbalanced dataset). Rare classes are dropped
automatically.

```bash
python projects/polyp_type_classifier.py
python projects/polyp_type_classifier.py --target subtype --min-class-size 10
```

## 2 — IHC biomarker statistics

For each biomarker, runs a non-parametric Kruskal–Wallis test across polyp-type
groups (no normality assumption — consistent with the Shapiro–Wilk checks in
`notebooks/ihc-part.ipynb`), and plots per-marker boxplots plus a Spearman
correlation heatmap.

```bash
python projects/ihc_biomarker_analysis.py
python projects/ihc_biomarker_analysis.py --group subtype
```

## 3 — Histopathology image classifier (transfer learning)

Fine-tunes a pretrained ResNet18 on histopathology patches. Labels come from the
`patient-polyp` id encoded in each filename, joined to `pathoImagesWithLabels.xlsx`
(same logic as `notebooks/GUST_pathoIHC.ipynb`). The **train/val split is grouped
by patient** so no patient leaks across the split. Runs on GPU if available,
otherwise CPU.

```bash
python projects/histopathology_cnn.py                     # full run
python projects/histopathology_cnn.py --images-root "20x/20x" --epochs 5
python projects/histopathology_cnn.py --limit 200 --epochs 1   # quick smoke test
```

> Note: results depend on the exact patch/label distribution in your copy of the
> dataset; the scripts print the class counts they actually found so you can
> sanity-check before trusting the metrics.
