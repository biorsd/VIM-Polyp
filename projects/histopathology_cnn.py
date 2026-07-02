#!/usr/bin/env python3
"""Project 3 — Histopathology polyp-type image classifier (transfer learning).

Fine-tunes a pretrained ResNet18 to classify histopathology patches by polyp
``type``. Labels are derived exactly the way notebooks/GUST_pathoIHC.ipynb does:
each image filename encodes a ``patient-polyp`` id (``patho-patient1-polyp1-...``),
which is joined to ``pathoImagesWithLabels.xlsx`` to look up the polyp type;
filenames containing ``normal`` / ``carcinom`` are labelled directly.

Key detail: the train/validation split is **grouped by patient**, so patches
from the same patient never appear in both sets (prevents optimistic leakage).

Requires the histopathology image folder (default ``<DATA_DIR>/10x/10x``) plus
``pathoImagesWithLabels.xlsx``. A GPU is used automatically if available, but it
also runs on CPU (use ``--limit`` for a quick smoke test).

Run from the repo root:
    python projects/histopathology_cnn.py
    python projects/histopathology_cnn.py --images-root "20x/20x" --epochs 5
    python projects/histopathology_cnn.py --limit 200 --epochs 1   # fast sanity check
"""

from __future__ import annotations

import argparse
import glob
import os
from collections import Counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from common import DATA_DIR, OUTPUT_DIR, load_patho_metadata

IMAGE_EXTS = ("*.tiff", "*.tif", "*.jpg", "*.jpeg", "*.png")


def extract_patient_polyp(filename: str) -> tuple[str, str | None]:
    """Return (patient_polyp_id, explicit_status) from a patho image filename.

    Mirrors the parsing in GUST_pathoIHC.ipynb: split on '-', part[1] is the
    patient, part[2] is the polyp (or a 'normal'/'carcinom' marker).
    """
    parts = os.path.basename(filename).split("-")
    lower = filename.lower()
    status = None
    for key in ("normal", "carcinom", "control"):
        if key in lower:
            status = key
            break
    if len(parts) >= 3:
        patient = parts[1].strip()
        if status in ("normal", "carcinom", "control"):
            return f"{patient}-{status}", status
        polyp = parts[2].strip()
        return f"{patient}-{polyp}", status
    return os.path.basename(filename), status


