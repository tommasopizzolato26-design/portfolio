import hashlib
import json
import shutil
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support, f1_score, accuracy_score

ROOT = Path(__file__).resolve().parents[1]

@pytest.mark.parametrize('tamper', ['counts', 'label_profile', 'parameters', 'truth'])
def test_comparison_rejects_inconsistent_artifacts(tmp_path, tamper):
    nbpath = ROOT / 'notebooks/21_official_benchmark_comparison.ipynb'
    assert nbpath.exists(), 'Manca il confronto ufficiale'
    n = json.loads(nbpath.read_text(encoding='utf-8'))
    source = next(''.join(c['source']) for c in n['cells'] if 'load_and_verify' in c.get('metadata',{}).get('tags',[]))
    folder = tmp_path / 'artifacts/decision_tree_official_test'
    folder.mkdir(parents=True)
    original = ROOT / 'artifacts/decision_tree_official_test'
    shutil.copy2(original / 'predictions.npz', folder / 'predictions.npz')
    r = json.loads((original / 'results.json').read_text(encoding='utf-8'))
    with np.load(original / 'predictions.npz', allow_pickle=False) as z:
        arrays = {k:z[k].copy() for k in z.files}
        expected_truth = z['truth'].copy()
    if tamper == 'counts': r['confusion_counts'][0][0] += 1
    if tamper == 'label_profile': r['label_profile'] = 'historical'
    if tamper == 'parameters': r['classifier_parameters']['max_depth'] = 3
    if tamper == 'truth':
        arrays['truth'][0] = 'U2R'
        np.savez_compressed(folder / 'predictions.npz', **arrays)
        r['predictions_sha256'] = hashlib.sha256((folder / 'predictions.npz').read_bytes()).hexdigest()
    (folder / 'results.json').write_text(json.dumps(r), encoding='utf-8')
    protocol_path = ROOT / 'configs/official_test_v1.json'
    ctx = dict(globals(), ROOT=tmp_path,
               protocol=json.loads(protocol_path.read_text()),
               protocol_hash=hashlib.sha256(protocol_path.read_bytes()).hexdigest(),
               expected_truth=expected_truth, FAMILY_ORDER=('Normal','DoS','Probe','R2L','U2R'),
               models={'decision_tree': ('Decision Tree','decision_tree_official_test')})
    with pytest.raises(AssertionError): exec(source,ctx)
