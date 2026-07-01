# Notebooks

All notebooks resolve the dataset location automatically via
[`src/vimpolyp_paths.py`](../src/vimpolyp_paths.py) — no manual path editing
needed. Each notebook's first code cell prints the resolved `DATA_DIR` /
`OUTPUT_DIR` and, on Kaggle/Colab, discovers those paths automatically; when
running locally it defaults to `../data` and `../outputs` (override with the
`VIMPOLYP_DATA_DIR` / `VIMPOLYP_OUTPUT_DIR` environment variables). Make sure
you've downloaded the dataset first — see the [root README](../README.md#2--quick-start).

| Notebook | Purpose | Data it needs |
|---|---|---|
| [`ihc-part.ipynb`](ihc-part.ipynb) | Exploratory IHC statistics: descriptive summaries, Shapiro–Wilk normality tests, categorical/numeric breakdowns for the 6 biomarkers | `ihc_data.xlsx` |
| [`pathoimageswithlabels.ipynb`](pathoimageswithlabels.ipynb) | Histopathology patch metadata loader: patient/polyp counts and polyp-type distribution plots | `pathoImagesWithLabels.xlsx` |
| [`colonvideoswithlabel.ipynb`](colonvideoswithlabel.ipynb) | Cross-modality overview: merges video, IHC, and histopathology metadata and plots IHC biomarker distributions by polyp type | `colonVideosWithLabels.xlsx`, `ihcData.xlsx`, `pathoImagesWithLabels.xlsx` |
| [`colonvideoswithlabels.ipynb`](colonvideoswithlabels.ipynb) | Full video pipeline: demographic/label plots, OpenCV key-frame extraction from `.avi` files, and ResNet50 (TensorFlow) frame embeddings | `colonVideosWithLabels.xlsx`, `colonVideosWithLabels/*.avi` |
| [`summarypatientsihc.ipynb`](summarypatientsihc.ipynb) | Patient-level IHC summary dashboard: polyp type/subtype counts, age/gender breakdowns | `ihc_data.xlsx`, `ihcData.xlsx` |
| [`GUST_pathoIHC.ipynb`](GUST_pathoIHC.ipynb) | Feature fusion: joins histopathology image patches with IHC scores and prepares ViT (transformers) / tabular features for modelling with PyTorch | `ihc_data.xlsx`, `10x/10x/` patch folder |

## Running a notebook

```bash
# from the repo root, after installing dependencies and downloading data
jupyter lab notebooks/ihc-part.ipynb
```

Notebooks opened directly on Google Colab (via the "Open in Colab" badge)
clone this repository automatically in their setup cell, so no manual `git
clone` is required there either.
