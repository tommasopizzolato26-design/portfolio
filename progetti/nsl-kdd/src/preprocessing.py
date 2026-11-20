"""Selezione esplicita degli input e definizione del solo encoding."""

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

from src.data import CATEGORICAL_COLUMNS, FEATURE_COLUMNS

NUMERIC_COLUMNS = tuple(c for c in FEATURE_COLUMNS if c not in CATEGORICAL_COLUMNS)


def select_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Conserva le 41 colonne originali nell'ordine dello schema, mai label/difficulty."""
    return frame.loc[:, list(FEATURE_COLUMNS)].copy()


def make_preprocessor() -> ColumnTransformer:
    """Definisce il trasformatore; nessun fit prima dello split.

    Numeriche esplicite, anziché remainder=passthrough, così un'eventuale
    colonna extra (target/difficulty) non può diventare un predittore.
    La matrice resta sparsa quando conviene; nessuna densificazione manuale.
    """
    return ColumnTransformer(
        [
            ('categorical', OneHotEncoder(handle_unknown='ignore'), list(CATEGORICAL_COLUMNS)),
            ('numeric', 'passthrough', list(NUMERIC_COLUMNS)),
        ],
        remainder='drop',
    )
