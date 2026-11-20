# Primo modello: risultati preliminari di validation

Misurati il 2 novembre 2026. Il test ufficiale **non è stato valutato**. Questi numeri non sono
confrontabili direttamente con Tabella IV di Divekar, che usa un altro insieme di valutazione.

## Protocollo fissato

KDDTrain+ completo, 125973 righe. Split stratificato 80/20, seed 42: **100778 train e 25195
validation**. Normal/DoS/Probe/R2L/U2R nel train: 53874/36741/9325/796/42; in validation:
13469/9186/2331/199/10. Gli stessi indici posizionali per entrambi i modelli sono salvati
localmente con hash sorgente in data/processed/validation_split.npz e .json.

41 feature, senza attack_label/family/difficulty. One-hot delle 3 categoriche con categorie
sconosciute ignorate; 38 numeriche invariate, fit solo train. Nessun scaling, SMOTE, selezione o tuning.
Baseline DummyClassifier(strategy="most_frequent"); albero DecisionTreeClassifier(max_depth=10,
random_state=42) in Pipeline. Altri parametri ai default registrati nel JSON locale.

| Modello | Accuracy | Weighted F1 | Macro F1 | Fit (s) | Predict (s) |
|---|---:|---:|---:|---:|---:|
| baseline | 0.534590 | 0.372460 | 0.139344 | 0.022597 | 0.000181 |
| decision_tree | 0.996547 | 0.996438 | 0.928445 | 0.923382 | 0.026069 |

Tempi della seconda esecuzione verificata, variabili con macchina e carico; non un confronto
di velocità ottimizzato. La baseline prevede sempre Normal: recall Normal=1, F1 Normal=0.696720;
precision, recall e F1 delle altre quattro famiglie sono 0. Le classi mai predette restano nel report,
con zero_division=0. Support, metriche complete e matrice baseline nel notebook 03 e nel JSON locale.

## Report per famiglia dell’albero

| Famiglia | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| Normal | 0.994897 | 0.998812 | 0.996851 | 13469 |
| DoS | 0.999238 | 0.999238 | 0.999238 | 9186 |
| Probe | 0.996553 | 0.992278 | 0.994411 | 2331 |
| R2L | 0.987342 | 0.783920 | 0.873950 | 199 |
| U2R | 0.875000 | 0.700000 | 0.777778 | 10 |

L’albero riconosce Normal, DoS e Probe con recall superiore a 0.99. Per R2L riconosce 156/199 e
ne confonde 43 con Normal. Per U2R riconosce 7/10: ogni caso vale 10 punti percentuali di recall,
quindi la stima è fragile. Macro F1 rende più visibile questa differenza rispetto al weighted F1.
Non abbiamo scelto un nuovo max_depth guardando questi risultati.

Matrice dell’albero: righe vere, colonne predette, ordine fisso.

| Vera / predetta | Normal | DoS | Probe | R2L | U2R |
|---|---:|---:|---:|---:|---:|
| Normal | 13453 | 6 | 7 | 2 | 1 |
| DoS | 6 | 9179 | 1 | 0 | 0 |
| Probe | 17 | 1 | 2313 | 0 | 0 |
| R2L | 43 | 0 | 0 | 156 | 0 |
| U2R | 3 | 0 | 0 | 0 | 7 |

## Riproducibilità e limiti

Python 3.11.9, numpy 2.4.6,
pandas 3.1.0, scikit-learn 1.9.1.
Dipendenze complete in requirements.txt. Notebook 01/02/03 eseguiti in ordine con kernel puliti,
timeout esplicito 180 secondi per cella, 0 errori; split, predizioni e metriche identici nella
ripetizione finale. I tempi sono esclusi da questo confronto. Suite: 21 test superati.

Gli artefatti locali first_model_results.json e first_model_predictions.npz contengono versioni,
parametri effettivi, tempi, metriche, matrici e predizioni. Le predizioni sono stringhe Unicode,
rileggibili con np.load(..., allow_pickle=False); nessun modello serializzato o dato grezzo pubblicato.

- Validazione casuale all’interno dello stesso training, con attacchi noti: non misura reti nuove,
  attacchi test-only o deriva temporale. I valori alti non dimostrano generalizzazione sul test.
- Sei vettori feature sono condivisi tra train/validation, tutti con label discordanti; overlap
  degli split ufficiali e duplicati sono dettagliati in DATA_AUDIT.md. Nessuna deduplica a posteriori.
