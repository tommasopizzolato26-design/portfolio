# Protocollo del test ufficiale — T28

Congelato il 5 novembre 2026, prima delle predizioni sul test. Configurazione completa:
[`official_test_v1.json`](../configs/official_test_v1.json).

Usiamo tutto KDDTrain+ per apprendere e tutto KDDTest+ per valutare. Non facciamo
un nuovo train_test_split: la separazione è già definita dai due file. Manteniamo
41 feature, cinque famiglie e le configurazioni sperimentate; nessuno SMOTE,
selezione di feature, deduplicazione o ricerca di parametri. Target e difficulty
sono esclusi dai predittori. Il test non decide parametri, soglie o preprocessing.

| Modello | Configurazione principale | Numeriche |
|---|---|---|
| Decision Tree | profondità 15, senza pesi | originali |
| Random Forest | 100 alberi, profondità 15, balanced | originali |
| Gaussian Naive Bayes | var_smoothing=1e-9 | StandardScaler |
| SVM RBF | C=1, gamma=scale, senza pesi | StandardScaler |
| Rete neurale | uno strato da 100, ReLU/Adam, massimo 300 epoche | StandardScaler |
| K-Means | 300 cluster, Lloyd, 10 inizializzazioni | StandardScaler |

Un fit per modello; seed 1 per i modelli stocastici. I dieci restart interni di
K-Means appartengono a un solo fit. GaussianNB e SVC senza probabilità non
richiedono un seed per queste configurazioni. I cinque holdout precedenti
restano un esperimento distinto: qui non stimiamo media, deviazione o intervalli.
Il confronto con la validation sarà descrittivo: cambia anche la quantità di training.

One-hot delle tre colonne categoriche, con categorie apprese sul solo training.
Le eventuali categorie nuove diventano blocchi di zeri. Scaler appreso sul training,
senza refit sul test. Ogni futuro notebook di modello costruirà il proprio
preprocessore con le API sklearn originali e verificherà il protocollo congelato.
Limiti di thread OPENBLAS_NUM_THREADS=2 e OMP_NUM_THREADS=2 prima di avviare il kernel;
versioni e tutti i parametri sono registrati nel JSON.

Metrica primaria: macro F1; anche weighted F1 (per confronto con il paper),
accuracy, precision/recall/F1/support e falsi positivi per classe. Confusion matrix
in conteggi e normalizzata per classe vera: diagonale = recall; 1−diagonale =
errore di quella classe. Precision necessaria per leggere i falsi allarmi.
Ordine fisso Normal, DoS, Probe, R2L, U2R; zero_division=0. Nessuna scelta del
modello o modifica di configurazione guidata dal test in questo protocollo.

Il profilo autore assegna worm a R2L e httptunnel a U2R; lo storico resta invariato.
Voto K-Means sui soli target di training, parità risolta con l'ordine delle famiglie,
cluster vuoti con la maggioranza globale del training.

## Limiti del confronto con il paper

È una baseline adattata: one-hot e 41 feature, configurazioni nostre, KMeans Lloyd
invece di MiniBatchKMeans del codice autore. Non riproduciamo encoding indipendente
train/test né altre incongruenze del sorgente. Differenze e prove sono in
[AUTHOR_CODE_AUDIT.md](AUTHOR_CODE_AUDIT.md). I conteggi dei file differiscono da
quelli dichiarati nel paper; non eliminiamo righe per farli coincidere. Duplicati e
sovrapposizioni train/test noti restano presenti e limitano l'interpretazione.

T28–T30 preparano e controllano soltanto gli input. T31–T36 richiederanno i sei
fit, in notebook separati; T37 confronterà i risultati. Nessuna metrica del test
ufficiale è stata calcolata in questa preparazione.
