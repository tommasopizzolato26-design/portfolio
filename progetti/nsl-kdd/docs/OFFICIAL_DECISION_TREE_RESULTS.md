# T31 — Decision Tree sul training completo e test ufficiale

Prova singola richiesta dall'utente. Notebook:
[15_decision_tree_official_test.ipynb](../notebooks/15_decision_tree_official_test.ipynb).
Protocollo congelato: [OFFICIAL_TEST_PROTOCOL.md](OFFICIAL_TEST_PROTOCOL.md).

125973 righe training, 22544 test, 41 feature originali (122 dopo one-hot),
profondità massima 15, seed 1, nessun peso di classe. Encoder appreso sul solo
training; numeriche originali. Target secondo il codice autore, nessuno split
aggiuntivo, tuning, ricampionamento o selezione di feature.

## Risultato misurato — 5 novembre 2026

Macro F1 **0.5099**, weighted F1 **0.7186**,
accuracy **75.96%**.

| Famiglia | Precision | Recall | Errore (1−recall) | Corretti/totale |
|---|---:|---:|---:|---:|
| Normal | 65.98% | 97.34% | 2.66% | 9453/9711 |
| DoS | 96.03% | 80.42% | 19.58% | 5998/7458 |
| Probe | 83.99% | 62.62% | 37.38% | 1516/2421 |
| R2L | 95.54% | 5.45% | 94.55% | 150/2754 |
| U2R | 87.50% | 3.50% | 96.50% | 7/200 |

Le difficoltà maggiori sono R2L e U2R: rispettivamente 2590 e 181 esempi vengono
classificati come Normal. La precision elevata delle poche predizioni R2L/U2R non
compensa il basso recall: la maggior parte di questi attacchi sfugge al modello.

Il precedente Decision Tree15 aveva macro F1 medio **0,8754** nei cinque holdout
interni; qui ottiene **0,5099** sul test ufficiale. Weighted F1 passa da **0,9973**
a **0,7186**; recall R2L da **93,47%** a **5,45%**, U2R da **40%** a **3,50%**.
Non sono prove sullo stesso insieme: cambiano campioni, distribuzione, attacchi
presenti, quantità di training e, nel test, il profilo di due label. Quindi non
possiamo attribuire il divario all'uso del 100% del training né misurare da questo
confronto il contributo di ciascuna causa.

La prova mostra un limite marcato su questo test. Non cambiamo automaticamente
profondità, feature o altri parametri. Gli altri cinque modelli restano da eseguire
solo dopo decisione dell'utente. Il test ufficiale è ora consultato: sviluppi
guidati dai suoi risultati andranno dichiarati esplorativi.

## Verifiche e riproducibilità

Il notebook completo parte da kernel pulito e termina senza errori, con due grafici
incorporati: confusion matrix e primi tre livelli dell'albero completo.
Albero misurato: profondità 15, 249 foglie.
Suite: **76 test superati**, quattro nuovi casi osservati RED → GREEN.
Ricalcolo indipendente con NumPy da tutte le 22544 predizioni: conteggi, recall,
precision, F1, accuracy, errori e falsi positivi concordano con gli artefatti.
Anche i valori storici sono ricalcolati dalle predizioni salvate, senza training.
Review indipendente: nessun rilievo importante; il salvataggio finale, ancora
in corso durante la review, è stato poi verificato con il ricalcolo e gli hash.
225 file preesistenti verificati invariati prima dell'aggiornamento documentale.
Nessun commit, push o pubblicazione.

**Registro delle esecuzioni:** una configurazione sperimentale, due fit completi
effettivi. Il primo aveva completato training e predizioni, ma il salvataggio JSON
si è interrotto perché il numero di foglie era un intero NumPy. Conversione esplicita
a int, test di regressione e riesecuzione completa: tutte le predizioni sono
identiche alla prima esecuzione. Non sono due prove indipendenti e non si calcola
una media. Il campo model_fits=1 in results.json descrive la singola esecuzione
riuscita, non il totale delle esecuzioni tecniche; execution_log.json registra entrambe.

Artefatti locali: artifacts/decision_tree_official_test/ con results.json,
predictions.npz (Unicode, lettura senza pickle), class_metrics.csv, confusion matrix
CSV/PNG e grafico albero. Hash di input, protocollo e predizioni nel riepilogo.

Ruling operativo: lavoro sul branch esistente senza commit base, senza creare un
worktree; file nuovi e manifesto hash mitigano il minore isolamento. Nessun
esperimento precedente sovrascritto. T32–T37 non avviati.