- Conteggi diversi dal paper e identità storica del mirror non certificata direttamente da UNB.
- Quattro label test-only hanno convenzioni di famiglia ancora da confermare (LABEL_MAPPING.md).
  Non incidono su questa validation; chiarirle prima del confronto sul test ufficiale.
- I warning Windows/ZMQ già osservati riguardano il runtime del kernel; nessun errore di cella.

Prossimo traguardo da concordare: protocollo comune per gli altri metodi, quindi benchmark sul
test ufficiale e confronto metodologico con Divekar. Nessun nuovo esperimento o push automatico.

## Riferimento su un singolo split: profondità 10, 13 e 15

Richiesto il 2 novembre 2026. Tutte le **41 feature** conservate; rimosso dal notebook
il precedente punto 8 con 40 feature. Nessuna eliminazione di colonne in queste prove.
Stesso split, seed 42 e preprocessing appreso solo sul train; API pandas/sklearn originali
direttamente nel notebook. Il riferimento a profondità 10 conserva i risultati iniziali.

| Profondità | Foglie | Accuracy validation | Macro F1 validation | Errori R2L | Errori U2R |
|---|---:|---:|---:|---:|---:|
| 10 | 139 | 0.996547 | 0.928445 | 43/199 (21.61%) | 3/10 (30%) |
| 13 | 204 | 0.997380 | 0.922114 | 14/199 (7.04%) | 3/10 (30%) |
| 15 | 226 | 0.997579 | 0.944019 | 14/199 (7.04%) | 3/10 (30%) |

### Esito misurato sullo stesso split

- **R2L:** passando da 10 a 13/15, gli errori scendono da **43/199 (21,61%)**
  a **14/199 (7,04%)**. Questi errori sono classificati come Normal.
- **U2R:** restano **3/10 errori (30%)**, tutti classificati come Normal, a ogni profondità.
  Aumentare la profondità fino a 15 non risolve questi casi su questa validation.
- **Falsi positivi U2R:** profondità 13 prevede U2R per 11 record, di cui 7 corretti;
  profondità 10 e 15 lo prevedono per 8 record, di cui 7 corretti. La precision U2R
  è quindi **63,64%** a 13, contro **87,50%** a 10/15. Anche una quota visualizzata
  come 0,0% nella matrice normalizzata può contenere errori: consultare i conteggi.
- **Macro F1:** 0,928445 a 10; 0,922114 a 13; **0,944019 a 15**. L'accuracy
  sale da 99,6547% a 99,758% a profondità 15, ma non risolve il limite U2R.

Fra le tre prove, 15 ha il macro F1 più alto; non è ancora una scelta finale del modello.
I risultati sono ripetibili su questo split, con due kernel puliti, non una stima del test.

### Lettura dei grafici ed evidenze

Le tre confusion matrix normalizzano per famiglia vera, con la stessa scala 0–100%.
Il notebook riporta anche tutte le matrici con conteggi e precision/recall/F1 per famiglia.
La normalizzazione per riga rende visibili gli errori sulle classi rare; i falsi positivi
si valutano anche con precision e conteggi. Support U2R=10: ogni errore pesa 10 punti percentuali.

Il disegno usa l'albero completo a profondità 15, limitando la sola rappresentazione
ai primi tre livelli. Non viene addestrato né valutato un albero a profondità 3 o 5.
Per cambiare il disegno, impostare depth_to_plot a 10/13/15; plot_max_depth è solo la vista.

Notebook 03: 36 celle, due esecuzioni con kernel puliti e zero errori. Predizioni e metriche
delle tre profondità identiche nella ripetizione; matrici normalizzate verificate rispetto
ai conteggi. Predizioni NPZ Unicode rileggibili con allow_pickle=False. Suite: 21 test superati.
Nessun risultato sul test ufficiale, ricampionamento o ulteriore tuning automatico.

Artefatti locali aggiornati in artifacts/: tree_depth_results.json,
tree_depth_predictions.npz, tree_depth_comparison.csv/.png, tree_depth_class_metrics.csv,
tree_depth_confusion_matrices.png e decision_tree_demo.png. Il vecchio CSV con 40 feature
è stato rimosso dal percorso attivo; copia storica in .local/ ignorata da Git.

## Aggiornamento: dieci ripetizioni

Il confronto sopra descrive solo il seed 42. Su richiesta dell'utente è stata aggiunta
la verifica con dieci split e dieci seed diversi per ciascuna profondità. Le medie
ridimensionano il risultato U2R del singolo split e sono il nuovo riferimento per
discutere stabilità: [REPEATED_VALIDATION_RESULTS.md](REPEATED_VALIDATION_RESULTS.md).
