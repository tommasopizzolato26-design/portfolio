"""Lo snapshot deve rigenerarsi dai file04 senza un nuovo addestramento."""

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from src.data import COLUMN_NAMES
from src.targets import FAMILY_ORDER


def test_snapshot_rebuilds_stale_statistics_idempotently_without_changing_inputs(tmp_path):
    script = Path(__file__).parents[1] / 'scripts/freeze_validation_reference.py'
    assert script.exists(), 'Manca il passaggio riproducibile di creazione dello snapshot'
    from scripts.freeze_validation_reference import freeze_validation_reference

    raw = tmp_path / 'data/raw/KDDTrain+.csv'
    raw.parent.mkdir(parents=True)
    rows = pd.DataFrame(0, index=range(100), columns=COLUMN_NAMES)
    rows['protocol_type'], rows['service'], rows['flag'] = 'tcp', 'http', 'SF'
    rows['attack_label'] = ['normal', 'neptune', 'ipsweep', 'guess_passwd', 'buffer_overflow'] * 20
    rows.to_csv(raw, index=False, header=False)
    y = pd.Series(list(FAMILY_ORDER) * 20)
    source = tmp_path / 'artifacts/repeated_validation'
    source.mkdir(parents=True)
    stale = {
        'source': 'data/raw/KDDTrain+.csv', 'source_sha256': hashlib.sha256(raw.read_bytes()).hexdigest(),
        'feature_count': 41, 'seeds': [1, 2, 3, 4, 5], 'depths': [15],
        'family_order': list(FAMILY_ORDER),
        'unique_validation_counts': {family: 0 for family in FAMILY_ORDER},
        'normalized_confusion_mean': {'15': np.zeros((5, 5)).tolist()},
    }
    (source / 'results.json').write_text(json.dumps(stale), encoding='utf-8')
    arrays = {}
    for run, seed in enumerate(stale['seeds'], 1):
        _, indices = train_test_split(np.arange(100), test_size=0.2, random_state=seed, stratify=y)
        truth = np.asarray(y.iloc[indices], dtype=str)
        predicted = truth.copy()
        predicted[predicted == 'U2R'] = 'Normal'
        arrays[f'run_{run:02d}_validation_indices'] = indices
        arrays[f'run_{run:02d}_truth'] = truth
        arrays[f'run_{run:02d}_depth_15'] = predicted
    np.savez_compressed(source / 'predictions.npz', **arrays)
    original = {name: (source / name).read_bytes() for name in ['results.json', 'predictions.npz']}

    freeze_validation_reference(tmp_path)
    target = tmp_path / 'artifacts/rare_class_reference'
    result_bytes = (target / 'results.json').read_bytes()
    result = json.loads(result_bytes)
    expected = np.eye(5)
    expected[4] = [1, 0, 0, 0, 0]
    np.testing.assert_array_equal(result['normalized_confusion_mean']['15'], expected)
    np.testing.assert_array_equal(result['normalized_confusion_std']['15'], np.zeros((5, 5)))
    assert result['unique_validation_counts']['U2R'] > 0
    assert result['reference_snapshot']['new_fits'] == 0
    with np.load(target / 'predictions.npz', allow_pickle=False) as saved:
        np.testing.assert_array_equal(saved['run_01_depth_15'], arrays['run_01_depth_15'])
    freeze_validation_reference(tmp_path)
    assert (target / 'results.json').read_bytes() == result_bytes
    for name, expected_bytes in original.items():
        assert (source / name).read_bytes() == expected_bytes
