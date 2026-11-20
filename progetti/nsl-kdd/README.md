# Rilevamento di attacchi su NSL-KDD

Progetto di tesi all’Università di Ferrara. Ho studiato come riconoscere gli attacchi dal traffico di rete e quanto cambia il risultato quando il modello incontra un tipo di attacco nuovo.

**[Leggi il resoconto completo della tesi (PDF)](docs/Tesi_Studio_Dataset_e_Decisioni.pdf)**

## Classificazione degli attacchi

Ho confrontato sei modelli su cinque classi di traffico. Ho addestrato le configurazioni finali sul **100% di KDDTrain+** (125.973 connessioni) e le ho valutate su **KDDTest+** (22.544 connessioni).

Il **MLP** (rete neurale) ha ottenuto il miglior macro F1 (**0,5469**), la media dei punteggi F1 delle cinque classi. Ha riconosciuto il **10,71%** degli attacchi R2L e l’**8,50%** degli U2R.

[Risultati dei sei modelli, matrici di confusione e confronto con Divekar et al.](docs/OFFICIAL_BENCHMARK_REPORT.md)

## Rilevamento di tipi di attacco mai visti

Ho reimplementato **DLHA**, il metodo di Wisanwanichthan e Thammawichai (2021). In questo confronto i modelli danno un esito **normale o attacco**. DLHA rileva più attacchi di tipi assenti dal training e genera più falsi allarmi.

| Metodo | Rilevamento su 3.750 attacchi di tipi assenti | Falsi allarmi su 9.711 connessioni normali |
|---|---:|---:|
| MLP | 48,69% | 7,32% |
| DLHA (media di cinque prove) | **90,68%** | 16,33% |

![Rilevamento di attacchi mai visti e falsi allarmi per MLP e DLHA](docs/assets/dlha_official_test/dlha_comparison.png)

[Confronto con il paper e matrici di confusione binarie](docs/DLHA_OFFICIAL_COMPARISON.md)

## Approfondimenti

- [Notebook e istruzioni per riprodurre gli esperimenti](notebooks/README.md)
- [NF-ToN-IoT-v3, il dataset scelto per il prossimo esperimento](docs/TEMPORAL_DATASETS.md)
