import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.data import FEATURE_COLUMNS, CATEGORICAL_COLUMNS

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['16_random_forest_official_test', '17_gaussian_nb_official_test',
         '18_svm_official_test', '19_neural_network_official_test', '20_kmeans_official_test']
IDS = ['random_forest_balanced', 'gaussian_naive_bayes', 'svm_rbf', 'neural_network', 'kmeans']

def cell(name, tag):
    path = ROOT / 'notebooks' / (name + '.ipynb')
    assert path.exists(), 'Manca il nuovo notebook'
    n = json.loads(path.read_text(encoding='utf-8'))
    return next(''.join(c['source']) for c in n['cells'] if tag in c.get('metadata', {}).get('tags', []))

@pytest.mark.parametrize('name,model_id', list(zip(NAMES, IDS)))
def test_frozen_model_parameters(name, model_id):
    protocol = json.loads((ROOT / 'configs/official_test_v1.json').read_text())
    ctx = dict(globals(), protocol=protocol)
    exec(cell(name, 'classifier'), ctx)
    actual = json.loads(json.dumps(ctx['model'].get_params()))
    assert actual == protocol['models'][model_id]['parameters']
    assert not hasattr(ctx['model'], 'n_features_in_')

@pytest.mark.parametrize('name', NAMES)
def test_preprocessor_ignores_test_statistics_and_targets(name):
    X_train = pd.DataFrame({c: ['a','b'] if c in CATEGORICAL_COLUMNS else [1.,3.] for c in FEATURE_COLUMNS})
    X_test = pd.DataFrame({c: ['new'] if c in CATEGORICAL_COLUMNS else [100.] for c in FEATURE_COLUMNS})
    X_train['difficulty'], X_test['difficulty'] = 0, 999
    X_train['attack_label'], X_test['attack_label'] = 'normal', 'worm'
    ctx = dict(globals(), X_train=X_train, X_test=X_test,
               numeric_columns=[c for c in FEATURE_COLUMNS if c not in CATEGORICAL_COLUMNS])
    exec(cell(name, 'preprocess'), ctx)
    assert ctx['X_test_encoded'].shape == (1,44)
    np.testing.assert_allclose(ctx['X_test_encoded'][0,:6], 0)
    expected = 100 if name.startswith('16_') else 98
    np.testing.assert_allclose(ctx['X_test_encoded'][0,6:], expected)

def test_cluster_votes_use_training_with_explicit_tie_and_empty_policy():
    ctx = dict(np=np, pd=pd, FAMILY_ORDER=('Normal','DoS','Probe','R2L','U2R'),
               train_clusters=np.array([0,0,1,1,1]),
               y_train=pd.Series(['Normal','DoS','DoS','DoS','Normal']), n_clusters=3)
    exec(cell('20_kmeans_official_test', 'cluster_mapping'), ctx)
    assert ctx['cluster_to_family'].tolist() == ['Normal','DoS','DoS']
    assert ctx['empty_clusters'] == [2]
    assert ctx['tied_clusters'] == [0]
