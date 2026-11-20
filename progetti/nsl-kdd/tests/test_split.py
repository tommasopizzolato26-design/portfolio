import numpy as np
import pandas as pd
import pytest

from src.split import make_validation_split


def test_positional_split_is_disjoint_complete_stratified_and_repeatable():
    y = pd.Series(['Normal', 'DoS', 'Probe', 'R2L', 'U2R'] * 20, index=np.arange(100) + 1000)
    train, validation = make_validation_split(y)
    again = make_validation_split(y)
    np.testing.assert_array_equal(train, again[0])
    np.testing.assert_array_equal(validation, again[1])
    assert len(train) == 80 and len(validation) == 20
    assert set(train).isdisjoint(validation)
    assert sorted(np.r_[train, validation].tolist()) == list(range(100))
    assert y.iloc[train].value_counts().tolist() == [16] * 5
    assert y.iloc[validation].value_counts().tolist() == [4] * 5


def test_missing_family_is_rejected_instead_of_silent_four_class_experiment():
    with pytest.raises(ValueError, match='cinque famiglie'):
        make_validation_split(pd.Series(['Normal', 'DoS'] * 10))
