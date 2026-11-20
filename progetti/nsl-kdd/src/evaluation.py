"""Metriche confrontabili con ordine fisso e classi mai predette visibili."""

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

from src.targets import FAMILY_ORDER


def evaluate_predictions(y_true: pd.Series, y_pred: np.ndarray) -> dict:
    """Riporta sempre tutte le cinque classi, anche se prive di predizioni."""
    for values in (y_true, y_pred):
        if pd.isna(values).any() or not set(values).issubset(FAMILY_ORDER):
            raise ValueError('Sono ammesse soltanto le cinque famiglie documentate.')
    return {
        'accuracy': float(accuracy_score(y_true, y_pred)),
        'f1_weighted': float(f1_score(y_true, y_pred, labels=FAMILY_ORDER, average='weighted', zero_division=0)),
        'f1_macro': float(f1_score(y_true, y_pred, labels=FAMILY_ORDER, average='macro', zero_division=0)),
        'classification_report': classification_report(
            y_true, y_pred, labels=FAMILY_ORDER, output_dict=True, zero_division=0,
        ),
        'confusion_matrix': confusion_matrix(y_true, y_pred, labels=FAMILY_ORDER).tolist(),
    }
