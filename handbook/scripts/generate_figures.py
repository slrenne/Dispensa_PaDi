#!/usr/bin/env python3
"""
generate_figures.py
-------------------
Reproducible script for generating supplementary figures for the
Digital Pathology and Image Analysis course handbook.

All primary figures are generated as TikZ/LaTeX in handbook/figures/.
This script provides Python-based alternatives and supplementary plots.

Requirements: matplotlib, numpy
Usage: python3 generate_figures.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'figures')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Figure S1: Simulated pixel intensity histogram (H&E stain) ──────────────
def plot_he_histogram():
    """Simulate RGB pixel intensity distributions for an H&E-stained slide."""
    np.random.seed(42)
    n = 5000
    # Haematoxylin: high blue, low red
    r_hx = np.random.normal(180, 25, n)
    g_hx = np.random.normal(130, 20, n)
    b_hx = np.random.normal(210, 15, n)
    # Eosin: high red/pink, low blue
    r_eo = np.random.normal(230, 20, n)
    g_eo = np.random.normal(160, 25, n)
    b_eo = np.random.normal(180, 20, n)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, r, g, b, title in zip(
        axes,
        [r_hx, r_eo], [g_hx, g_eo], [b_hx, b_eo],
        ['Haematoxylin region', 'Eosin region']
    ):
        ax.hist(r.clip(0, 255), bins=40, alpha=0.6, color='red', label='R')
        ax.hist(g.clip(0, 255), bins=40, alpha=0.6, color='green', label='G')
        ax.hist(b.clip(0, 255), bins=40, alpha=0.6, color='blue', label='B')
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_xlabel('Pixel intensity (0–255)')
        ax.set_ylabel('Frequency')
        ax.legend()
        ax.set_xlim(0, 255)

    fig.suptitle('Simulated RGB Pixel Intensity Distributions in H&E Staining',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'figS1_he_histogram.pdf')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'Saved: {out}')


# ── Figure S2: Schematic learning curve (training vs validation loss) ────────
def plot_learning_curve():
    """Illustrative training and validation loss curves for a CNN."""
    epochs = np.arange(1, 51)
    train_loss = 1.2 * np.exp(-0.08 * epochs) + 0.05 + np.random.normal(0, 0.01, 50)
    val_loss   = 1.3 * np.exp(-0.06 * epochs) + 0.12 + np.random.normal(0, 0.02, 50)
    # Simulate slight overfitting after epoch 35
    val_loss[35:] += np.linspace(0, 0.08, 15)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(epochs, train_loss, label='Training loss', color='steelblue', lw=2)
    ax.plot(epochs, val_loss,   label='Validation loss', color='darkorange', lw=2, ls='--')
    ax.axvline(35, color='gray', ls=':', lw=1.5, label='Overfitting onset')
    ax.set_xlabel('Epoch', fontsize=12)
    ax.set_ylabel('Loss', fontsize=12)
    ax.set_title('Illustrative CNN Training and Validation Loss Curves', fontsize=13, fontweight='bold')
    ax.legend(fontsize=11)
    ax.set_ylim(0, 1.4)
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'figS2_learning_curve.pdf')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'Saved: {out}')


if __name__ == '__main__':
    plot_he_histogram()
    plot_learning_curve()
    print('All supplementary figures generated.')
