# T27 — Verifica del codice degli autori

**Completato il 5 novembre 2026.** Sola ricerca documentale e analisi statica:
zero training, nessuna metrica del test ufficiale, nessuna modifica a modelli,
mapping applicativo o notebook. T28–T30 non avviati.

## Esito utile per il prossimo planning

Il codice rende esplicite diverse scelte prima sconosciute, ma non costituisce
una procedura completa e verificata per rigenerare tutte le righe della Tabella IV.
Per il confronto con Divekar occorre distinguere la tassonomia del loro codice,
il protocollo descritto nel paper e le nostre baseline di sviluppo.

- Le quattro etichette incerte sono tutte presenti nel dizionario autore.
  `worm` è R2L, non DoS; anche `httptunnel` diverge: U2R anziché R2L.
- Il clustering implementato è **MiniBatchKMeans**, non il KMeans Lloyd completo
  dei nostri esperimenti.
- Sono disponibili parametri espliciti dei sei classificatori; nel ramo NSL
  ispezionato non è implementata la ricerca CV descritta nel paper.
- L'avvio predefinito è binario; il ramo multiclasse attiva il ricampionamento.
  Non è presente uno switch per riprodurre direttamente tutte le condizioni
  originali/SMOTE della tabella. [Sorgenti: main e classificatori](#fonti-fissate).

## Fonti fissate e verificabili

Il [progetto GitLab dell'autore](https://gitlab.com/ARDivekar/Benchmarking-datasets-KDD-99-alternatives-Code)
si presenta come codice del paper IEEE 8586840. Il README contiene soltanto il
vecchio titolo del repository; non è una guida completa alla riproduzione.

Snapshot: [commit `75b8f8b1…`](https://gitlab.com/ARDivekar/Benchmarking-datasets-KDD-99-alternatives-Code/-/commit/75b8f8b1ca6bdb3a9a96736c0c623d984d8d6bb9),
9 marzo 2019, branch `master`. I cinque file NSL hanno gli stessi blob Git nel
[commit master precedente alla pubblicazione arXiv, `c86f42ec…`](https://gitlab.com/ARDivekar/Benchmarking-datasets-KDD-99-alternatives-Code/-/commit/c86f42ec1e031b8c77c7e2dd24e89da0d4d42ba2),
26 giugno 2017, e nel secondo branch fissato a
[`579a9fd2…`](https://gitlab.com/ARDivekar/Benchmarking-datasets-KDD-99-alternatives-Code/-/commit/579a9fd2734c1d3765bb1a4b6f5e0de46fbdea7b).
Questo verifica la stabilità dei sorgenti consultati; non dimostra quale esecuzione
abbia prodotto ogni numero del paper. [Manifest con blob e SHA-256](AUTHOR_CODE_MANIFEST.json).

File primari, tutti fissati al commit:

| Fonte | Contenuto esaminato |
|---|---|
| [constants.py](https://gitlab.com/ARDivekar/Benchmarking-datasets-KDD-99-alternatives-Code/-/blob/75b8f8b1ca6bdb3a9a96736c0c623d984d8d6bb9/NSL/Code/constants.py) | Etichetta grezza → famiglia |
| [preprocessing.py](https://gitlab.com/ARDivekar/Benchmarking-datasets-KDD-99-alternatives-Code/-/blob/75b8f8b1ca6bdb3a9a96736c0c623d984d8d6bb9/NSL/Code/preprocessing.py) | Lettura, encoding, selezione, scaler |
| [main.py](https://gitlab.com/ARDivekar/Benchmarking-datasets-KDD-99-alternatives-Code/-/blob/75b8f8b1ca6bdb3a9a96736c0c623d984d8d6bb9/NSL/Code/main.py) | Ordine dei passaggi e condizioni attivate |
| [classifiers.py](https://gitlab.com/ARDivekar/Benchmarking-datasets-KDD-99-alternatives-Code/-/blob/75b8f8b1ca6bdb3a9a96736c0c623d984d8d6bb9/NSL/Code/classifiers.py) | Classificatori, predizione, metriche e voto |
| [util.py](https://gitlab.com/ARDivekar/Benchmarking-datasets-KDD-99-alternatives-Code/-/blob/75b8f8b1ca6bdb3a9a96736c0c623d984d8d6bb9/NSL/Code/util.py) | Sottocampionamento per SVM |

Acquisizione tramite API pubblica GitLab, progetto `4055141`; nessun codice autore
importato o eseguito. Il nostro script usa `ast.parse` e `ast.literal_eval` per
leggere i dizionari. Sorgenti e nota di ricerca locale restano fuori dal materiale
pubblicabile. Nell'albero esaminato non è presente una licenza esplicita: qui
documentiamo i comportamenti e citiamo le fonti, senza incorporare il codice.

## Etichette: cosa è stato chiarito

Confrontate tutte le **40 etichette** della mappa del progetto: due differenze.
L'autore include inoltre `unknown`, che non fa parte della nostra mappa a cinque
famiglie. Il dizionario viene effettivamente applicato al target multiclasse da
`__string2int_encoding`, righe 33–35 di preprocessing.py.

| Etichetta | Progetto attuale | Codice autore | Fonte diretta |
|---|---|---|---|
| `worm` | DoS | **R2L** | constants.py, riga 38 |
| `snmpgetattack` | R2L | R2L | constants.py, riga 29 |
| `snmpguess` | R2L | R2L | constants.py, riga 33 |
| `sqlattack` | U2R | U2R | constants.py, riga 41 |
| `httptunnel` | R2L | **U2R** | constants.py, riga 31 |

Questa è evidenza della **convenzione autore**, non una certificazione UNB della
tassonomia. Per esempio MIT colloca `httptunnel` fra R2L e `sqlattack` fra U2R:
[Lippmann et al., The 1999 DARPA Off-Line Intrusion Detection Evaluation,
Tabella 3, p.10](https://archive.ll.mit.edu/ideval/files/1999Eval-ComputerNetworks2000.pdf).
I documenti MIT descrivono anche `snmpget`/`snmp-get` come R2L, ma non identificano
separatamente entrambe le stringhe NSL-KDD: non serve inferirle per conoscere
la convenzione Divekar, perché compaiono letteralmente nel suo dizionario.

La [tabella primaria UCI training_attack_types](https://kdd.ics.uci.edu/databases/kddcup99/training_attack_types)
copre le 22 etichette degli attacchi di training e non risolve queste etichette
test-only. La [pagina NSL-KDD di UNB](https://www.unb.ca/cic/datasets/nsl.html)
non fornisce oggi la tabella completa. Per `worm` non è stata trovata in questa
ricerca una fonte del produttore che certifichi DoS come convenzione originale.

**Conseguenza:** per una futura valutazione rivolta al confronto con Divekar,
proponiamo una mappa esplicitamente identificata come convenzione autore. Va
scelta prima di calcolare le metriche del test. T27 documenta gli scostamenti;
non sostituisce `src/targets.py`. Essendo entrambe le differenze test-only, le
metriche di validation già ottenute non sono influenzate da questo confronto.

## Preprocessing: paper, codice disponibile e progetto

Il riferimento testuale è il [paper, §III.A–C](https://arxiv.org/pdf/1811.05372#page=4).
Il percorso effettivo è ricostruito da preprocessing.py e main.py ai link sopra.

| Passaggio | Codice NSL disponibile | Nostro protocollo attuale / implicazione |
|---|---|---|
| Lettura | `read_csv(..., names=None)`; ultime due colonne escluse da X, penultima usata come target | Noi specifichiamo `header=None` e tutti i nomi. Se l'input autore fosse senza header, il default leggerebbe la prima riga come intestazione. È un rischio condizionale, non la causa accertata dei diversi conteggi del paper: i CSV NSL usati non sono presenti nello snapshot. |
| Categoriche | LabelEncoder sulle colonne 1,2,3, ristimato separatamente a ogni lettura train/test | Noi OneHotEncoder stimato sul train. Encoding indipendenti possono associare codici diversi alla stessa categoria se i vocabolari differiscono. |
| Selezione attiva | `main` chiama il metodo `variance`; soglia `0.8*(1-0.8)`, circa 0,16, prima dello scaling | Noi conserviamo 41 feature. Non è la selezione MDI > 0 descritta nel paper; non è disponibile una lista finale certificata delle 20 feature. |
| Altro selettore presente | `feature_imp`: RF da 12 alberi/profondità 20, conserva importanze > 0,01 | Non è chiamato dal percorso `main` e non coincide con MDI > 0. |
| Scaling | StandardScaler fit sul train e transform di train/test | Confine corretto in questa funzione. Noi lo usiamo sulle 38 numeriche per NB/SVM/MLP/K-Means; gli alberi restano senza scaling numerico. |
| Valutazione | Fit sul train e predict sul test separato; classificazione e CM | Noi cinque holdout interni 80/20: manca ancora la misura sullo stesso tipo di test. |

Riferimenti puntuali: [lettura/encoding, righe 11–39](https://gitlab.com/ARDivekar/Benchmarking-datasets-KDD-99-alternatives-Code/-/blob/75b8f8b1ca6bdb3a9a96736c0c623d984d8d6bb9/NSL/Code/preprocessing.py#L11),
[selezione e scaler, righe 46–89](https://gitlab.com/ARDivekar/Benchmarking-datasets-KDD-99-alternatives-Code/-/blob/75b8f8b1ca6bdb3a9a96736c0c623d984d8d6bb9/NSL/Code/preprocessing.py#L46),
[chiamata attiva, main.py riga 33](https://gitlab.com/ARDivekar/Benchmarking-datasets-KDD-99-alternatives-Code/-/blob/75b8f8b1ca6bdb3a9a96736c0c623d984d8d6bb9/NSL/Code/main.py#L33).

## Parametri espliciti rintracciati

Questi sono **argomenti nel codice**, non configurazioni ottimali certificate
per ciascuna riga della Tabella IV. I parametri non impostati dipendono dai default
della libreria dell'epoca; il paper dichiara sklearn 0.18.1. Non sostituirli con
i default attuali presumendo equivalenza. Il branch alternativo ha gli stessi
cinque sorgenti NSL. Nel ramo ispezionato non compaiono la griglia, il punteggio
di selezione completo o il risultato di una ricerca CV per ogni modello.

| Modello | Con `reducedFeature=True` | Altro ramo esplicito / scostamento dalle nostre baseline |
|---|---|---|
| GaussianNB | Costruttore senza argomenti | Nostro NB: numeriche scalate e var_smoothing 1e-9 esplicito; nel main autore multiclasse NB riceve SMOTE ma non undersampling. |
| Decision Tree | `max_depth=20` | Senza riduzione: profondità illimitata. Nostro riferimento: profondità 15. |
| Random Forest | 12 alberi, profondità 20, n_jobs=-1 | Senza riduzione: 13 alberi, profondità illimitata. Nostro RF: 100 alberi, profondità 15, pesi balanced. |
| MLP | Uno strato da 20, alpha=1e-5, early_stopping=False | Senza riduzione: 30, alpha=1e-4, early_stopping=True. Nostro MLP: 100, alpha=1e-4, max_iter=300. |
| SVC | C=10, class_weight=balanced, cache=1500 MB; sottocampionamento prima del fit | Size richiesta 15000 sia per train sia per test; scelta per classe con arrotondamento per eccesso e senza replacement. Nostro SVC: C=1, senza pesi, dati interi, cache512 MB. |
| MiniBatchKMeans | 300 cluster, n_init=10, batch_size=10000, init_size=20000, max_no_improvement=100, reassignment_ratio=1e-6 | Senza riduzione: 400 cluster. Nostro metodo: KMeans Lloyd, 300 cluster; è un algoritmo distinto. |

Fonti: [DT/RF/MLP/GNB, righe 138–214](https://gitlab.com/ARDivekar/Benchmarking-datasets-KDD-99-alternatives-Code/-/blob/75b8f8b1ca6bdb3a9a96736c0c623d984d8d6bb9/NSL/Code/classifiers.py#L138),
[SVC, righe 217–244](https://gitlab.com/ARDivekar/Benchmarking-datasets-KDD-99-alternatives-Code/-/blob/75b8f8b1ca6bdb3a9a96736c0c623d984d8d6bb9/NSL/Code/classifiers.py#L217),
[clustering/voto, righe 247–292](https://gitlab.com/ARDivekar/Benchmarking-datasets-KDD-99-alternatives-Code/-/blob/75b8f8b1ca6bdb3a9a96736c0c623d984d8d6bb9/NSL/Code/classifiers.py#L247),
[sottocampionamento SVM, util.py righe 7–39](https://gitlab.com/ARDivekar/Benchmarking-datasets-KDD-99-alternatives-Code/-/blob/75b8f8b1ca6bdb3a9a96736c0c623d984d8d6bb9/NSL/Code/util.py#L7).

Il voto usa soltanto `km.labels_` e `y_train`: non rietichetta usando il test.
In parità `np.unique` seguito da `argmax` favorisce la prima etichetta ordinata;
cluster vuoti ricevono il codice 0, cioè DoS nell'ordine multiclasse dichiarato.
Il paper descrive invece spareggio casuale. Noi usiamo FAMILY_ORDER e maggioranza
globale del training per i cluster vuoti. Sono differenze da dichiarare.

## Perché il codice non basta per una replica automatica

1. **Condizione attivata:** il punto d'ingresso esegue `main(True, True)`, dunque
   binario e feature ridotte. Con `binary=False` il main applica sempre SMOTE e
   undersampling; NB conserva il train dopo SMOTE senza undersampling. La scritta
   “Original NSL Dataset” stampa la distribuzione prima del ricampionamento,
   non dimostra una valutazione multiclasse originale separata.
2. **Compatibilità del ramo SVM:** inferenza statica, non errore osservato in un
   run. Con cinque classi bilanciate a 995 righe, come descritto nel paper, il
   train dopo undersampling ha 4975 righe. Il default SVM ne richiede circa 15000
   senza replacement: quel percorso richiederebbe una modifica. Non è dimostrato
   quale invocazione sia stata usata per i risultati pubblicati.
3. **Ricerca e dati mancanti:** non sono presenti i CSV NSL invocati, gli output
   dei fit, le scelte finali per ciascuna condizione o un lock completo dell'ambiente.
   Nessun seed sperimentale esplicito nei cinque file NSL esaminati. Le dichiarazioni
   del paper su cinque fold e selezione MDI non trovano una corrispondenza completa
   nel percorso disponibile.

Fonti: [main.py, righe 19–74](https://gitlab.com/ARDivekar/Benchmarking-datasets-KDD-99-alternatives-Code/-/blob/75b8f8b1ca6bdb3a9a96736c0c623d984d8d6bb9/NSL/Code/main.py#L19),
classifiers.py e util.py sopra; albero e hash dei sorgenti nel manifest.
Le incongruenze appartengono allo snapshot disponibile: non provano da sole un
errore nei risultati dell'articolo e non autorizzano a eliminar righe per far
coincidere i conteggi.

## Decisioni lasciate al prossimo ticket

Prima di T28 va identificato il protocollo: nostra baseline sul test con convenzione
autore e scostamenti dichiarati, oppure uno studio distinto di maggiore aderenza
al codice. La prima opzione mantiene leggibili i risultati già ottenuti; la seconda
richiede scelte ulteriori su MiniBatchKMeans, selezione e parametri. Non vanno
mescolate le due condizioni sotto la stessa etichetta di esperimento.

Per il solo T27 sono conclusi: identificazione/versionamento della fonte,
confronto delle 40 etichette, parametri espliciti, preprocessing, differenze
paper/codice e lacune. Non abbiamo preparato il test o scelto nuove configurazioni.
