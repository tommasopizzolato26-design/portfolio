# Dataset con attacchi e serie temporali

Ricognizione del 20 novembre 2026. Obiettivo: unire etichette di intrusion detection, come NSL-KDD, e analisi temporale del traffico, come CESNET-TimeSeries26. La presenza di timestamp non rende automaticamente un dataset una serie regolare: possono servire aggregazione e controlli sulla continuità.

## UGR'16: candidato per serie di lungo periodo

Traffico NetFlow reale di un ISP. La raccolta di riferimento copre marzo–giugno 2016; il test luglio–agosto comprende attacchi controllati insieme al traffico reale. Il traffico di riferimento non è garantito privo di anomalie. [Paper degli autori, NOMS 2023](https://digibug.ugr.es/bitstream/handle/10481/81203/0.Main.pdf?isAllowed=y&sequence=3).

La distribuzione degli autori **UGR16_FeatureData** contiene aggregazioni ogni minuto: normalmente 134 contatori e 8 conteggi di attacchi per osservazione. Sono disponibili CSV e MATLAB; il README documenta timestamp e calendario nelle strutture MATLAB. Non è un pannello di byte e pacchetti per host già pronto come CESNET. I timestamp nei singoli CSV non sono stati verificati. [Repository degli autori](https://github.com/josecamachop/UGR16_FeatureData).

La variante v1 usa marzo–giugno; v2 esclude giugno perché contiene anomalie reali che influenzano il riconoscimento delle botnet. V3/v4 cambiano anche anonimizzazione e direzionalità dei flussi. Verificare calendario e buchi prima di creare finestre consecutive. [NOMS 2023](https://digibug.ugr.es/bitstream/handle/10481/81203/0.Main.pdf?isAllowed=y&sequence=3). Un successivo studio mostra che la variante dei dati può incidere sui risultati più della scelta del modello. [Camacho e Rodríguez-Gómez, Data 2025](https://doi.org/10.3390/data10030033).

## TON_IoT: alternativa per serie costruite dai flussi

Testbed IoT/IIoT con traffico normale e attacchi. Offre PCAP, log e CSV Zeek, dati processati, telemetria di sensori e ground truth con timestamp degli eventi. Si possono progettare aggregazioni temporali del traffico, anche per host, partendo dai dati completi. La cartella Train_Test contiene campioni: non presumere che conservino la continuità temporale. Durata, dimensioni e schema di ogni CSV non verificati direttamente. [Fonte UNSW](https://research.unsw.edu.au/projects/toniot-datasets).

## CICIDS2017 e CSE-CIC-IDS2018 corretti

Traffico di laboratorio con attacchi programmati. CICIDS2017 copre cinque giorni; sono disponibili PCAP e flussi etichettati con riferimenti temporali. Occorre selezionare una distribuzione che conservi timestamp, poi costruire le serie. È più adatto a finestre brevi che allo studio di stagionalità lunghe. [Fonte UNB](https://www.unb.ca/cic/datasets/ids-2017.html).

Preferire la ricostruzione Liu–Engelen et al. CNS2022, che corregge problemi di estrazione e labeling. La distinzione tra attacchi riusciti e tentativi richiede una scelta esplicita nella valutazione. [Studio, documentazione e download](https://intrusion-detection.distrinet-research.be/CNS2022/index.html).

## IoT-23

Comprende 23 scenari: 20 catture con malware e 3 benigne, raccolte nel 2018–2019. Offre PCAP e flussi Zeek etichettati in conn.log.labeled. Utile per finestre temporali del comportamento di botnet e dispositivi IoT; gli scenari non formano una singola serie continua. La pagina ufficiale indica 8,8 GB per i soli flussi e 21 GB per la versione completa. [Stratosphere Laboratory](https://www.stratosphereips.org/datasets-iot23).

## NF-ToN-IoT-v3: prima scelta per la classificazione con contesto temporale

La versione NetFlow **v3** è distribuita in CSV, con un flusso per riga, 53 attributi NetFlow e due etichette per il rilevamento binario e la classificazione. La University of Queensland riporta 27.520.260 flussi, con nove tipi di attacco oltre al traffico benigno. I timestamp di inizio e fine sono in millisecondi Unix. IP, byte e pacchetti permettono di costruire serie di traffico in finestre regolari, anche per host. Gli autori mostrano aggregazioni al minuto nella sezione 5.4. [Distribuzione UQ](https://rdm.uq.edu.au/files/343e2e8c-6e6e-4a0c-813d-a46acea1b7f4), [classi e quantità](https://staff.itee.uq.edu.au/marius/NIDS_datasets/), [Luay et al., sezioni 4 e 5](https://arxiv.org/html/2503.04404v3#S4).

Li e Zhou hanno verificato l'ordine temporale del CSV e riportato la distribuzione per classe in cinque blocchi cronologici. Ad esempio DDoS compare in più blocchi, mentre backdoor e ransomware compaiono solo nell'ultimo. Il dataset permette quindi di misurare sia la classificazione di tipi già osservati sia il rilevamento binario di tipi assenti dal training. Gli attacchi sono programmati in un ambiente IoT di laboratorio. L'ordine cronologico dei record va verificato separatamente dalla continuità delle finestre per host. [Li e Zhou, sezione 4.1 e tabella A19](https://www.mdpi.com/2079-9292/15/20/4854), [testbed UNSW](https://research.unsw.edu.au/projects/toniot-datasets).

## LITNET-2020: candidato per una rete accademica reale

Il paper documenta circa dieci mesi tra primo e ultimo flusso, 12 tipi di attacco e una tabella di flussi con dati temporali. Un coautore pubblica `ALLinONE.zip` da 1,15 GB su GitHub. La continuità dei periodi effettivamente conservati nell'archivio pubblico resta da verificare, insieme alle feature usate per costruire le etichette. [Paper, sezioni 3.4 e 4.2](https://doi.org/10.3390/electronics9050800), [archivio del coautore](https://github.com/Grigaliunas/electronics9050800/blob/main/dataset/ALLinONE.zip).

## Scelta proposta

La precisazione del tutor dà priorità all'etichetta per flusso, così da mantenere il confronto con NSL-KDD. Per questo sceglierei **NF-ToN-IoT-v3**. UGR'16 FeatureData resta adatto allo studio dell'andamento del traffico su periodi lunghi, con un minuto per riga e conteggi di attacchi. LITNET-2020 è l'alternativa se la rete accademica reale è un requisito.

La prima prova confronta, sugli stessi flussi futuri, un classificatore tabellare e lo stesso modello con statistiche del traffico passato, come byte, pacchetti e flussi nelle finestre precedenti. Si assegnano le statistiche dei flussi completati al tempo in cui diventano osservabili. Si usano i timestamp per l'ordine e gli IP per aggregare. L'obiettivo è misurare il contributo del contesto al riconoscimento per classe, al rilevamento binario degli attacchi mai visti e al tasso di falsi allarmi. La verifica qui è documentale. Prima del test vanno controllati direttamente nel CSV copertura delle finestre e classi nei blocchi scelti.

Per la versione pubblicata del riferimento NF-ToN-IoT-v3, vedere Luay et al. (2026), [*Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection*](https://doi.org/10.1109/ACCESS.2026.3688204).
