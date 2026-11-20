import numpy as np
import pandas as pd

from src.data import FEATURE_COLUMNS
from src.model import make_first_model


def test_pipeline_learns_numeric_rule_and_predicts_unseen_service():
    X = pd.DataFrame(0., index=range(20), columns=FEATURE_COLUMNS)
    X['protocol_type'], X['service'], X['flag'] = 'tcp', 'http', 'SF'
    X['src_bytes'] = range(20)
    y = np.array(['Normal'] * 10 + ['DoS'] * 10)
    model = make_first_model()
    model.fit(X, y)
    np.testing.assert_array_equal(model.predict(X), y)
    unseen = X.iloc[[0, 19]].copy()
    unseen['service'] = 'unseen_service'
    assert model.predict(unseen).tolist() == ['Normal', 'DoS']
    assert model.named_steps['classifier'].max_depth == 10
    assert model.named_steps['classifier'].random_state == 42
