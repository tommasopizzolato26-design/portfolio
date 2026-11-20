"""Congela e riconcilia le cinque prove del notebook04, senza addestrare modelli."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data import COLUMN_NAMES
from src.targets import ATTACK_TO_FAMILY, FAMILY_ORDER


def freeze_validation_reference(project_root: Path) -> dict:
    """Ricostruisce uno snapshot idempotente dagli indici e dalle predizioni reali.

    results.json e predictions.npz del notebook04 restano invariati. I seed1–5
    sono il protocollo scelto per questo blocco; un protocollo diverso va esplicitato.
    """
    original = project_root / 'artifacts/repeated_validation'
    target = project_root / 'artifacts/rare_class_reference'
    before = json.loads((original / 'results.json').read_text(encoding='utf-8'))
    if before['seeds'] != [1, 2, 3, 4, 5] or before['feature_count'] != 41:
        raise ValueError('Questo confronto richiede cinque prove con seed1–5 e41feature.')
    if before['family_order'] != list(FAMILY_ORDER):
        raise ValueError('Ordine delle famiglie diverso dal protocollo.')
    raw = project_root / before['source']
    if hashlib.sha256(raw.read_bytes()).hexdigest() != before['source_sha256']:
        raise ValueError('Hash del dataset diverso dalla sorgente delle predizioni.')
    labels = pd.read_csv(raw, header=None, names=COLUMN_NAMES, usecols=['attack_label'])['attack_label'].map(ATTACK_TO_FAMILY)
    if labels.isna().any():
        raise ValueError('Etichette mancanti o non mappate.')

    reference = copy.deepcopy(before)
    run_rows, class_rows, split_records, indices_seen = [], [], [], []
    counts_by_depth = {depth: [] for depth in before['depths']}
    normalized_by_depth = {depth: [] for depth in before['depths']}
    with np.load(original / 'predictions.npz', allow_pickle=False) as saved:
        for run, seed in enumerate(before['seeds'], start=1):
            train_idx, indices = train_test_split(np.arange(len(labels)), stratify=labels, test_size=0.2, random_state=seed)
            np.testing.assert_array_equal(indices, saved[f'run_{run:02d}_validation_indices'])
            truth = saved[f'run_{run:02d}_truth']
            np.testing.assert_array_equal(truth, labels.iloc[indices].to_numpy())
            indices_seen.append(indices)
            split_records.append({
                'run': run, 'seed': seed, 'train_rows': len(train_idx), 'validation_rows': len(indices),
                'train_indices_sha256': hashlib.sha256(train_idx.tobytes()).hexdigest(),
                'validation_indices_sha256': hashlib.sha256(indices.tobytes()).hexdigest(),
            })
            for depth in before['depths']:
                predicted = saved[f'run_{run:02d}_depth_{depth}']
                if not set(predicted).issubset(FAMILY_ORDER):
                    raise ValueError('Predizioni con famiglie non documentate.')
                report = classification_report(truth, predicted, labels=FAMILY_ORDER, output_dict=True, zero_division=0)
                counts = confusion_matrix(truth, predicted, labels=FAMILY_ORDER)
                counts_by_depth[depth].append(counts)
                normalized_by_depth[depth].append(counts / counts.sum(axis=1, keepdims=True))
                run_rows.append({
                    'run': run, 'seed': seed, 'max_depth': depth,
                    'accuracy': accuracy_score(truth, predicted),
                    'macro_f1': f1_score(truth, predicted, labels=FAMILY_ORDER, average='macro', zero_division=0),
                    'weighted_f1': f1_score(truth, predicted, labels=FAMILY_ORDER, average='weighted', zero_division=0),
                })
                for i, family in enumerate(FAMILY_ORDER):
                    support, correct = int(counts[i].sum()), int(counts[i, i])
                    class_rows.append({
                        'run': run, 'seed': seed, 'max_depth': depth, 'famiglia': family,
                        'support': support, 'corretti': correct, 'errori': support - correct,
                        'falsi_positivi': int(counts[:, i].sum() - correct),
                        'quota_errori': (support - correct) / support,
                        'precision': report[family]['precision'], 'recall': report[family]['recall'],
                        'f1': report[family]['f1-score'],
                    })

    reference['run_metrics'] = run_rows
    reference['class_metrics'] = class_rows
    reference['splits'] = split_records
    reference['confusion_counts_by_depth'] = {
        str(depth): [matrix.tolist() for matrix in values] for depth, values in counts_by_depth.items()
    }
    reference['normalized_confusion_mean'] = {
        str(depth): np.stack(values).mean(axis=0).tolist() for depth, values in normalized_by_depth.items()
    }
    reference['normalized_confusion_std'] = {
        str(depth): np.stack(values).std(axis=0, ddof=1).tolist() for depth, values in normalized_by_depth.items()
    }
    seen = np.unique(np.concatenate(indices_seen))
    reference['unique_validation_counts'] = {family: int(labels.iloc[seen].eq(family).sum()) for family in FAMILY_ORDER}
    reconciled = [key for key in ['run_metrics', 'class_metrics', 'splits', 'confusion_counts_by_depth',
                                  'normalized_confusion_mean', 'normalized_confusion_std', 'unique_validation_counts']
                  if reference[key] != before.get(key)]
    reference['reference_snapshot'] = {
        'source_results': 'artifacts/repeated_validation/results.json',
        'source_results_sha256': hashlib.sha256((original / 'results.json').read_bytes()).hexdigest(),
        'source_predictions_sha256': hashlib.sha256((original / 'predictions.npz').read_bytes()).hexdigest(),
        'reconciled_from_saved_predictions': reconciled, 'new_fits': 0,
    }
    target.mkdir(parents=True, exist_ok=True)
    (target / 'results.json').write_text(json.dumps(reference, indent=2), encoding='utf-8')
    shutil.copy2(original / 'predictions.npz', target / 'predictions.npz')
    pd.DataFrame(run_rows).to_csv(target / 'run_metrics.csv', index=False)
    pd.DataFrame(class_rows).to_csv(target / 'class_metrics.csv', index=False)
    return reference


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    snapshot = freeze_validation_reference(args.project_root)
    print('Snapshot rigenerato senza fit; seed:', snapshot['seeds'])
    print('Campi riconciliati:', snapshot['reference_snapshot']['reconciled_from_saved_predictions'])
