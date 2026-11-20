"""Il file consegnato deve essere rileggibile senza abilitare pickle."""
import json
from pathlib import Path

import numpy as np


def test_notebook_saves_prediction_strings_readable_without_pickle(tmp_path):
    notebook_path = Path(__file__).parents[1] / 'notebooks/03_first_model.ipynb'
    notebook = json.loads(notebook_path.read_text(encoding='utf-8'))
    saving_cell = next(cell for cell in notebook['cells'] if 'save_predictions' in cell['metadata'].get('tags', []))
    # Una Pipeline con target pandas string produce predizioni object.
    namespace = {
        'np': np, 'artifacts': tmp_path, 'validation_idx': np.array([3, 8]),
        'predictions': {'baseline': np.array(['Normal', 'Normal'], dtype=object),
                        'decision_tree': np.array(['Normal', 'DoS'], dtype=object)},
    }
    exec(''.join(saving_cell['source']), namespace)
    with np.load(tmp_path / 'first_model_predictions.npz', allow_pickle=False) as saved:
        assert saved['validation_indices'].tolist() == [3, 8]
        assert saved['baseline'].tolist() == ['Normal', 'Normal']
        assert saved['decision_tree'].tolist() == ['Normal', 'DoS']
