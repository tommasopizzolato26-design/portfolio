"""Primo albero fissato prima degli esperimenti, senza tuning."""

from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier

from src.preprocessing import make_preprocessor


def make_first_model() -> Pipeline:
    """Il fit della Pipeline apprende encoder e albero soltanto dal suo train."""
    return Pipeline([
        ('preprocessor', make_preprocessor()),
        ('classifier', DecisionTreeClassifier(max_depth=10, random_state=42)),
    ])
