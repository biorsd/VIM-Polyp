# VIM-Polyp
VIM-Polyp: A Multimodal Dataset of Colonoscopy Videos, Histopathology Images, and Protein Expression Levels from Colorectal Polyps

# VIM‑Polyp Repository  
A multimodal benchmark dataset & code base for colorectal polyp research  
*(Colonoscopy videos • Histopathology images • IHC biomarker scores)*  

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

## 2  Quick start  

```bash
# ① clone code
git clone https://github.com/YOUR‑ORG/VIM-Polyp.git
cd VIM-Polyp

# ② create environment
conda env create -f environment.yml      # or pip install -r requirements.txt
conda activate vimpolyp

# ③ fetch data (choose ONE):
python scripts/download_zenodo.py  --doi 10.5281/zenodo.15388073
#        ‑‑or‑‑
kaggle datasets download refikasultandogan/colon-polyp-dataset -p data/ --unzip

# ④ open example notebook
jupyter lab notebooks/colonvideoswithlabel.ipynb

3  Repository layout
VIM-Polyp/
├── notebooks/
│   ├── colonvideoswithlabel.ipynb       # Video preprocessing, labelling demo
│   ├── colonvideoswithlabels.ipynb      # Alternative pipe incl. vessel‑density filter
│   ├── pathoimageswithlabels.ipynb      # Histopath patch loader & stain‑norm
│   ├── ihc-part.ipynb                   # Exploratory IHC stats & Shapiro–Wilk tests
│   └── summarypatientsihc.ipynb         # Patient‑level summary dashboard
├── scripts/
│   └── download_zenodo.py               # DOI‑based bulk fetch helper
├── data/                                # <-- you download into here
│   ├── colonVideosWithLabels/
│   ├── pathoImagesWithLabels/
│   └── *.xlsx
├── README.md
├── LICENSE
└── environment.yml / requirements.txt

How to cite?
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




Acknowledgements
Data collection was funded by TÜBİTAK 1001 — Grant 120E204 and forms part of the PhD thesis “Artificial Intelligence Assisted Prognostic Marker Determination from Colonoscopy and Histopathology Images for Colon Polyps” (R.S. Doğan, 2023).
We thank Kayseri City Hospital Gastroenterology & Pathology Departments for their support.

Contact
Questions or issues? Open an issue or contact
Dr Refika Sultan Doğan
• doganrefikasultan@gmail.com

