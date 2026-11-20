import numpy as np
import pandas as pd

from src.data import FEATURE_COLUMNS
from src.preprocessing import make_preprocessor, select_features


def sample_frame():
    frame = pd.DataFrame(0., index=range(4), columns=FEATURE_COLUMNS)
    frame['protocol_type'] = ['tcp'] * 4
    frame['service'] = ['http'] * 4
    frame['flag'] = ['SF'] * 4
    frame['src_bytes'] = [1., 2., 3., 4.]
    return frame


def test_labels_and_difficulty_never_enter_transformed_features():
    frame = sample_frame().assign(attack_label='normal', difficulty=21, family='Normal')
    X = select_features(frame)
    assert X.shape == (4, 41)
    assert not {'attack_label', 'difficulty', 'family'} & set(X.columns)
    transformer = make_preprocessor()
    expected = transformer.fit_transform(X)
    actual = transformer.transform(frame.assign(difficulty=-1000, attack_label='neptune'))
    np.testing.assert_array_equal(actual, expected)
    assert len(transformer.get_feature_names_out()) == 41


def test_validation_only_category_is_ignored_without_learning_it():
    X = sample_frame()
    transformer = make_preprocessor()
    transformer.fit(X.iloc[:3])
    validation = X.iloc[[3]].copy()
    validation['service'] = 'validation_only'
    encoded = transformer.transform(validation)
    encoder = transformer.named_transformers_['categorical']
    assert encoder.categories_[1].tolist() == ['http']
    assert encoded.shape == (1, 41)
    assert encoded[0, :3].tolist() == [1., 0., 1.]
    assert np.isfinite(encoded).all()
    assert encoded[0, 4] == 4.  # src_bytes: numerica conservata
