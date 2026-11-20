"""Acquisisce una copia identificabile di NSL-KDD, senza modificare i record.

La pagina UNB e i limiti del mirror sono documentati in docs/DATA_SOURCE.md.
Eseguire con: python scripts/download_data.py
"""

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

REPOSITORY = "Jehuty4949/NSL_KDD"
COMMIT = "27bbbdf5c5cccf9970b8b6037a0f19dc09c5a0a9"
FILES = {
    "KDDTrain+.txt": "20002897492adc110190a10509aa694f26f7f308",
    "KDDTest+.txt": "b30e89605285a5ccd8cf8fd38dba72906c20d3dd",
}


def save_verified_file(path: Path, content: bytes, expected_blob: str) -> None:
    """Verifica il blob Git e conserva eventuali file locali differenti."""
    git_header = f"blob {len(content)}\0".encode("ascii")
    actual_blob = hashlib.sha1(git_header + content).hexdigest()
    if actual_blob != expected_blob:
        raise ValueError(f"Controllo di integrità fallito per {path.name}")

    if path.exists():
        if path.read_bytes() != content:
            raise FileExistsError(f"File locale diverso: {path.name}. Nessuna sovrascrittura.")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as destination:
        destination.write(content)


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    raw_directory = project_root / "data" / "raw"
    manifest = {
        "dataset": "NSL-KDD",
        "repository": f"https://github.com/{REPOSITORY}",
        "commit": COMMIT,
        "official_description": "https://www.unb.ca/cic/datasets/nsl.html",
        "citation": "Tavallaee et al., A Detailed Analysis of the KDD CUP 99 Data Set, CISDA 2009",
        "csv_format": "Byte-identical copy of the headerless TXT; 41 features, label, difficulty.",
        "files": [],
    }

    for name, expected_blob in FILES.items():
        url = f"https://raw.githubusercontent.com/{REPOSITORY}/{COMMIT}/{quote(name, safe='')}"
        original = raw_directory / name
        if original.exists():
            content = original.read_bytes()
        else:
            with urlopen(url, timeout=60) as response:
                content = response.read()

        save_verified_file(original, content, expected_blob)
        csv_copy = original.with_suffix(".csv")
        save_verified_file(csv_copy, content, expected_blob)
        manifest["files"].append(
            {
                "original": original.relative_to(project_root).as_posix(),
                "csv_copy": csv_copy.relative_to(project_root).as_posix(),
                "url": url,
                "acquired_utc": datetime.fromtimestamp(original.stat().st_mtime, UTC).isoformat(),
                "bytes": len(content),
                "git_blob_sha1": expected_blob,
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )
        print(f"Verificati {name} e {csv_copy.name}: {len(content):,} byte")

    serialized = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    (raw_directory / "manifest.json").write_text(serialized, encoding="utf-8")
    (project_root / "docs" / "DATA_MANIFEST.json").write_text(serialized, encoding="utf-8")
    print("Manifest locale e copia in docs/DATA_MANIFEST.json aggiornati.")


if __name__ == "__main__":
    main()
