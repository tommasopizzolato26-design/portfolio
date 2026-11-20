# Confronto sulle classi rare — T12–T14

Misurato il 2 novembre 2026. [Notebook 08](../notebooks/08_model_comparison.ipynb).

## Protocollo concordato

- Cinque split stratificati80/20, seed 1–5, dal solo KDDTrain+;100778train/25195validation.
  Stessi indici e risposte per tutti i modelli dentro ogni run.
- Tutte41 feature; tre categoriche one-hot e38numeriche invariate. Encoder e pesi appresi
  soltanto dal train pertinente. API pandas/sklearn originali visibili nei notebook.
- Riferimento: DecisionTreeClassifier(max_depth=15,class_weight=None), predizioni esistenti,
  zero nuovi fit. Snapshot riconciliato dalle predizioni reali, con provenienza e hash.
- Variante1: DecisionTreeClassifier(max_depth=15,class_weight="balanced"),5 fit.
- Variante2: RandomForestClassifier(n_estimators=100,max_depth=15,class_weight="balanced",
  max_features="sqrt",bootstrap=True,n_jobs=2),5 fit. random_state=seed per ogni modello.
- Parametri restanti ai default di sklearn1.9.1 registrati per seed. Nessun'altra configurazione
  tentata, feature eliminata, SMOTE o test ufficiale valutato.
- Criterio Q1: precision/recall/falsi positivi e variabilità letti insieme; il solo macro F1
  non sceglie automaticamente un vincitore.

## Esito misurato sulle cinque prove concordate

Stessi seed 1–5 e stessi record di validation per i tre modelli. Le medie delle
metriche sono calcolate per run; DS è la deviazione standard campionaria fra le cinque prove.

| Modello | Precision U2R media | Recall U2R medio | FP U2R medi/run | Macro F1 media ± DS |
|---|---:|---:|---:|---:|
| Albero15 senza pesi | 49.62% | 40.00% | 3.2 | 0.875387 ± 0.055038 |
| Albero15 balanced | 24.42% | 58.00% | 24.2 | 0.810615 ± 0.037510 |
| Random Forest balanced | 78.34% | 60.00% | 2.2 | 0.920033 ± 0.031215 |

L'albero pesato aumenta il recall U2R, ma i falsi positivi medi salgono da 3,2 a 24,2
per run e la precision scende al 24,42%. Il macro F1 diminuisce: su queste prove il
compromesso è sfavorevole rispetto al riferimento.

La Random Forest migliora contemporaneamente precision e recall U2R medi e riduce
i falsi positivi medi a 2,2. Il macro F1 sale a 0,920033; è il candidato più promettente
di questo confronto. **U2R resta difficile:** errore medio 40%, con singole prove dal20%
al70%; DS del recall 21,21 punti percentuali. Non è una promozione automatica a modello finale.

Per R2L la Random Forest raggiunge recall medio 97,09% e precision 94,83%, contro
93,47%/95,98% del riferimento: recupera più casi, con un piccolo calo della precision.
L'albero pesato ha recall 96,28% ma precision 60,02%, con137,6 falsi positivi medi/run.

Le cinque validation contengono 31 U2R distinti riutilizzati fra run. Non sono campioni
indipendenti; non attribuiamo significatività statistica alle sole medie e non misuriamo
prestazioni sul test ufficiale. La pesatura e l'ensemble sono varianti di sviluppo nostre.

## Dispersione e altre famiglie

| Modello | Precision U2R media ± DS | Recall U2R medio ± DS | Recall R2L medio | Precision R2L media |
|---|---:|---:|---:|---:|
| Albero15 senza pesi | 49.62% ± 28.88pp | 40.00% ± 25.50pp | 93.47% | 95.98% |
| Albero15 balanced | 24.42% ± 14.64pp | 58.00% ± 19.24pp | 96.28% | 60.02% |
| Random Forest balanced | 78.34% ± 18.95pp | 60.00% ± 21.21pp | 97.09% | 94.83% |

Il report nel notebook comprende tutte le famiglie. Per confronto aggregato:

| Modello | Accuracy media ± DS | Weighted F1 medio ± DS |
|---|---:|---:|
| Albero15 senza pesi | 0.997325 ± 0.000387 | 0.997279 ± 0.000433 |
| Albero15 balanced | 0.991927 ± 0.002930 | 0.992980 ± 0.002246 |
| Random Forest balanced | 0.998262 ± 0.000252 | 0.998248 ± 0.000243 |

DS è campionaria, ddof=1; non è errore standard o intervallo di confidenza. Precision/F1
vengono calcolati per run e poi mediati, non ricavati dalle matrici medie. Le differenze
fra variante e riferimento sono abbinate per seed e famiglia, con media/DS/min/max;
non vengono usate per una dichiarazione di significatività su split sovrapposti.

## Riproduzione e verifiche

Eseguire il notebook 04 con i cinque seed 1–5 correnti, poi05→06→07→08 da kernel pulito.
Il passo0 del05 rigenera artifacts/rare_class_reference/ tramite uno script del progetto,
senza fit. Ripetere06/07 ripete gli addestramenti;05/08 analizzano soltanto risultati salvati.

Sono stati eseguiti esattamente10nuovi fit, nessun nuovo fit del riferimento. Verificati
tutti gli indici, le risposte, i pesi per train e le categorie apprese, le metriche e
le matrici dai file delle predizioni. Media/DS/min/max e differenze abbinate ricalcolate
indipendentemente. NPZ Unicode leggibili con allow_pickle=False.

Suite27 test passati:5nuovi controlli su denominatori/abbinamento e1regressione sullo snapshot,
osservati fallire prima della funzionalità e passare dopo. Revisione indipendente: nessun
errore scientifico rilevato. Risolto il rilievo importante sulla rigenerazione dello snapshot;
precisata anche la descrizione dei limiti nei JSON delle varianti a una sola profondità.
Notebook 05/08 rieseguiti senza fit dopo la correzione; non riaddestrate le varianti.
Notebook 00–04 e results.json/predictions.npz originali verificati immutati con SHA-256.

## Dove leggere

- Notebook 05: profilo e diagnosi;06: albero pesato;07: Random Forest;08: confronto.
- RARE_CLASS_DIAGNOSIS.md: tipologie, esposizioni e limiti dei conteggi.
- artifacts/decision_tree_balanced/ e random_forest_balanced/: parametri, pesi, metriche,
  categorie apprese e predizioni per tutte le cinque run, inclusi esiti sfavorevoli.
- artifacts/rare_class_comparison/: CSV individuali e riepiloghi, paired_deltas.csv,
  mean_confusion_matrices.png; HTML locali05–08 in artifacts/.
- .local/classi-rare/: log, verifiche, hash e decisioni operative; cartella esclusa da Git.

## Prossimo passo proposto, non eseguito

Conservare la Random Forest come candidato e discutere il limite U2R prima di altre prove.
Le cinque ripetizioni permettono un confronto, ma non dimostrano generalizzazione. Prima
del benchmark finale restano da fissare protocollo comune agli altri metodi e mapping delle
label test-only. Questa variante pesata non è la replica dei parametri del paper.
Nessun altro tuning, test ufficiale, commit o pubblicazione avviato automaticamente.
