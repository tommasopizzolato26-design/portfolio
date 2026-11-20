"""Contratti scientifici: celle effettive, piccoli dati, nessun fit del benchmark."""
import json
import ast
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

NOTEBOOKS = Path(__file__).parents[1] / 'notebooks'
MODELS = ['11_neural_network.ipynb', '12_kmeans.ipynb']


def source(name, tag):
    path = NOTEBOOKS / name
    assert path.exists(), f'Manca {name}'
    cells = json.loads(path.read_text(encoding='utf-8'))['cells']
    found = [c for c in cells if tag in c['metadata'].get('tags', [])]
    assert len(found) == 1, tag
    return ''.join(found[0]['source'])


@pytest.mark.parametrize('name', MODELS)
@pytest.mark.parametrize('corruption', [None, 'indices', 'truth'])
def test_same_validation_records_before_training(name, corruption):
    code = source(name, 'paired_split_check')
    namespace = {'np': np, 'prepared_splits': [{'run': 1,
        'validation_indices': np.array([5, 2] if corruption != 'indices' else [2, 5]),
        'y_validation': pd.Series(['Normal', 'U2R' if corruption != 'truth' else 'R2L'])}],
        'reference_arrays': {'run_01_validation_indices': np.array([5, 2]),
                             'run_01_truth': np.array(['Normal', 'U2R'])}}
    if corruption:
        with pytest.raises(AssertionError):
            exec(code, namespace)
    else:
        exec(code, namespace)


@pytest.mark.parametrize('name', MODELS)
def test_never_predicted_rare_class_stays_in_metrics(name):
    code = source(name, 'evaluate_predictions')
    namespace = {'np': np, 'pd': pd, 'seeds': [1],
                 'FAMILY_ORDER': ['Normal', 'DoS', 'Probe', 'R2L', 'U2R'],
                 'prediction_arrays': {'run_01_truth': np.array(['Normal', 'DoS', 'Probe', 'R2L', 'U2R', 'U2R']),
                                       'run_01_predicted': np.array(['Normal'] * 6)}}
    exec(code, namespace)
    u2r = namespace['class_results'].set_index('famiglia').loc['U2R']
    assert u2r[['support', 'corretti', 'errori', 'falsi_positivi']].tolist() == [2, 0, 2, 0]
    assert u2r[['precision', 'recall', 'f1', 'quota_errori']].tolist() == [0, 0, 0, 1]
    assert namespace['normalized_matrices'][0][4, 0] == 1


def test_cluster_majority_uses_training_labels_with_explicit_ties_and_empty_cluster():
    code = source('12_kmeans.ipynb', 'cluster_vote')
    namespace = {'np': np, 'pd': pd, 'display': lambda *a: None,
                 'FAMILY_ORDER': ['Normal', 'DoS', 'Probe', 'R2L', 'U2R'],
                 'cluster_count': 4,
                 'training_assignments': {1: np.array([0, 0, 0, 1, 1, 2, 2, 2])},
                 'training_targets': {1: np.array(['Normal', 'Normal', 'U2R', 'DoS', 'Probe', 'R2L', 'R2L', 'R2L'])},
                 # Opposite validation answers must not change the frozen mapping.
                 'y_validation': pd.Series(['U2R'] * 8)}
    exec(code, namespace)
    assert namespace['cluster_to_family'][1].tolist() == ['Normal', 'DoS', 'R2L', 'R2L']
    assert namespace['cluster_vote_checks'][0]['tied_clusters'] == [1]
    assert namespace['cluster_vote_checks'][0]['empty_clusters'] == [3]
    assert namespace['cluster_vote_checks'][0]['unrepresented_families'] == ['Probe', 'U2R']
    np.testing.assert_array_equal(namespace['cluster_tables'][1].sum(axis=0), [2, 1, 1, 3, 1])


@pytest.mark.parametrize('name', MODELS)
@pytest.mark.parametrize('schema', [1, 2])
@pytest.mark.parametrize('corruption', [False, True])
def test_embedded_comparison_matches_predictions_to_recorded_counts(name, schema, corruption):
    tree = ast.parse(source(name, 'compare_saved_models'))
    assignments = [node for node in ast.walk(tree) if isinstance(node, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == 'recorded_counts' for t in node.targets)]
    checks = [node for node in ast.walk(tree) if isinstance(node, ast.If)
              and 'recorded_counts' in ast.unparse(node.test)]
    assert len(assignments) == len(checks) == 1, 'Manca il controllo di coerenza JSON/NPZ'
    code = compile(ast.Module(body=assignments + checks, type_ignores=[]), name, 'exec')
    expected = np.eye(5, dtype=int)
    actual = expected.copy()
    if corruption:
        actual[0, 0] -= 1
        actual[0, 1] += 1
    metadata = ({'schema_version': 2, 'confusion_counts': [expected.tolist()]} if schema == 2
                else {'confusion_counts_by_depth': {'15': [expected.tolist()]}})
    namespace = {'np': np, 'metadata': metadata, 'run': 1, 'compared_id': 'model', 'counts': actual}
    if corruption:
        with pytest.raises(ValueError):
            exec(code, namespace)
    else:
        exec(code, namespace)
