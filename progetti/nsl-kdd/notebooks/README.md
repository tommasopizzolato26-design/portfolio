# Notebook NSL-KDD

Apri [00 — Panoramica](00_project_overview.ipynb) per orientarti. Per riprodurre le misure, scarica i dati come indicato nel [README principale](../README.md) ed esegui con kernel Python (NSL-KDD) pulito.

## Test ufficiale

| Notebook | Contenuto |
|---|---|
| [14](14_official_test_preparation.ipynb) | Verifica il protocollo, gli input e la mappatura delle etichette. |
| [15](15_decision_tree_official_test.ipynb) | Decision Tree. |
| [16](16_random_forest_official_test.ipynb) | Random Forest. |
| [17](17_gaussian_nb_official_test.ipynb) | Gaussian Naive Bayes. |
| [18](18_svm_official_test.ipynb) | SVM RBF. |
| [19](19_neural_network_official_test.ipynb) | MLP. |
| [20](20_kmeans_official_test.ipynb) | K-Means con etichette dai dati di training. |
| [21](21_official_benchmark_comparison.ipynb) | Confronta le sei configurazioni e i risultati con Divekar et al. (2018). |
| [22](22_seen_unseen_attacks.ipynb) | Confronta tipi presenti e assenti nel training. |
| [23](23_rare_attack_subtypes.ipynb) | Mostra dove sbagliano i modelli sui sottotipi R2L e U2R. |
| [24](24_false_alarm_diagnosis.ipynb) | Analizza i falsi allarmi sul traffico normale. |
| [25](25_dlha_official_test.ipynb) | Reimplementa DLHA e confronta gli allarmi binari con il MLP del notebook 19. |

Esegui 14–20 per preparare il protocollo e generare le predizioni. I notebook 21–24 usano le predizioni dei sei modelli. Il 25 richiede soltanto i dati, il protocollo e le predizioni MLP prodotte dal 19. Per replicare le condizioni di esecuzione originali imposta `OPENBLAS_NUM_THREADS=2` e `OMP_NUM_THREADS=2` prima dell’avvio del kernel.

## Validation interna e storico

API originali pandas/sklearn visibili; da src/ soltanto costanti nei notebook 02–13.
Eseguire con kernel Python(NSL-KDD) pulito, nell'ordine pertinente:

| Notebook | Domanda |
|---|---|
|00_project_overview|Qual è il contesto del progetto?|
|01_data_exploration|Come leggere colonne, legenda e audit?|
|02_data_preparation|Quali input/encoding/target e quando apprendere il preprocessing?|
|03_first_model|Come confrontare baseline e alberi10/13/15 sullo stesso split?|
|04_repeated_validation|Quanto variano i risultati fra ripetizioni? La configurazione corrente è seed 1–5.|
|05_rare_class_diagnosis|Quali record e tipologie rare vengono sbagliati?|
|06_class_weight|Che cosa cambia pesando le classi nell'albero15?|
|07_random_forest|Come si comporta RF100 alberi15 balanced sugli stessi split?|
|08_model_comparison|Quali compromessi emergono fra i tre modelli?|

Il passo0 del05 rigenera un riferimento congelato dalle predizioni04, senza fit,
verificando gli indici e correggendo eventuali statistiche non ricalcolate. Occorrono
cinque prove1–5: è il protocollo corrente confermato.05e08 non addestrano;06e07 sì.
Fonte del confronto in docs/RARE_CLASS_COMPARISON.md. Esecuzioni/HTML locali in artifacts/.
Questi notebook valutano gli split interni di KDDTrain+.

## Nuovi modelli — un notebook per ciascuno

| Notebook | Domanda |
|---|---|
|09_gaussian_naive_bayes|Che risultati ottiene una baseline GaussianNB e quanti falsi allarmi produce?|
|10_svm_rbf|Come si comporta SVM RBF sugli stessi cinque split e rispetto ai quattro modelli precedenti?|

Eseguire prima09 e poi10. Ciascuno contiene input, preprocessing, training, predizione,
metriche e confronto, con API originali e codice esplicito. Entrambi addestrano cinque
volte; rileggere gli output salvati non richiede training. Numeriche standardizzate
train-only; nessun tuning. Servono gli artefatti04–07 esistenti, descritti sopra.
Risultati/limiti in [NB_SVM_RESULTS.md](../docs/NB_SVM_RESULTS.md).


## Copertura dei sei metodi

11_neural_network.ipynb (MLP100) →12_kmeans.ipynb (300cluster + voto training)
→13_benchmark_comparison.ipynb (zero fit). Stessi cinque split80/20 seed1–5.
Un modello per notebook, API originali e fasi distinte; cinque fit per nuovo modello.
MLP e K-Means completano i sei tipi di modello, senza esaurire il benchmark ufficiale.
Per una copia senza artefatti:04 →05 →06 →07 →09 →10 →11 →12 →13.
Con riferimenti già disponibili eseguire solo11,poi12,poi13 con kernel puliti.
Risultati, parametri, convergenza e limiti in [confronto completo](../docs/BENCHMARK_MODEL_COMPARISON.md).
