# Provenienza dei dati NSL-KDD

Consultazione e acquisizione: 2 novembre 2026. Fonte adottata per questa prova: mirror pubblico, non download diretto dai curatori.

## Fonte primaria e condizioni d'uso

La [pagina UNB](https://www.unb.ca/cic/datasets/nsl.html) descrive KDDTrain+.TXT e KDDTest+.TXT come file in formato CSV con tipo di attacco e difficulty level. Alla consultazione dichiara che il dataset non è più disponibile sul sito.

La stessa pagina permette uso, redistribuzione e mirroring richiedendo la citazione di NSL-KDD e di M. Tavallaee, E. Bagheri, W. Lu e A. Ghorbani, *A Detailed Analysis of the KDD CUP 99 Data Set*, CISDA 2009 ([riferimento IEEE](https://ieeexplore.ieee.org/document/5356528)). Queste condizioni riguardano il dataset; non determinano la licenza del nostro codice o del codice di terzi.

## Mirror fissato

- Repository: [Jehuty4949/NSL_KDD](https://github.com/Jehuty4949/NSL_KDD), raggiunto anche dal precedente indirizzo defcom17/NSL_KDD.
- Commit: [27bbbdf5c5cccf9970b8b6037a0f19dc09c5a0a9](https://github.com/Jehuty4949/NSL_KDD/commit/27bbbdf5c5cccf9970b8b6037a0f19dc09c5a0a9), 30 luglio 2015.
- File adottati: i due TXT completi. Non usiamo i CSV già riformattati dal mirror, il subset al 20% o KDDTest-21.
- Blob Git attesi: train `20002897492adc110190a10509aa694f26f7f308`; test `b30e89605285a5ccd8cf8fd38dba72906c20d3dd`, letti dai metadati del commit.

Il mirror dichiara di includere anche un archivio originale, ma in questa prova non ne abbiamo autenticato la provenienza contro un download storico UNB. Fissare commit e hash rende identificabile la copia usata; non certifica che sia il file preciso usato da Divekar.

## File locali e CSV richiesto

`scripts/download_data.py` verifica i blob e salva gli originali in `data/raw/`. Crea quindi KDDTrain+.csv e KDDTest+.csv come copie **identiche byte per byte** dei TXT: nessun header aggiunto, nessuna riga eliminata e nessun tipo convertito. L'estensione cambia; il contenuto era già separato da virgole.

Il comando registra URL completo fissato al commit, data di acquisizione, dimensione e SHA-256 in `data/raw/manifest.json` e nella copia pubblicabile [DATA_MANIFEST.json](DATA_MANIFEST.json). I percorsi del manifest sono relativi al progetto. Un file locale diverso non viene sovrascritto.

## Schema

Nomi e ordine delle 41 feature derivano dalla [specifica originale UCI KDD](https://kdd.ics.uci.edu/databases/kddcup99/kddcup.names), confrontata con [Field Names.csv del mirror fissato](https://github.com/Jehuty4949/NSL_KDD/blob/27bbbdf5c5cccf9970b8b6037a0f19dc09c5a0a9/Field%20Names.csv). UNB documenta le due colonne aggiuntive: attack label e difficulty.

Il [ReadMe del mirror](https://github.com/Jehuty4949/NSL_KDD/blob/27bbbdf5c5cccf9970b8b6037a0f19dc09c5a0a9/ReadMe.txt) considera numeriche le quattro variabili land, logged_in, is_host_login e is_guest_login, già espresse con interi. Nel nostro notebook distinguiamo il tipo fisico numerico dalla loro interpretazione come indicatori discreti. protocol_type, service e flag sono stringhe; attack_label è il target grezzo, difficulty è metadato da escludere dal futuro modello.

La prima esplorazione riguarda il training. Controlli completi di mancanti, duplicati, distribuzione delle famiglie e anomalie sono riservati a T04/T05; questa acquisizione non li dichiara già superati.

## Dimensioni effettivamente lette

Nel ticket T03 il loader legge 125.973 righe train e 22.544 test, entrambe con 43 colonne. Sono rispettivamente 1 e 2 righe in più dei conteggi pubblicati nel paper di Divekar. Le prime righe vengono conservate come dati; nessuna eliminazione o deduplicazione è stata applicata. La causa della divergenza dal paper non è accertata.
