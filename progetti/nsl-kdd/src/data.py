"""Schema e caricamento dei TXT/CSV NSL-KDD originali, senza header."""

import csv
from pathlib import Path

import pandas as pd

FEATURE_COLUMNS = (
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
    "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",
    "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations",
    "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login",
    "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate",
    "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate",
    "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
    "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate",
    "dst_host_rerror_rate", "dst_host_srv_rerror_rate",
)
CATEGORICAL_COLUMNS = ("protocol_type", "service", "flag")
COLUMN_NAMES = (*FEATURE_COLUMNS, "attack_label", "difficulty")


def load_nsl_kdd(path: Path) -> pd.DataFrame:
    """Legge tutti i record; rifiuta file vuoti e righe con larghezza errata.

    I nomi delle feature seguono kddcup.names (UCI). Le due colonne finali
    sono documentate da UNB; fonti complete in docs/DATA_SOURCE.md.
    Nessuna riga viene rimossa e nessuna trasformazione viene appresa.
    """
    row_count = 0
    with path.open(encoding="utf-8", newline="") as source:
        for row_count, row in enumerate(csv.reader(source), start=1):
            if len(row) != len(COLUMN_NAMES):
                raise ValueError(
                    f"Riga {row_count}: attese 43 colonne, trovate {len(row)}."
                )
    if row_count == 0:
        raise ValueError("Il file NSL-KDD è vuoto.")

    string_types = {column: "string" for column in (*CATEGORICAL_COLUMNS, "attack_label")}
    return pd.read_csv(path, header=None, names=COLUMN_NAMES, dtype=string_types)