def build_index(images_root, meta: pd.DataFrame) -> pd.DataFrame:
    paths = []
    for ext in IMAGE_EXTS:
        paths.extend(glob.glob(os.path.join(str(images_root), "**", ext), recursive=True))
    if not paths:
        raise SystemExit(
            f"No images found under {images_root}.\n"
            f"Download the dataset (python scripts/download_zenodo.py) or pass "
            f"--images-root pointing at a magnification folder that contains patches."
        )

    meta = meta.copy()
    meta["patient_polyp"] = (
        meta["patient"].astype(str).str.strip() + "-" + meta["polyp"].astype(str).str.strip()
    )
    pp_to_type = dict(zip(meta["patient_polyp"], meta["type"]))

    rows = []
    for p in paths:
        pid, status = extract_patient_polyp(p)
        label = "carcinoma" if status == "carcinom" else status if status else pp_to_type.get(pid)
        patient = pid.split("-")[0]
        if pd.notna(label) and label is not None:
            rows.append({"image_path": p, "patient": patient, "label": str(label)})
    df = pd.DataFrame(rows)
    if df.empty:
        raise SystemExit("Found images but could not map any to a label — check filename format / metadata.")
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--images-root", default="10x/10x",
                        help="Image folder relative to DATA_DIR (default: 10x/10x)")
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--val-frac", type=float, default=0.2)
    parser.add_argument("--min-class-size", type=int, default=20)
    parser.add_argument("--limit", type=int, default=0, help="Use at most N images (0 = all; for quick tests)")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    # Heavy deps imported lazily so the other projects don't need torch installed.
    import torch
    from sklearn.model_selection import GroupShuffleSplit
    from torch import nn
    from torch.utils.data import DataLoader, Dataset
    from torchvision import models, transforms
    from torchvision.models import ResNet18_Weights
    from PIL import Image

    torch.manual_seed(args.seed)
    np.random.seed(args.seed)

    images_root = DATA_DIR / args.images_root
    meta = load_patho_metadata()
    index = build_index(images_root, meta)

    # Keep only sufficiently populated classes.
    counts = index["label"].value_counts()
    keep = counts[counts >= args.min_class_size].index
    index = index[index["label"].isin(keep)].reset_index(drop=True)
    if index["label"].nunique() < 2:
        raise SystemExit(f"Fewer than 2 classes with >= {args.min_class_size} images. Counts: {dict(counts)}")
    if args.limit:
        index = index.sample(n=min(args.limit, len(index)), random_state=args.seed).reset_index(drop=True)

    classes = sorted(index["label"].unique())
    class_to_idx = {c: i for i, c in enumerate(classes)}
    print(f"{len(index)} images, {len(classes)} classes: {dict(index['label'].value_counts())}")

    # Patient-grouped split to avoid leakage.
    gss = GroupShuffleSplit(n_splits=1, test_size=args.val_frac, random_state=args.seed)
    train_idx, val_idx = next(gss.split(index, groups=index["patient"]))
    train_df = index.iloc[train_idx].reset_index(drop=True)
    val_df = index.iloc[val_idx].reset_index(drop=True)
    print(f"Train: {len(train_df)} images / {train_df['patient'].nunique()} patients | "
          f"Val: {len(val_df)} images / {val_df['patient'].nunique()} patients")

    weights = ResNet18_Weights.DEFAULT
    preprocess = weights.transforms()
    train_tf = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        preprocess,
    ])

    class PatchDataset(Dataset):
        def __init__(self, frame, tf):
            self.frame = frame
            self.tf = tf

        def __len__(self):
            return len(self.frame)

        def __getitem__(self, i):
            row = self.frame.iloc[i]
            img = Image.open(row["image_path"]).convert("RGB")
            return self.tf(img), class_to_idx[row["label"]]

    train_loader = DataLoader(PatchDataset(train_df, train_tf), batch_size=args.batch_size,
                              shuffle=True, num_workers=2)
    val_loader = DataLoader(PatchDataset(val_df, preprocess), batch_size=args.batch_size,
                            shuffle=False, num_workers=2)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    model = models.resnet18(weights=weights)
    for p in model.parameters():   # freeze backbone, train the new head
        p.requires_grad = False
    model.fc = nn.Linear(model.fc.in_features, len(classes))
    model = model.to(device)

    # Class-weighted loss to counter imbalance.
    freq = Counter(train_df["label"])
    class_weights = torch.tensor(
        [len(train_df) / (len(classes) * freq[c]) for c in classes], dtype=torch.float32, device=device)
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    optimizer = torch.optim.Adam(model.fc.parameters(), lr=args.lr)

    def run_epoch(loader, train: bool):
        model.train(train)
        total, correct, loss_sum = 0, 0, 0.0
        all_true, all_pred = [], []
        with torch.set_grad_enabled(train):
            for x, y in loader:
                x, y = x.to(device), y.to(device)
                logits = model(x)
                loss = criterion(logits, y)
                if train:
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()
                loss_sum += loss.item() * x.size(0)
                pred = logits.argmax(1)
                correct += (pred == y).sum().item()
                total += x.size(0)
                all_true.extend(y.cpu().tolist())
                all_pred.extend(pred.cpu().tolist())
        return loss_sum / total, correct / total, all_true, all_pred

    best_acc, best_state = 0.0, None
    for epoch in range(1, args.epochs + 1):
        tr_loss, tr_acc, _, _ = run_epoch(train_loader, train=True)
        va_loss, va_acc, y_true, y_pred = run_epoch(val_loader, train=False)
        print(f"Epoch {epoch:2d}/{args.epochs} | train loss {tr_loss:.3f} acc {tr_acc:.3f} "
              f"| val loss {va_loss:.3f} acc {va_acc:.3f}")
        if va_acc >= best_acc:
            best_acc, best_state = va_acc, {"y_true": y_true, "y_pred": y_pred}
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            torch.save({"model_state": model.state_dict(), "classes": classes},
                       OUTPUT_DIR / "histopathology_resnet18.pt")

    # Confusion matrix for the best epoch.
    from sklearn.metrics import ConfusionMatrixDisplay, classification_report
    print(f"\nBest val accuracy: {best_acc:.3f}")
    print(classification_report(best_state["y_true"], best_state["y_pred"],
                                target_names=classes, zero_division=0))
    fig, ax = plt.subplots(figsize=(6, 5))
    ConfusionMatrixDisplay.from_predictions(
        best_state["y_true"], best_state["y_pred"],
        display_labels=classes, ax=ax, xticks_rotation=45, colorbar=False)
    ax.set_title("Histopathology type — validation confusion matrix")
    fig.tight_layout()
    cm_path = OUTPUT_DIR / "histopathology_confusion_matrix.png"
    fig.savefig(cm_path, dpi=150)
    plt.close(fig)
    print(f"Saved: {OUTPUT_DIR / 'histopathology_resnet18.pt'}\n       {cm_path}")


if __name__ == "__main__":
    main()
