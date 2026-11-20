"""Mappatura esplicita attacco → famiglia; provenienza in docs/LABEL_MAPPING.md."""

import pandas as pd

FAMILY_ORDER = ('Normal', 'DoS', 'Probe', 'R2L', 'U2R')
ATTACK_GROUPS = {
    'Normal': ('normal',),
    'DoS': ('back', 'land', 'neptune', 'pod', 'smurf', 'teardrop',
            'apache2', 'mailbomb', 'processtable', 'udpstorm', 'worm'),
    'Probe': ('ipsweep', 'nmap', 'portsweep', 'satan', 'mscan', 'saint'),
    'R2L': ('ftp_write', 'guess_passwd', 'imap', 'multihop', 'phf', 'spy',
            'warezclient', 'warezmaster', 'httptunnel', 'named', 'sendmail',
            'snmpgetattack', 'snmpguess', 'xlock', 'xsnoop'),
    'U2R': ('buffer_overflow', 'loadmodule', 'perl', 'rootkit', 'ps', 'sqlattack', 'xterm'),
}
ATTACK_TO_FAMILY = {attack: family for family, attacks in ATTACK_GROUPS.items() for attack in attacks}


def attack_to_family(labels: pd.Series) -> pd.Series:
    """Preserva righe/indice; rifiuta etichette mancanti o non documentate.

    Nessuna normalizzazione implicita di maiuscole, spazi o punto finale:
    una variante inattesa deve essere esaminata, non assorbita silenziosamente.
    """
    unknown = labels.isna() | ~labels.isin(ATTACK_TO_FAMILY)
    if unknown.any():
        values = labels.loc[unknown].astype('string').fillna('<mancante>').unique().tolist()
        raise ValueError(f'Etichette non mappate: {values}')
    return labels.map(ATTACK_TO_FAMILY).rename('family')


# Convenzione del codice Divekar, commit 75b8f8b; audit in docs/AUTHOR_CODE_AUDIT.md.
# Copia separata: non modifica il mapping degli esperimenti storici.
AUTHOR_ATTACK_TO_FAMILY = {**ATTACK_TO_FAMILY, 'worm': 'R2L', 'httptunnel': 'U2R'}
