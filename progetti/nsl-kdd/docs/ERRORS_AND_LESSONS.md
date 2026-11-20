# Errori e lezioni apprese

Registriamo problemi reali che aiutano a capire metodo e qualità del lavoro. Un problema è chiuso solo dopo una verifica descritta; un esperimento fallito resta un risultato documentabile.

## E01 — Documentazione legata a un obiettivo superato

**Fase:** preparazione. **Stato:** documentazione riallineata.

Lo stato operativo e la proposta erano stati consolidati sul forecasting CESNET26. Il chiarimento successivo ha fissato NSL-KDD e classificazione. Continuare a leggere quelle note come istruzioni correnti avrebbe portato a usare modelli e metriche inadatti.

**Correzione:** introdotti un handoff breve e una sintesi del benchmark NSL-KDD; contrassegnati come superati o in pausa i precedenti documenti operativi CESNET. Nessun modello di forecasting era stato implementato o addestrato per questo progetto.

**Lezione:** prima di ogni ticket verificare dataset, task, protocollo e risultato atteso nella fonte di stato corrente. Gli aggiornamenti dell'utente prevalgono sulle proposte precedenti.

## Come aggiungere un errore

Per ogni nuovo caso indicare: sintomo osservato, causa verificata o ancora ipotizzata, impatto sui risultati, correzione, verifica eseguita e lezione. Se cambia il metodo, aggiornare anche le decisioni. Evitare log personali o trascrizioni della chat.

## E02 — Verifica avviata durante l'installazione

**Fase:** T01, 2 novembre 2026. **Stato:** risolto e verificato.

Una prima verifica degli import ha restituito ipykernel non trovato perché pip stava ancora installando le dipendenze. La verifica è stata avviata troppo presto; il fallimento non dimostrava un ambiente incompatibile. Nessun risultato sui dati è stato coinvolto.

**Correzione e verifica:** attesa l'uscita positiva di pip, poi ripetuti import, pip check e una cella nel kernel dell'ambiente: tutti riusciti. **Lezione:** completare l'installazione prima dei controlli dipendenti e non considerare il solo pip check una prova che tutti i pacchetti richiesti siano presenti.

## E03 — Predizioni object in un archivio NPZ

**Fase:** T09/revisione finale, 2 novembre 2026. **Stato:** corretto e verificato.

Le predizioni dell’albero da target pandas string avevano dtype object. np.savez le aveva conservate
come oggetti, impedendo la lettura con np.load e allow_pickle=False. Il confronto di riproducibilità
ha sollevato ValueError; il revisore aveva segnalato la stessa causa. Le metriche erano corrette.

**Correzione:** conversione esplicita in stringhe Unicode prima del salvataggio. Regression test
che esegue la cella reale del notebook: osservato fallire, poi passare; suite21pass. Ripetuti tutti
i notebook con kernel puliti: split, predizioni e metriche identici. **Lezione:** verificare il formato
effettivo degli artefatti consegnati, oltre alle metriche in memoria. Corretta anche la riga accuracy
nelle tabelle perclasse: rimossa per evitare un support fittizio; accuracy resta nel riepilogo.

## E04 — Statistiche e predizioni provenienti da run diversi

**Rilevato durante T10–T14,2novembre2026.** I file04 correnti contengono cinque prove
seed1–5 valide, ma matrici normalizzate medie/DS e unique_validation_counts non
coincidevano con le predizioni: conservavano i valori del precedente gruppo di dieci.
L'incoerenza è stata verificata ricalcolando dai NPZ; non sono state osservate le azioni
di esecuzione che l'hanno prodotta. Il controllo dei seed ha fermato il nuovo percorso prima dei fit.

**Correzione verificata:** scelta esplicita dell'utente di usare cinque prove; snapshot
separato ricostruito dalle predizioni reali e indici ricalcolati. Notebook04 e file
originali preservati. Lo script pubblico freeze_validation_reference.py viene eseguito
da05, è idempotente e non addestra; regressiontest con statistiche obsolete RED→GREEN.
Nei cinque split ci sono31U2R distinti, non43. Tutte le nuove medie sono ricalcolate e verificate.

**Lezione:** dopo cambi a seed o numero di run, eseguire il notebook dall'inizio con
kernel pulito; confrontare sempre metriche aggregate con predizioni e indici effettivi.
La revisione ha inoltre rilevato che lo snapshot locale andava reso rigenerabile da
checkout: il nuovo script e il passo0 del05 risolvono anche questa dipendenza implicita.


## E05 — Predizioni incompatibili con il JSON nel confronto

Sintomo riprodotto in review: un NPZ proveniente da un altro modello poteva
superare hash del dataset, seed, indici e target uguali. L'identità nel JSON non
verificava la coerenza delle predizioni con i conteggi dichiarati. I risultati
effettivi erano corretti e verificati indipendentemente: nessuna misura cambiata.

Correzione11/12/13: ricalcolare la CM per run e confrontarla con confusion_counts
(schema 2) o `confusion_counts_by_depth['15']` (schema 1), rifiutando incompatibilità.
Nove regressioni osservate fallire e poi passare; suite67verde. Confronti reali
rieseguiti senza fit,39file dei due nuovi modelli byte-identici e68vecchifileprotetti
invariati. È una verifica di coerenza delle metriche, non autenticità crittografica:
una diversa assegnazione che conserva esattamente tutti i conteggi non è distinta.


## E06 — Numero di foglie NumPy nel JSON (T31, 5 novembre 2026)

La prima esecuzione aveva terminato fit, predizioni, CSV e grafici; json.dumps
ha rifiutato np.int64 restituito da get_n_leaves. Riproduzione con albero sintetico
di due righe, test RED → GREEN e conversione esplicita int per profondità/foglie.
Suite76pass. Ripetizione tecnica completa stessa configurazione, predizioni
identiche. Due fit effettivi, una sola configurazione; nessuna media delle repliche.
Lezione: verificare la serializzazione dei metadati sklearn prima di esecuzioni
complete; il numero di fit del risultato non sostituisce il registro delle esecuzioni.
