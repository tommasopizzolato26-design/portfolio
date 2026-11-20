import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_recall_fscore_support
from sklearn.tree import DecisionTreeClassifier

ROOT = Path(__file__).resolve().parents[1]


def cell(tag):
    path = ROOT / 'notebooks/15_decision_tree_official_test.ipynb'
    assert path.exists(), 'Manca il notebook T31'
    notebook = json.loads(path.read_text(encoding='utf-8'))
    return next(''.join(c['source']) for c in notebook['cells'] if tag in c.get('metadata', {}).get('tags', []))


def test_metrics_include_never_predicted_class_and_false_positives():
    context = dict(np=np, pd=pd, accuracy_score=accuracy_score, confusion_matrix=confusion_matrix,
                   f1_score=f1_score, precision_recall_fscore_support=precision_recall_fscore_support,
                   FAMILY_ORDER=('Normal', 'DoS', 'Probe', 'R2L', 'U2R'),
                   y_test=np.array(['Normal', 'DoS', 'Probe', 'R2L', 'U2R', 'U2R']),
                   y_pred=np.array(['Normal', 'DoS', 'Probe', 'Normal', 'Normal', 'Normal']))
    exec(cell('metrics'), context)
    table = context['class_metrics'].set_index('family')
    assert table.loc['Normal', 'false_positives'] == 3
    assert table.loc['U2R', 'support'] == 2
    assert table.loc['U2R', 'recall'] == 0
    assert table.loc['U2R', 'error_rate'] == 1
    assert table.loc['Normal', 'precision'] == .25
    assert context['metrics']['accuracy'] == .5
    assert context['metrics']['macro_f1'] == pytest.approx(.48)
    np.testing.assert_allclose(context['cm_normalized'].sum(axis=1), 1)


def test_classifier_guard_rejects_changed_parameters_before_training():
    protocol = json.loads((ROOT / 'configs/official_test_v1.json').read_text())
    protocol['models']['decision_tree']['parameters']['max_depth'] = 3
    with pytest.raises(AssertionError, match='configurazione'):
        exec(cell('classifier'), {'DecisionTreeClassifier': DecisionTreeClassifier, 'protocol': protocol})


def test_classifier_guard_accepts_frozen_configuration_without_fitting():
    protocol = json.loads((ROOT / 'configs/official_test_v1.json').read_text())
    context = {'DecisionTreeClassifier': DecisionTreeClassifier, 'protocol': protocol}
    exec(cell('classifier'), context)
    assert context['model'].get_params() == protocol['models']['decision_tree']['parameters']
    assert not hasattr(context['model'], 'tree_')


def test_tree_metadata_is_json_serializable():
    import ast
    notebook = json.loads((ROOT / 'notebooks/15_decision_tree_official_test.ipynb').read_text(encoding='utf-8'))
    source = next(''.join(c['source']) for c in notebook['cells'] if c['cell_type'] == 'code' and "'actual_depth':" in ''.join(c['source']))
    tree = ast.parse(source)
    results = next(node.value for node in tree.body if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'results' for t in node.targets))
    metadata = ast.Dict(keys=[], values=[])
    for key, value in zip(results.keys, results.values):
        if key.value in ('actual_depth', 'leaves'):
            metadata.keys.append(key)
            metadata.values.append(value)
    model = DecisionTreeClassifier(random_state=1).fit([[0], [1]], ['Normal', 'DoS'])
    values = eval(compile(ast.fix_missing_locations(ast.Expression(metadata)), '<metadata>', 'eval'), {'model': model})
    assert json.loads(json.dumps(values)) == {'actual_depth': 1, 'leaves': 2}
