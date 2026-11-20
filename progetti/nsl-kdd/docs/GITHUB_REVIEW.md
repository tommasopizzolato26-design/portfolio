# Ricognizione GitHub NSL-KDD

Data: 2026-11-02. Scopo: riferimenti per il lavoro futuro; nessun codice copiato, repository clonato o risultato adottato. Il benchmark locale resta una classificazione a cinque famiglie e il confronto con Divekar2018 richiederà un protocollo proprio.

Metodo: lettura di pagine e codice originali GitHub. Il connector GitHub ha restituito `Transport closed`; è stato usato il web come ripiego. Commit SHA non risolti: i link sottostanti puntano a `master` e vanno fissati a un commit prima di un eventuale riuso. Questa è una ricognizione, non una riproduzione eseguita.

## 1. Mamcose/NSL-KDD-Network-Intrusion-Detection

- **Cosa fa:** notebook con Random Forest, KNN, SVC ed ensemble dichiarati nel [README](https://github.com/Mamcose/NSL-KDD-Network-Intrusion-Detection/blob/master/README.md).
- **Spunto:** il [notebook NID.ipynb](https://raw.githubusercontent.com/Mamcose/NSL-KDD-Network-Intrusion-Detection/master/NID.ipynb) esplicita i nomi delle colonne e mostra dimensioni, prime righe e distribuzioni delle etichette. Carica CSV a 42 colonne (41 feature e label), quindi non va usato come schema automatico dei TXT originali con difficulty.
- **Limite verificato:** crea quattro problemi separati normal/famiglia, anziché un unico classificatore a cinque classi. Adatta LabelEncoder, OneHotEncoder e StandardScaler separatamente anche sul test. Quest'ultimo usa statistiche del test e non rappresenta la trasformazione appresa sul train: il futuro preprocessing locale dovrà invece apprendere sul train e trasformare validation/test. Non è una conclusione ricavata dalle accuracy, ma dalle chiamate `fit` lette nel notebook.
- **Licenza:** file [LICENSE](https://github.com/Mamcose/NSL-KDD-Network-Intrusion-Detection/blob/master/LICENSE) presente; GitHub lo identifica GPL-3.0 nella [pagina del repository](https://github.com/Mamcose/NSL-KDD-Network-Intrusion-Detection). Il testo integrale non è stato restituito dalla pagina del file.

## 2. thinline72/nsl-kdd

- **Cosa fa:** notebook Python/PySpark con feature selection, PCA, K-Means e Gaussian Mixture associati a Random Forest, oltre a ensemble. Il [README con codice](https://github.com/thinline72/nsl-kdd/blob/master/README.md) e il [notebook](https://github.com/thinline72/nsl-kdd/blob/master/NSL-KDD.ipynb) offrono una progressione leggibile da caricamento ed EDA a modelli e valutazione.
- **Spunto:** separa percorsi train/test e dichiara colonne e gruppi di tipi. Nella preparazione, `prep_model` viene adattato su `scaled_train_df` e poi applicato anche al test.
- **Limite verificato:** l'encoding personalizzato ricava comunque categorie separatamente dal test; la singola pipeline non prova l'assenza di leakage nell'intero flusso. Gli approcci ibridi e Spark aggiungono complessità non necessaria ai primi ticket e non equivalgono al K-Means con semplice assegnazione di etichette dal training.
- **Licenza:** [LICENSE](https://github.com/thinline72/nsl-kdd/blob/master/LICENSE) presente e identificato Apache-2.0 da [GitHub](https://github.com/thinline72/nsl-kdd); testo integrale non restituito dalla pagina del file.

## 3. r7sy/IntrusionDetection

- **Cosa fa:** la [descrizione originale](https://github.com/r7sy/IntrusionDetection) presenta un approccio autoencoder; il repository espone il notebook [Improving Network Intrusion Detection using a Denoising Autoencoder with Dropout](https://github.com/r7sy/IntrusionDetection/blob/master/Improving%20Network%20Intrusion%20Detection%20using%20a%20Denoising%20Autoencoder%20with%20Dropout.ipynb).
- **Spunto:** tenerlo come riferimento distinto per un'eventuale estensione con autoencoder.
- **Limite verificato:** non è il riferimento diretto per i classificatori ora previsti. La lettura del corpo del notebook non è riuscita: loader, mapping delle famiglie, preprocessing e protocollo train/test restano non verificati.
- **Licenza:** non verificata; nell'elenco radice consultato compare il solo notebook. Non presumere un permesso di riuso.

## Implicazioni per il progetto

Per i primi tre ticket serve un notebook breve e originale con caricamento esplicito e `head`, `info`, `describe`. Questi repository offrono esempi di presentazione e casi da controllare, senza sostituire la specifica dello schema o la fonte del dataset. Non è emersa una catena di provenienza sufficientemente verificata da adottare uno di questi mirror dei dati: la presenza di CSV/TXT nel repository non certifica che siano copie immutate dell'archivio originale.
