import numpy as np
import pandas as pd
import pytest

from src.evaluation import evaluate_predictions


def test_hand_checked_metrics_keep_never_predicted_classes():
    actual = pd.Series(['Normal', 'Normal', 'DoS', 'Probe', 'R2L', 'U2R'])
    result = evaluate_predictions(actual, np.array(['Normal'] * 6))
    assert result['accuracy'] == pytest.approx(1 / 3)
    assert result['f1_weighted'] == pytest.approx(1 / 6)
    assert result['f1_macro'] == pytest.approx(1 / 10)
    assert result['classification_report']['Normal']['precision'] == pytest.approx(1 / 3)
    assert result['classification_report']['Normal']['recall'] == 1
    for family in ['DoS', 'Probe', 'R2L', 'U2R']:
        assert result['classification_report'][family]['f1-score'] == 0
        assert result['classification_report'][family]['support'] == 1
    assert result['confusion_matrix'] == [[2, 0, 0, 0, 0], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0]]
    assert np.asarray(result['confusion_matrix']).sum() == 6
    assert np.isfinite([result[k] for k in ['accuracy', 'f1_weighted', 'f1_macro']]).all()


def test_unknown_family_is_rejected_before_confusion_matrix_can_drop_it():
    with pytest.raises(ValueError, match='famiglie'):
        evaluate_predictions(pd.Series(['Normal']), np.array(['new_family']))
