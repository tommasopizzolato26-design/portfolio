from pathlib import Path

import pytest

from scripts.download_data import save_verified_file


# Git blob SHA-1 di b"test\n", valore noto e indipendente dall'implementazione.
TEST_BLOB = "9daeafb9864cf43055ae93beb0afd6c7d144bfa4"


def test_saves_verified_bytes_and_can_repeat(tmp_path: Path):
    destination = tmp_path / "sample.txt"

    save_verified_file(destination, b"test\n", TEST_BLOB)
    save_verified_file(destination, b"test\n", TEST_BLOB)

    assert destination.read_bytes() == b"test\n"


def test_rejects_unexpected_download_before_writing(tmp_path: Path):
    destination = tmp_path / "sample.txt"

    with pytest.raises(ValueError, match="integrità"):
        save_verified_file(destination, b"wrong\n", TEST_BLOB)

    assert not destination.exists()


def test_preserves_existing_different_file(tmp_path: Path):
    destination = tmp_path / "sample.txt"
    destination.write_bytes(b"local edit\n")

    with pytest.raises(FileExistsError):
        save_verified_file(destination, b"test\n", TEST_BLOB)

    assert destination.read_bytes() == b"local edit\n"
