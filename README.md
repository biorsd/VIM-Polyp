# VIM-Polyp
A multimodal benchmark dataset & code base for colorectal polyp research (colonoscopy videos, histopathology images, IHC biomarker scores).

[![Zenodo](https://img.shields.io/badge/Data-Zenodo-%23009788)](https://doi.org/10.5281/zenodo.15388073)
[![Kaggle](https://img.shields.io/badge/Data-Kaggle-blue)](https://www.kaggle.com/datasets/refikasultandogan/colonpolyp/data)[![License: CC BY 4.0](https://img.shields.io/badge/License-CC--BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)


---

## 1  Overview
This repo hosts **all notebooks & helper scripts** that accompany  

> **Doğan RS\*, Akay E, Doğan S, Yılmaz B.**  
> *VIM‑Polyp: Multimodal Colon Polyp Dataset with Video, Histopathology, and Protein Expression*  
> *Nature Scientific Data* (2025)

The full dataset mixes three modalities gathered from **201 patients / 399 polyps**:

| Modality | Volume | Folder | Purpose |
|----------|--------|--------|---------|
| Colonoscopy videos | 202 raw, 133 labelled (`.avi`, 422 min) | `colonVideosWithLabels/` | Endoscopic appearance & localisation |
| Histopathology images | 1 903 WSIs patches (`.tiff`) at 5 magnifications | `pathoImagesWithLabels/` | Cellular morphology |
| Immunohistochemistry (IHC) | 6 biomarkers × 394 polyps | `ihc_data.xlsx` | Protein‑level phenotype |

Each patient/polyp carries a **shared ID** so you can fuse the three tracks.

---

## 2  Quick start

```bash
# clone the code
git clone https://github.com/biorsd/VIM-Polyp.git
cd VIM-Polyp

# create the environment
conda env create -f environment.yml && conda activate vimpolyp   # or: pip install -r requirements.txt

# fetch the data (choose ONE) -- both write into ./data by default
python scripts/download_zenodo.py                  # public, no account needed
#        --or--
python scripts/download_kaggle.py                  # requires ~/.kaggle/kaggle.json

# open an example notebook -- paths resolve automatically, see notebooks/README.md
jupyter lab notebooks/ihc-part.ipynb
```

Every notebook's first cell auto-detects where the data lives (Kaggle, Colab,
or your local `./data`), so you never have to hand-edit a file path. Override
the defaults at any time with:

```bash
export VIMPOLYP_DATA_DIR=/path/to/data
export VIMPOLYP_OUTPUT_DIR=/path/to/outputs
```

## 3  Repository layout

```
VIM-Polyp/
├── notebooks/
│   ├── README.md                        # what each notebook does & what data it needs
│   ├── ihc-part.ipynb                   # Exploratory IHC stats & Shapiro-Wilk tests
│   ├── pathoimageswithlabels.ipynb      # Histopath patch metadata loader & plots
│   ├── colonvideoswithlabel.ipynb       # Cross-modality overview & IHC plots
│   ├── colonvideoswithlabels.ipynb      # Video pipeline: key-frame extraction + ResNet50
│   ├── summarypatientsihc.ipynb         # Patient-level summary dashboard
│   └── GUST_pathoIHC.ipynb              # Histopathology image + IHC feature fusion (ViT/PyTorch)
├── projects/                            # runnable example ML / analysis projects
│   ├── README.md
│   ├── common.py                       # shared data loaders (reuse src/vimpolyp_paths.py)
│   ├── polyp_type_classifier.py        # predict polyp type from IHC biomarkers (RandomForest)
│   ├── ihc_biomarker_analysis.py       # Kruskal–Wallis + correlation analysis of biomarkers
│   └── histopathology_cnn.py           # ResNet18 transfer-learning image classifier
├── scripts/
│   ├── download_zenodo.py               # DOI-based bulk fetch helper (Zenodo REST API)
│   └── download_kaggle.py               # Kaggle API download helper
├── src/
│   └── vimpolyp_paths.py                # DATA_DIR / OUTPUT_DIR auto-detection, shared by every notebook
├── data/                                # <-- you download into here (git-ignored)
│   ├── colonVideosWithLabels/
│   ├── 10x/, 20x/, ...                  # histopathology patch magnifications
│   └── *.xlsx
├── outputs/                             # <-- generated plots/figures land here (git-ignored)
├── README.md
├── LICENSE
├── requirements.txt
└── environment.yml
```

## 4  Citation

If you use this dataset or code, please cite:

```bibtex
@dataset{Dogan2025_VIMPolyp,
  author       = {Doğan, Refika Sultan and Akay, Ebru and Doğan, Serkan and Yılmaz, Bülent},
  title        = {VIM-Polyp: Multimodal Colon Polyp Dataset (v1.0)},
  year         = {2025},
  doi          = {10.5281/zenodo.15388073}
}

@article{Dogan2025_SciData,
  author  = {Doğan, R. S. and Akay, E. and Doğan, S. and Yılmaz, B.},
  title   = {VIM-Polyp: Multimodal Colon Polyp Dataset with Video, Histopathology, and Protein Expression},
  journal = {Scientific Data},
  year    = {2025}
}

@article{Dogan2024_FrontOncol,
  author  = {Doğan, R. S. and Yılmaz, B.},
  title   = {Histopathology image classification: highlighting the gap between manual analysis and AI automation},
  journal = {Frontiers in Oncology},
  volume  = {13},
  pages   = {1325271},
  year    = {2024},
  doi     = {10.3389/fonc.2023.1325271},
  url     = {https://www.frontiersin.org/journals/oncology/articles/10.3389/fonc.2023.1325271/full}
}


@article{Dogan2024_IntelMed,
  author  = {Doğan, R. S. and Akay, E. and Doğan, S. and Yılmaz, B.},
  title   = {Hyperplastic and tubular polyp classification using machine learning and feature selection},
  journal = {Intelligence-Based Medicine},
  volume  = {10},
  pages   = {100177},
  year    = {2024},
  doi     = {10.1016/j.ibmed.2024.100177},
  url     = {https://linkinghub.elsevier.com/retrieve/pii/S2666521224000449}
}


@inproceedings{Dogan2018_TIPTEKNO,
  author  = {Doğan, R. S. and Yılmaz, B.},
  title   = {Polyp localization in colonoscopy images using vessel density},
  booktitle = {2018 Medical Technologies National Congress (TIPTEKNO)},
  pages   = {1--4},
  year    = {2018}
}

@article{Dogan2024_IJIST,
  author  = {Kaçmaz, R. N. and Doğan, R. S. and Yılmaz, B.},
  title   = {A comprehensive study on automatic non‐informative frame detection in colonoscopy videos},
  journal = {International Journal of Imaging Systems and Technology},
  volume  = {34},
  number  = {1},
  pages   = {e23017},
  year    = {2024}
}

@article{Dogan2021_EuroBiotech,
  author  = {Doğan, R. and Yılmaz, B.},
  title   = {Comparison of deep learning and conventional machine learning methods for classification of colon polyp types},
  journal = {EuroBiotech Journal},
  volume  = {5},
  number  = {1},
  year    = {2021}
}

@inproceedings{Dogan2023_EMR,
  author  = {Doğan, R. S. and Akay, E. and Doğan, S. and Yılmaz, B.},
  title   = {Feature Extraction and Biomarker Analysis for Differentiating Colon Polyps from Colonoscopic Images},
  booktitle = {The 12th Conference of Eastern Mediterranean Region of International Federation of Automatic Control (IFAC)},
  year    = {2023}
}

@phdthesis{Dogan2023_AGU,
  author  = {Doğan, R. S.},
  title   = {Artificial intelligence assisted prognostic marker determination from colonoscopy and histopathology images for colon polyps},
  school  = {Abdullah Gül University},
  year    = {2023}
}

```

## 5  Acknowledgements

Data collection was funded by TÜBİTAK 1001 — Grant 120E204 and forms part of the PhD thesis
"Artificial Intelligence Assisted Prognostic Marker Determination from Colonoscopy and
Histopathology Images for Colon Polyps" (R.S. Doğan, 2023).
We thank Kayseri City Hospital Gastroenterology & Pathology Departments for their support.

## 6  Contact

Questions or issues? Open an issue on this repository, or contact Dr Refika Sultan Doğan
at doganrefikasultan@gmail.com.
