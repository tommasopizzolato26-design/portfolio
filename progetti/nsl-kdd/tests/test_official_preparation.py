import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.data import FEATURE_COLUMNS, CATEGORICAL_COLUMNS
from src.targets import ATTACK_TO_FAMILY

ROOT = Path(__file__).resolve().parents[1]


def cell(tag):
    path = ROOT / 'notebooks/14_official_test_preparation.ipynb'
    assert path.exists(), 'Manca il notebook di preparazione ufficiale'
    notebook = json.loads(path.read_text(encoding='utf-8'))
    return next(''.join(c['source']) for c in notebook['cells'] if tag in c.get('metadata', {}).get('tags', []))


def test_author_profile_preserves_historical_mapping():
    import src.targets as targets
    author = getattr(targets, 'AUTHOR_ATTACK_TO_FAMILY', None)
    assert author is not None, 'Manca il profilo autore separato'
    assert author is not ATTACK_TO_FAMILY
    assert set(author) == set(ATTACK_TO_FAMILY)
    assert {k for k in author if author[k] != ATTACK_TO_FAMILY[k]} == {'worm', 'httptunnel'}
    assert [author[k] for k in ['worm', 'httptunnel']] == ['R2L', 'U2R']
    assert [ATTACK_TO_FAMILY[k] for k in ['worm', 'httptunnel']] == ['DoS', 'R2L']


@pytest.mark.parametrize('bad_label', ['unseen_attack', None, 'normal.'])
def test_notebook_rejects_unmapped_targets(bad_label):
    context = {'train': pd.DataFrame({'attack_label': ['normal']}),
               'test': pd.DataFrame({'attack_label': [bad_label]}),
               'AUTHOR_ATTACK_TO_FAMILY': {'normal': 'Normal'}}
    with pytest.raises(ValueError, match='Etichette'):
        exec(cell('map_targets'), context)


def test_preprocessing_uses_train_only_and_excludes_targets():
    train = pd.DataFrame({c: ['a', 'b'] if c in CATEGORICAL_COLUMNS else [1., 3.] for c in FEATURE_COLUMNS})
    test = pd.DataFrame({c: ['new'] if c in CATEGORICAL_COLUMNS else [100.] for c in FEATURE_COLUMNS})
    train['attack_label'], test['attack_label'] = 'normal', 'worm'
    train['difficulty'], test['difficulty'] = 1, 999
    context = dict(train=train, test=test, FEATURE_COLUMNS=FEATURE_COLUMNS,
                   CATEGORICAL_COLUMNS=CATEGORICAL_COLUMNS, ColumnTransformer=ColumnTransformer,
                   OneHotEncoder=OneHotEncoder, StandardScaler=StandardScaler, np=np)
    exec(cell('select_features'), context)
    exec(cell('preprocess'), context)
    assert list(context['X_train']) == list(FEATURE_COLUMNS)
    scaled = context['scaled_preprocessor']
    np.testing.assert_allclose(scaled.named_transformers_['numeric'].mean_, 2)
    assert scaled.named_transformers_['numeric'].n_samples_seen_ == 2
    for categories in scaled.named_transformers_['categorical'].categories_:
        assert categories.tolist() == ['a', 'b']
    np.testing.assert_allclose(context['X_test_scaled'][0, -38:], 98)
    np.testing.assert_allclose(context['X_test_scaled'][0, :6], 0)
    np.testing.assert_allclose(context['X_test_tree'][0, -38:], 100)
