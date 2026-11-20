# Riprodurre gli esperimenti NSL-KDD

Con Python 3.11 su Windows, esegui questi comandi dalla cartella `progetti/nsl-kdd`:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m ipykernel install --prefix .venv --name nsl-kdd --display-name "Python (NSL-KDD)"
.\.venv\Scripts\python.exe scripts/download_data.py
```

Lo script verifica i file e li salva in `data/raw/`. Le predizioni vengono salvate in `artifacts/`. [Provenienza dei dati](../docs/DATA_SOURCE.md) · [Protocollo ufficiale](../docs/OFFICIAL_TEST_PROTOCOL.md).

Apri i notebook in VS Code con l’interprete di `.venv`. Il [notebook 01](01_data_exploration.ipynb) spiega le colonne del dataset.

| Notebook | Cosa produce |
|---|---|
| [14](14_official_test_preparation.ipynb) | Verifica i dati e la mappatura delle classi. |
| [15](15_decision_tree_official_test.ipynb) · [16](16_random_forest_official_test.ipynb) · [17](17_gaussian_nb_official_test.ipynb) · [18](18_svm_official_test.ipynb) · [19](19_neural_network_official_test.ipynb) · [20](20_kmeans_official_test.ipynb) | Addestrano e valutano Decision Tree, Random Forest, Gaussian Naive Bayes, SVM, MLP e K-Means. |
| [21](21_official_benchmark_comparison.ipynb) | Confronta i sei modelli con il benchmark di Divekar et al. |
| [22](22_seen_unseen_attacks.ipynb) · [23](23_rare_attack_subtypes.ipynb) · [24](24_false_alarm_diagnosis.ipynb) | Analizzano attacchi mai visti, classi rare e falsi allarmi. |
| [25](25_dlha_official_test.ipynb) | Reimplementa DLHA e lo confronta con il MLP del notebook 19. |

Per il solo confronto DLHA, dopo il download esegui il [19](19_neural_network_official_test.ipynb) e il [25](25_dlha_official_test.ipynb). Per replicare le condizioni delle esecuzioni originali imposta `OPENBLAS_NUM_THREADS=2` e `OMP_NUM_THREADS=2` prima di avviare il kernel.

Dopo il notebook 15 puoi eseguire tutti i test con `.\.venv\Scripts\python.exe -m pytest -q`.
