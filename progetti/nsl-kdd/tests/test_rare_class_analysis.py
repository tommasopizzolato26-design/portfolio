"""I notebook devono normalizzare le esposizioni e confrontare gli stessi record."""

import copy
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest


NOTEBOOKS = Path(__file__).parents[1] / 'notebooks'


def tagged_cell(notebook_name, tag):
    path = NOTEBOOKS / notebook_name
    assert path.exists(), f'Notebook non ancora implementato: {notebook_name}'
    notebook = json.loads(path.read_text(encoding='utf-8'))
    cells = [cell for cell in notebook['cells'] if tag in cell['metadata'].get('tags', [])]
    assert len(cells) == 1, f'Cella eseguibile richiesta: {tag}'
    return ''.join(cells[0]['source'])


def test_error_rate_uses_actual_validation_exposures_and_keeps_prediction_counts():
    # Usare /10 invece delle esposizioni reali romperebbe entrambi i risultati.
    events = pd.DataFrame({
        'max_depth': [15, 15, 15], 'row_position': [7, 7, 8], 'run': [1, 2, 1],
        'family': ['U2R'] * 3, 'attack_label': ['perl', 'perl', 'rootkit'],
        'predicted': ['Normal', 'U2R', 'Normal'], 'is_error': [True, False, True],
    })
    namespace = {'pd': pd, 'rare_events': events, 'FAMILY_ORDER': ('Normal', 'DoS', 'Probe', 'R2L', 'U2R')}
    exec(tagged_cell('05_rare_class_diagnosis.ipynb', 'record_error_rates'), namespace)
    rows = namespace['record_diagnosis'].set_index('row_position')
    assert rows.loc[7, ['n_validation', 'n_errors', 'error_rate']].tolist() == [2, 1, 0.5]
    assert rows.loc[8, ['n_validation', 'n_errors', 'error_rate']].tolist() == [1, 1, 1.0]
    assert rows.loc[7, ['predicted_Normal', 'predicted_U2R']].tolist() == [1, 1]


def test_error_rates_do_not_pool_different_depths_for_the_same_record():
    # Omettere max_depth dal raggruppamento nasconderebbe il cambiamento fra modelli.
    events = pd.DataFrame({
        'max_depth': [13, 15], 'row_position': [7, 7], 'run': [1, 1],
        'family': ['U2R', 'U2R'], 'attack_label': ['perl', 'perl'],
        'predicted': ['Normal', 'U2R'], 'is_error': [True, False],
    })
    namespace = {'pd': pd, 'rare_events': events, 'FAMILY_ORDER': ('Normal', 'DoS', 'Probe', 'R2L', 'U2R')}
    exec(tagged_cell('05_rare_class_diagnosis.ipynb', 'record_error_rates'), namespace)
    rows = namespace['record_diagnosis'].set_index('max_depth')
    assert rows.loc[13, 'error_rate'] == 1.0
    assert rows.loc[15, 'error_rate'] == 0.0


def comparison_inputs():
    meta = {'source_sha256': 'same-source', 'seeds': list(range(42, 52)),
            'feature_count': 41, 'family_order': ['Normal', 'DoS', 'Probe', 'R2L', 'U2R']}
    arrays = {}
    for run in range(1, 11):
        arrays[f'run_{run:02d}_validation_indices'] = np.array([5, 8])
        arrays[f'run_{run:02d}_truth'] = np.array(['Normal', 'U2R'])
    return {
        'np': np,
        'experiments': {name: copy.deepcopy(meta) for name in ['decision_tree', 'decision_tree_balanced']},
        'arrays_by_model': {name: copy.deepcopy(arrays) for name in ['decision_tree', 'decision_tree_balanced']},
        'reference_id': 'decision_tree',
    }


def test_comparison_rejects_same_sized_but_different_validation_records():
    namespace = comparison_inputs()
    namespace['arrays_by_model']['decision_tree_balanced']['run_01_validation_indices'] = np.array([8, 5])
    source = tagged_cell('08_model_comparison.ipynb', 'validate_paired_comparison')
    with pytest.raises(AssertionError):
        exec(source, namespace)


def test_comparison_rejects_mismatched_true_labels_on_identical_indices():
    namespace = comparison_inputs()
    namespace['arrays_by_model']['decision_tree_balanced']['run_01_truth'] = np.array(['Normal', 'R2L'])
    source = tagged_cell('08_model_comparison.ipynb', 'validate_paired_comparison')
    with pytest.raises(AssertionError):
        exec(source, namespace)


def test_comparison_accepts_matching_records_and_labels():
    namespace = comparison_inputs()
    exec(tagged_cell('08_model_comparison.ipynb', 'validate_paired_comparison'), namespace)
