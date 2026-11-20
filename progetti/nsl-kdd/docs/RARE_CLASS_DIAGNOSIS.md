# Diagnosi U2R/R2L — T10 e T11

Misurata il 2 novembre 2026. [Notebook 05](../notebooks/05_rare_class_diagnosis.ipynb).
Nessun nuovo fit: sono state analizzate le predizioni esistenti delle profondità10/13/15
sui cinque seed 1–5 scelti dall'utente. Tutte le41 feature e le etichette originali conservate.

## Profilo delle classi rare nel training

KDDTrain+ comprende52 U2R e995 R2L. Le tipologie grezze e i conteggi sono:

| family | attack_label | training_records |
| --- | --- | --- |
| R2L | ftp_write | 8 |
| R2L | guess_passwd | 53 |
| R2L | imap | 11 |
| R2L | multihop | 7 |
| R2L | phf | 4 |
| R2L | spy | 2 |
| R2L | warezclient | 890 |
| R2L | warezmaster | 20 |
| U2R | buffer_overflow | 30 |
| U2R | loadmodule | 9 |
| U2R | perl | 3 |
| U2R | rootkit | 10 |

Ogni run contiene10 U2R in validation e42 nel train,199 R2L in validation e796 nel train.
Nelle cinque validation appaiono31 U2R distinti e668 R2L distinti;21 U2R e327 R2L non sono
mai stati valutati in validation in queste prove e non hanno un tasso d'errore osservato.

## Errori delle tipologie U2R a profondità15

Le apparizioni possono ripetere lo stesso record. Il denominatore è il numero effettivo
di apparizioni in validation, non il numero totale delle ripetizioni.

| attack_label | training_records | distinct_validation_records | errori/apparizioni | quota_errori |
| --- | --- | --- | --- | --- |
| buffer_overflow | 30 | 16 | 11/27 | 40.74% |
| loadmodule | 9 | 5 | 7/8 | 87.50% |
| perl | 3 | 2 | 0/2 | 0.00% |
| rootkit | 10 | 8 | 12/13 | 92.31% |

Fra i31 U2R distinti osservati a profondità15,18 sono sempre sbagliati nelle loro apparizioni
e13 sempre corretti. Questo descrive le predizioni del riferimento su queste prove, non
una proprietà intrinseca o una prova di etichette errate. `rootkit` e `loadmodule` sono
i gruppi con maggior frequenza d'errore; `perl` ha soltanto2 apparizioni, entrambe corrette:
non basta per concludere che quella tipologia sia risolta.

Le tabelle per record includono row_position, famiglia/attacco grezzo, profondità,
n_validation, n_errors, error_rate e conteggi predicted_*. I falsi positivi sono separati
per famiglia vera, tipologia grezza e famiglia prevista. Risultati dettagliati locali in
artifacts/rare_class_diagnosis/: record_diagnosis.csv, type_diagnosis.csv,
false_positive_types.csv, split_support.csv, evaluation_events.csv e never_validated.csv.

## Integrità del riferimento

I file04 correnti hanno cinque run valide1–5, ma i campi di matrici normalizzate medie/DS
e record distinti riportavano ancora la precedente elaborazione con dieci run. Sono stati
ricalcolati dalle predizioni reali e congelati in artifacts/rare_class_reference/.
Lo script pubblicabile scripts/freeze_validation_reference.py, eseguito dal passo0 del05,
ricrea lo snapshot senza fit e senza modificare results.json/predictions.npz originali.
Il risultato è idempotente; gli indici sono verificati contro train_test_split.

Test sintetici verificano denominatori diversi e separazione fra profondità. I conteggi
reali sono stati riconciliati con le matrici di ogni run e con il CSV originale.
Duplicati e overlap restano i limiti descritti in DATA_AUDIT.md; nessuna correzione di dati.
