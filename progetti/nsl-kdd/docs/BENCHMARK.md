# Benchmark NSL-KDD: sintesi

Fonte: Divekar et al. (2018), *Benchmarking datasets for Anomaly-based Network Intrusion Detection: KDD CUP 99 alternatives*. [Articolo](https://ieeexplore.ieee.org/document/8586840), PDF pp. 3-6.

## Esperimento pertinente

Ogni record descrive una connessione con 41 caratteristiche. Le classi sono Normal, DoS, Probe, R2L e U2R. Il paper confronta sei classificatori con scikit-learn e include una variante NSL-SMOTE con training ricampionato. Il test viene mantenuto invariato. È un compito di classificazione tabellare.

Nel testo sono descritti encoding delle stringhe in interi, selezione mediante importanza Gini/MDI, standardizzazione e ricerca degli iperparametri con CV a cinque fold. Le liste complete di feature, griglie, configurazioni finali e seed non sono fornite. Le versioni dichiarate sono scikit-learn 0.18.1 e imbalanced-learn 0.2.1; usare librerie attuali richiederà di dichiarare gli adattamenti.

## Risultati pubblicati da confrontare

Weighted F1 in percentuale, **non risultati del nostro progetto**. Tabella IV: multiclasse; Tabella VII: binario.

| Modello | NSL-KDD, 5 classi | NSL-SMOTE, 5 classi | NSL-KDD, binario |
|---|---:|---:|---:|
| Gaussian Naive Bayes | 57 | 57 | 78 |
| SVM RBF | 74 | 71 | 82 |
| Decision Tree | 68 | 71 | 81 |
| Random Forest | 70 | 72 | 81 |
| Rete neurale | 71 | 70 | 81 |
| K-Means + voto | 68 | 65 | 83 |

Il confronto deve considerare anche F1/recall delle singole classi, soprattutto R2L e U2R: il weighted F1 può nascondere prestazioni scarse sulle minoranze. K-Means assegna le etichette dei cluster usando soltanto il training.

## Incognite da risolvere nel planning

- Definire quali colonne sopra sono nel primo traguardo: binario, multiclasse e ricampionamento sono esperimenti distinti.
- Il paper riporta 125.972 record train e 22.542 test; verificare i file effettivi, header e conteggi. Non eliminare righe per far coincidere i numeri.
- Il paper conserva 20 feature NSL-KDD, ma non le elenca: ricostruire il selettore oppure dichiarare un adattamento. Non sostituire MDI > 0 con top-20 senza spiegazione.
- Escludere target e difficulty level dagli input. Non interpretare l'ordine dei record come tempo.
- Scaler, selettore e SMOTE devono essere confinati al training di ciascun fold. Il paper non documenta tutti questi confini.
- Una replica numerica esatta non è garantita dal solo PDF. Concordare il significato di riproduzione e documentare le scelte mancanti.

## Dati

[Descrizione ufficiale UNB](https://www.unb.ca/cic/datasets/nsl.html). Disponibilità e provenienza dei file saranno verificate all'acquisizione. Registrare URL, versione, SHA-256, schema e distribuzione delle classi; non versionare i dati grezzi. Il testo NSL-KDD comprende anche un indicatore di difficoltà oltre alle 41 feature e all'etichetta.

## Aggiornamento T27 — codice autore verificato

Il 5 novembre 2026 è stato rintracciato e ispezionato il codice NSL del repository
autore. [Audit con riferimenti alle righe](AUTHOR_CODE_AUDIT.md) e
[manifest dei cinque sorgenti](AUTHOR_CODE_MANIFEST.json).
Le configurazioni esplicite chiariscono diverse incognite, senza certificare tutti
i parametri finali delle righe del paper. Lo snapshot usa MiniBatchKMeans;
main attiva selezione per varianza e avvia il binario. Il ramo multiclasse esegue
ricampionamento. Non coincide interamente con MDI/CV e condizioni descritte nel testo.
La convenzione autore differisce dalla mappa attuale per worm e httptunnel.
Il nostro notebook12 usa KMeans Lloyd: resta una baseline adattata, con scostamento
ora meglio identificato. T27 non modifica esperimenti né avvia il test ufficiale.
