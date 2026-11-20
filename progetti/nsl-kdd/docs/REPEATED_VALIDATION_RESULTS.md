# Dieci ripetizioni del Decision Tree: medie e variabilità

Misurate il 2 novembre 2026 su richiesta dell'utente. Notebook:
[04_repeated_validation.ipynb](../notebooks/04_repeated_validation.ipynb).

## Protocollo

- Solo KDDTrain+, 125973 righe; tutte le 41 feature, nessuna riga eliminata.
- Dieci split stratificati 80/20: 100778 train e 25195 validation ciascuno.
  Seed fissati prima delle misure: 42–51. Lo stesso seed controlla split e albero.
  Varia quindi la casualità di entrambi, non soltanto quella degli split equivalenti del classificatore.
- Tre profondità: 10, 13, 15; **30 fit**. I tre modelli di ogni run usano le stesse righe
  di train e validation, per un confronto abbinato. Nessuna ricerca di altri parametri.
- OneHotEncoder delle tre categoriche e albero in una nuova Pipeline sklearn per fit;
  encoder appreso solo sul train pertinente. Le 38 numeriche restano invariate.
- API pandas/sklearn originali nel notebook; da src/ soltanto costanti dello schema e mapping.
  Nessuna lettura o valutazione del test ufficiale.

Un intero identico in random_state riproduce la stessa casualità; dieci interi diversi
consentono dieci prove diverse e riproducibili. Rimuovere random_state non è necessario.
[Documentazione sklearn](https://scikit-learn.org/stable/common_pitfalls.html#controlling-randomness).

## Come vengono aggregate le misure

Ogni run ha lo stesso peso. Media, deviazione standard campionaria (ddof=1), minimo e
massimo sono calcolati sulle dieci metriche individuali. La DS descrive dispersione fra
run; non è un errore standard né un intervallo di confidenza. Le confusion matrix vengono
normalizzate per famiglia vera in ogni run e poi mediate; conserviamo anche la DS di ogni
cella e tutti i conteggi originali. Precision e F1 sono mediati dalle metriche delle run,
senza ricavarli dalla matrice media.

## Esito delle dieci prove

DS = deviazione standard campionaria fra le ripetizioni; pp = punti percentuali.

| Profondità | Errori R2L: media ± DS | Errori U2R: media ± DS | Macro F1: media ± DS |
|---|---:|---:|---:|
| 10 | 19.45% ± 2.77 pp | 55.00% ± 15.09 pp | 0.8851 ± 0.0282 |
| 13 | 8.74% ± 2.15 pp | 49.00% ± 18.53 pp | 0.9008 ± 0.0317 |
| 15 | 8.29% ± 1.87 pp | 47.00% ± 16.36 pp | 0.9013 ± 0.0296 |

- **R2L:** il vantaggio delle profondità 13/15 si conferma nei dieci split:
  gli errori medi scendono dal 19,45% all'8,74% e all'8,29%.
- **U2R:** gli errori medi sono 55%, 49% e 47%. In tutte e tre le configurazioni
  le singole prove vanno dal 30% al 70% di errori. Il precedente seed 42, con 30%,
  era uno degli esiti più favorevoli osservati, non la prestazione tipica.
- **Precision U2R media:** 77,08% a 10, 69,11% a 13 e 64,70% a 15. Con gli alberi
  più profondi il recall medio sale (45% / 51% / 53%), ma aumentano i falsi positivi.
- **13 contro 15:** il macro F1 medio differisce di circa 0,0005; 15 supera 13
  in 4 split su 10, mentre 13 lo supera negli altri 6. È un confronto descrittivo:
  non emerge un vincitore stabile dalle medie e da queste dieci prove sovrapposte.

Ogni validation contiene 10 U2R; in totale abbiamo valutato **43 record U2R distinti**,
riutilizzati fra gli split, non 100 casi indipendenti. Le dieci prove rendono visibile
la variabilità; non risolvono la scarsità di dati o il rischio di generalizzazione.
Non scegliamo automaticamente un modello finale e non avviamo altri esperimenti.

## Metriche aggregate complete

| Profondità | Accuracy media ± DS | Weighted F1 media ± DS | Macro F1 min–max |
|---|---:|---:|---:|
| 10 | 0.996487 ± 0.000318 | 0.996369 ± 0.000336 | 0.841178–0.928445 |
| 13 | 0.997444 ± 0.000288 | 0.997404 ± 0.000310 | 0.851619–0.936992 |
| 15 | 0.997611 ± 0.000256 | 0.997584 ± 0.000275 | 0.844447–0.944019 |

## Limiti e verifiche

Le validation si sovrappongono e non sono indipendenti: le ripetizioni non creano nuovi
dati e non giustificano intervalli di confidenza ingenui. Duplicati e overlap fra vettori
di feature non sono stati modificati: resta il protocollo di DATA_AUDIT.md. I risultati
descrivono la sensibilità alla casualità su NSL-KDD, non reti moderne o il test ufficiale.
Le profondità sono state esplorate sulla validation: questa non è una stima finale indipendente.

Esecuzione da kernel pulito: notebook 04 con 17 celle eseguite, zero errori; aggiunta poi
soltanto una cella Markdown con questi esiti, per un totale finale di 18 celle.
Verificati 10 split distinti e disgiunzione train/validation dentro ciascun run.
Il seed 42 ricrea esattamente tutte e tre le predizioni del confronto precedente.
Tutte le metriche, le medie/DS/min/max e le matrici sono state ricalcolate indipendentemente
dagli indici, dalle risposte e dalle predizioni salvate, senza nuovi fit. Suite: 21 test passati.

## Artefatti locali

In artifacts/repeated_validation/, ignorata da Git:

- run_metrics.csv: 30 righe di metriche aggregate, con run/seed/profondità.
- class_metrics.csv: 150 righe di conteggi, precision, recall e F1 per famiglia.
- overall_summary.csv e class_summary.csv: media/DS/min/max.
- results.json: protocollo, hash sorgente, versioni, risultati, matrici e conteggi distinti.
- predictions.npz: indici, risposte e predizioni Unicode; lettura con allow_pickle=False.
- mean_confusion_matrices.png: le tre matrici normalizzate medie, stessa scala 0–100%.

HTML locale in artifacts/04_repeated_validation.html. Evidenze in .local/repeated-validation/.
Nessuna modifica ai risultati del notebook 03, alle dipendenze o ai dati. Nessun commit/push.
