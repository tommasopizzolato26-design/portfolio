"""Confronto end-to-end delle predizioni, senza fit e senza dati esterni."""
import json
from pathlib import Path

import numpy as np
import pytest
from sklearn.metrics import confusion_matrix

from test_nn_kmeans_notebooks import source


@pytest.mark.parametrize('corruption', [None, 'schema', 'identity', 'indices', 'truth', 'source', 'split', 'label', 'prediction'])
def test_full_comparison_requires_matching_provenance_and_records(tmp_path, corruption):
    code = source('13_benchmark_comparison.ipynb', 'load_paired_predictions')
    families = ['Normal', 'DoS', 'Probe', 'R2L', 'U2R']
    reference = {'source_sha256': 'known_hash', 'seeds': [1], 'validation_size': .2,
                 'feature_count': 41, 'family_order': families, 'splits': [{'seed': 1, 'train_size': 20, 'validation_size': 5}]}
    metadata = {**reference, 'schema_version': 2, 'model_id': 'neural_network',
                'confusion_counts': [np.eye(5, dtype=int).tolist()]}
    arrays = {'run_01_validation_indices': np.arange(5), 'run_01_truth': np.array(families),
              'run_01_predicted': np.array(families)}
    if corruption == 'schema': metadata['schema_version'] = 999
    if corruption == 'identity': metadata['model_id'] = 'svm_rbf'
    if corruption == 'source': metadata['source_sha256'] = 'wrong_hash'
    if corruption == 'split': metadata['validation_size'] = .3
    if corruption == 'indices': arrays['run_01_validation_indices'] = np.arange(4, -1, -1)
    if corruption == 'truth': arrays['run_01_truth'] = np.array(families[::-1])
    if corruption == 'label': arrays['run_01_predicted'][0] = 'Other'
    if corruption == 'prediction': arrays['run_01_predicted'][0] = 'DoS'
    folder = tmp_path / 'artifacts/neural_network'
    folder.mkdir(parents=True)
    (folder / 'results.json').write_text(json.dumps(metadata))
    np.savez_compressed(folder / 'predictions.npz', **arrays)
    namespace = {'np': np, 'json': json, 'confusion_matrix': confusion_matrix, 'project_root': tmp_path,
        'saved_models': {'neural_network': 'neural_network'}, 'reference': reference,
        'source_sha256': 'known_hash', 'seeds': [1], 'FAMILY_ORDER': families,
        'reference_arrays': {'run_01_validation_indices': np.arange(5), 'run_01_truth': np.array(families)}}
    if corruption:
        with pytest.raises(ValueError):
            exec(code, namespace)
    else:
        exec(code, namespace)
        np.testing.assert_array_equal(namespace['paired_predictions']['neural_network'][1]['predicted'], families)
