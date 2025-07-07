# VIM-Polyp
VIM-Polyp: A Multimodal Dataset of Colonoscopy Videos, Histopathology Images, and Protein Expression Levels from Colorectal Polyps

# VIM‑Polyp Repository  
A multimodal benchmark dataset & code base for colorectal polyp research  
*(Colonoscopy videos • Histopathology images • IHC biomarker scores)*  

[![Zenodo](https://img.shields.io/badge/Data-Zenodo-%23009788)](https://doi.org/10.5281/zenodo.15388073)
[![Kaggle](https://img.shields.io/badge/Data-Kaggle-blue)](https://www.kaggle.com/datasets/refikasultandogan/vim-polyp)
[![License: ODbL](https://img.shields.io/badge/License-ODbL-brightgreen.svg)](LICENSE)

---

## 1  Overview
This repo hosts **all notebooks & helper scripts** that accompany  

> **Doğan RS\*, Akay E, Doğan S, Yılmaz B.**  
> *VIM‑Polyp: Multimodal Colon Polyp Dataset with Video, Histopathology, and Protein Expression*  
> *Scientific Data* (under review, 2025)

The full dataset mixes three modalities gathered from **201 patients / 399 polyps**:

| Modality | Volume | Folder | Purpose |
|----------|--------|--------|---------|
| Colonoscopy videos | 202 raw, 133 labelled (`.avi`, 422 min) | `colonVideosWithLabels/` | Endoscopic appearance & localisation |
| Histopathology images | 1 903 WSIs patches (`.tiff`) at 5 magnifications | `pathoImagesWithLabels/` | Cellular morphology |
| Immunohistochemistry (IHC) | 6 biomarkers × 383 polyps | `ihc_data.xlsx` | Protein‑level phenotype |

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
  title   = {VIM‑Polyp: Multimodal Colon Polyp Dataset with Video, Histopathology, and Protein Expression},
  journal = {Scientific Data},
  year    = {2025},
  note    = {under review}
}

Acknowledgements
Data collection was funded by TÜBİTAK 1001 — Grant 120E204 and forms part of the PhD thesis “Artificial Intelligence Assisted Prognostic Marker Determination from Colonoscopy and Histopathology Images for Colon Polyps” (R.S. Doğan, 2023).
We thank Kayseri City Hospital Gastroenterology & Pathology Departments for their support.

Contact
Questions or issues? Open an issue or contact
Dr Refika Sultan Doğan
• doganrefikasultan@gmail.com

