from pathlib import Path

import pandas as pd
import pytest

from src.data import load_nsl_kdd


def make_row(duration: int, label: str) -> str:
    # 41 feature: duration, tre stringhe e altre 37 numeriche; poi target/difficulty.
    fields = [str(duration), "tcp", "http", "SF", *(["0"] * 37), label, "21"]
    return ",".join(fields)


def test_preserves_first_record_and_column_roles(tmp_path: Path):
    source = tmp_path / "sample.csv"
    source.write_text(make_row(7, "normal") + "\n" + make_row(9, "neptune"))

    frame = load_nsl_kdd(source)

    assert frame.shape == (2, 43)
    assert frame["duration"].tolist() == [7, 9]
    assert frame["protocol_type"].tolist() == ["tcp", "tcp"]
    assert frame["attack_label"].tolist() == ["normal", "neptune"]
    assert frame["difficulty"].tolist() == [21, 21]
    assert pd.api.types.is_numeric_dtype(frame["src_bytes"])


@pytest.mark.parametrize("field_count", [42, 44])
def test_rejects_wrong_number_of_columns(tmp_path: Path, field_count: int):
    source = tmp_path / "bad.csv"
    source.write_text(",".join(["0"] * field_count))

    with pytest.raises(ValueError, match="Riga 1.*43"):
        load_nsl_kdd(source)


def test_rejects_short_record_after_valid_first_record(tmp_path: Path):
    source = tmp_path / "bad.csv"
    source.write_text(make_row(7, "normal") + "\n1,tcp,http\n")

    with pytest.raises(ValueError, match="Riga 2.*43"):
        load_nsl_kdd(source)


def test_rejects_empty_file(tmp_path: Path):
    source = tmp_path / "empty.csv"
    source.write_text("")

    with pytest.raises(ValueError, match="vuoto"):
        load_nsl_kdd(source)
