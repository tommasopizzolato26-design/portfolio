"""Contratti scientifici dei nuovi notebook, senza ripetere i fit sperimentali."""
import ast
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest


NOTEBOOKS = Path(__file__).parents[1] / 'notebooks'
MODELS = ['09_gaussian_naive_bayes.ipynb', '10_svm_rbf.ipynb']


def cell_source(name, tag):
    path = NOTEBOOKS / name
    assert path.exists(), f'Notebook non ancora implementato: {name}'
    cells = json.loads(path.read_text(encoding='utf-8'))['cells']
    matching = [c for c in cells if tag in c['metadata'].get('tags', [])]
    assert len(matching) == 1, f'Cella richiesta: {tag}'
    return ''.join(matching[0]['source'])


@pytest.mark.parametrize('name', MODELS)
@pytest.mark.parametrize('mismatch', ['indices', 'truth', None])
def test_fit_guard_requires_the_same_validation_records_and_labels(name, mismatch):
    # Saltare il controllo consentirebbe un confronto abbinato scientificamente falso.
    source = cell_source(name, 'paired_split_check')
    saved = {'run_01_validation_indices': np.array([8, 3]),
             'run_01_truth': np.array(['Normal', 'U2R'])}
    namespace = {'np': np, 'run': 1, 'reference_arrays': saved,
                 'validation_indices': np.array([8, 3]),
                 'y_validation': pd.Series(['Normal', 'U2R'])}
    if mismatch == 'indices':
        namespace['validation_indices'] = np.array([3, 8])
    if mismatch == 'truth':
        namespace['y_validation'] = pd.Series(['Normal', 'R2L'])
    namespace['prepared_splits'] = [{'run': 1,
                                    'validation_indices': namespace['validation_indices'],
                                    'y_validation': namespace['y_validation']}]
    if mismatch:
        with pytest.raises(AssertionError):
            exec(source, namespace)
    else:
        exec(source, namespace)


@pytest.mark.parametrize('name', MODELS)
def test_evaluation_counts_a_rare_class_that_is_never_predicted(name):
    # Eliminare U2R dalle label, confondere FP/FN o dividere per tutti i record rompe il contratto.
    families = ['Normal', 'DoS', 'Probe', 'R2L', 'U2R']
    namespace = {'np': np, 'pd': pd, 'seeds': [1], 'FAMILY_ORDER': families,
                 'prediction_arrays': {
                     'run_01_truth': np.array(['Normal', 'Normal', 'DoS', 'Probe', 'R2L', 'U2R', 'U2R']),
                     'run_01_predicted': np.array(['Normal'] * 7)}}
    exec(cell_source(name, 'evaluate_predictions'), namespace)
    u2r = namespace['class_results'].set_index('famiglia').loc['U2R']
    assert u2r[['support', 'corretti', 'errori', 'falsi_positivi']].tolist() == [2, 0, 2, 0]
    assert u2r[['precision', 'recall', 'f1', 'quota_errori']].tolist() == [0, 0, 0, 1]
    normal = namespace['class_results'].set_index('famiglia').loc['Normal']
    assert normal['falsi_positivi'] == 5
    assert normal['precision'] == pytest.approx(2 / 7)
    assert namespace['run_results'].iloc[0]['macro_f1'] == pytest.approx(4 / 45)
    assert namespace['normalized_matrices'][0][4, 0] == 1
    assert namespace['normalized_matrices'][0][0, 0] == 1


@pytest.mark.parametrize('name', MODELS)
@pytest.mark.parametrize('corruption', ['schema', 'identity', None])
def test_saved_comparison_rejects_unknown_schema_or_mislabeled_model(name, corruption):
    # Un NPZ valido di un altro modello non deve essere mostrato sotto il nome atteso.
    tree = ast.parse(cell_source(name, 'compare_saved_models'))
    artifact_loop = next(node for node in tree.body if isinstance(node, ast.For))
    checks = [node for node in artifact_loop.body if isinstance(node, ast.If)]
    assert len(checks) == 2, 'Mancano i controlli di schema e identità degli artefatti.'
    source = compile(ast.Module(body=checks, type_ignores=[]), name, 'exec')
    model_id = 'gaussian_naive_bayes' if name.startswith('09') else 'svm_rbf'
    metadata = {'schema_version': 99 if corruption == 'schema' else 2,
                'model_id': 'another_model' if corruption == 'identity' else model_id}
    namespace = {'metadata': metadata, 'compared_id': model_id}
    if corruption:
        with pytest.raises(ValueError):
            exec(source, namespace)
    else:
        exec(source, namespace)
