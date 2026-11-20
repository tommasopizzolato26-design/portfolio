# Controllo qualità e scelte di cleaning

Misurato il 2 novembre 2026 sui CSV byte-identici ai TXT identificati in DATA_MANIFEST.json.
Riproduzione: sezione 7 del notebook 01; overlap interno nella sezione 5 del notebook 02.

| Controllo | KDDTrain+ | KDDTest+ |
|---|---:|---:|
| Righe | 125973 | 22544 |
| Colonne | 43 | 43 |
| Valori mancanti | 0 | 0 |
| Numeri non finiti (incl. difficulty) | 0 | 0 |
| Duplicati oltre la prima occorrenza, 43 colonne | 0 | 0 |
| Duplicati oltre la prima occorrenza, 41 feature | 16 | 57 |
| Colonne costanti | num_outbound_cmds | num_outbound_cmds |
| Record con su_attempted=2 | 59 | 2 |

Le etichette del train comprendono normal e 22 attacchi. Le 17 tipologie presenti solo nel test
sono documentate in LABEL_MAPPING.md. Per il test sono stati effettuati soltanto controlli
strutturali, di integrità e copertura: nessuna metrica o distribuzione usata per scegliere il modello.

## Esito: dati utilizzabili, valori originali conservati

- Nessuna imputazione: mancanti e non finiti assenti.
- Nessuna deduplicazione: non esistono duplicati completi; feature identiche possono avere label
  diverse. La loro eliminazione richiederebbe una regola ulteriore e cambierebbe il protocollo.
- `su_attempted` è descritto come indicatore nella specifica UCI, ma il valore 2 non è spiegato
  da quella descrizione. Non supponiamo che sia equivalente a 0 o 1: lo conserviamo.
- `num_outbound_cmds` è costante e resta tra le 41 feature: nessuna selezione aggiunta.
- Non cambiamo unità, nomi delle categorie o label; numeriche invariate, tre categoriche one-hot
  con vocabolario appreso soltanto nel train pertinente, dopo lo split.

## Overlap: un limite da rendere visibile

Tra train e test ufficiali esistono **610 record unici identici sulle 43 colonne** e **654 vettori
unici identici sulle sole 41 feature**. Sono intersezioni tra insiemi di chiavi uniche, non somme
di righe con molteplicità. Non modifichiamo gli split ufficiali e non usiamo questo controllo per tuning.

Lo split interno stratificato 80/20 ha indici disgiunti ma **6 vettori feature unici condivisi**;
tutti e 6 hanno attacchi discordanti fra le due parti. Indipendenza degli indici non significa
indipendenza delle feature. Manteniamo il protocollo concordato, senza pulizia a posteriori.
Una sensibilità con split per gruppi è un possibile esperimento futuro, separato da queste misure.

Il paper riporta 125972/22542 righe; questi file hanno 125973/22544. La causa non è accertata.
Non eliminiamo record per forzare la coincidenza e non dichiariamo una replica numerica esatta.
La pagina UNB descrive miglioramenti rispetto a KDD99, ma non certifica l’identità storica del mirror.

Fonti: [specifica UCI](https://kdd.ics.uci.edu/databases/kddcup99/task.html),
[NSL-KDD UNB](https://www.unb.ca/cic/datasets/nsl.html); provenienza dei file in DATA_SOURCE.md.
