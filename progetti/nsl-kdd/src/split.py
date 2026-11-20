"""Un solo split stratificato del training ufficiale, con indici posizionali."""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from src.targets import FAMILY_ORDER


def make_validation_split(
    y: pd.Series, *, test_size: float = 0.2, random_state: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    """Restituisce posizioni per .iloc; non legge il test ufficiale."""
    if y.isna().any() or set(y.unique()) != set(FAMILY_ORDER):
        raise ValueError('Il target deve contenere esattamente le cinque famiglie.')
    train, validation = train_test_split(
        np.arange(len(y)), test_size=test_size, random_state=random_state, stratify=y,
    )
    if any(set(y.iloc[part]) != set(FAMILY_ORDER) for part in (train, validation)):
        raise ValueError('Lo split non conserva tutte le cinque famiglie.')
    return train, validation
