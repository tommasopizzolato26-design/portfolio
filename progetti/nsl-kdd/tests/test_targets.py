import pandas as pd
import pytest

from src.targets import attack_to_family


def test_mapping_preserves_rows_index_and_all_five_families():
    labels = pd.Series(['normal', 'neptune', 'ipsweep', 'guess_passwd', 'buffer_overflow'], index=[9, 8, 7, 6, 5])
    result = attack_to_family(labels)
    assert result.tolist() == ['Normal', 'DoS', 'Probe', 'R2L', 'U2R']
    assert result.index.tolist() == [9, 8, 7, 6, 5]


def test_test_only_labels_have_an_explicit_mapping():
    labels = pd.Series(['apache2', 'mailbomb', 'processtable', 'udpstorm', 'worm', 'mscan', 'saint', 'httptunnel', 'named', 'sendmail', 'snmpgetattack', 'snmpguess', 'xlock', 'xsnoop', 'ps', 'sqlattack', 'xterm'])
    assert attack_to_family(labels).tolist() == ['DoS'] * 5 + ['Probe'] * 2 + ['R2L'] * 7 + ['U2R'] * 3


@pytest.mark.parametrize('label', ['new_attack', None, 'normal.'])
def test_unmapped_or_missing_label_is_rejected(label):
    with pytest.raises(ValueError, match='Etichette'):
        attack_to_family(pd.Series(['normal', label]))
