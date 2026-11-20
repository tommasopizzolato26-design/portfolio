# Decisioni

## D01 — Obiettivo corretto

**Confermato dall'utente, 1 novembre 2026.** Riconoscimento degli attacchi su NSL-KDD e confronto con il benchmark. CESNET24/26 e modelli di forecasting sono in pausa. La precedente proposta CESNET non è il protocollo di questo progetto.

## D02 — Portfolio e leggibilità

**Confermato dall'utente.** Il progetto servirà anche al CV su GitHub. Documentazione essenziale, notebook divisi per argomento, errori e correzioni visibili. Qualità prima della velocità. Scelta organizzativa: notebook per il racconto e piccoli moduli per le funzioni condivise.

## D03 — Avvio per piccoli passi

**Confermato dall'utente.** Questa fase prepara la cartella. Nella prossima sessione: planning, poi ticket con criteri di completamento; quindi sviluppo. Nessun addestramento avviato.

## D04 — Librerie e fedeltà

**Proposta da definire nel planning.** Partire da scikit-learn per i sei metodi originali; PyTorch eventualmente per una variante della rete neurale. Riutilizzare codice con provenienza e licenza verificabili, senza attribuire agli autori repository di terzi.

## D05 — Continuità

**Scelta organizzativa.** `AGENTS.md` contiene regole stabili; l'handoff locale conserva soltanto stato verificato e prossimo passo. Aprire una nuova chat sul progetto per ripartire senza l'intera cronologia. Nessuna skill handoff aggiuntiva installata.

## D06 — Lavoro autonomo graduale

**Confermato dall'utente, 1 novembre 2026.** Nella sessione del 2 novembre: planning e poi una prima prova di lavoro autonomo breve su un ticket definito, con verifiche e revisione. Aumentare progressivamente durata e numero di ticket in base alla qualità osservata. Limiti e criteri di arresto saranno fissati nel planning. Nessuna esecuzione automatica o notturna è stata programmata.

## D07 — Primo modello e ticket piccoli

**Confermato dall'utente, 2 novembre 2026.** Limitare il prossimo goal al punto 3 del percorso discusso: preparare i dati e provare un primo modello semplice sulle cinque classi. Priorità a leggibilità e pulizia del codice. Usare ticket piccoli, per esempio download verificato e prima esplorazione in notebook come unità distinte. L'utente sceglierà quanti ticket eseguire per la prima prova; questa richiesta autorizza il planning, non l'avvio dei ticket.

**Proposta operativa dell'assistente, non ancora approvata nei dettagli.** Nove ticket in docs/superpowers/plans/2026-11-02-primo-modello.md. Primo modello Decision Tree senza tuning, con baseline DummyClassifier e validazione ricavata dal solo training; test ufficiale riservato al successivo benchmark. Parametri e confini sono in docs/PLANNING.md. Nessun ticket avviato nella preparazione del piano.

## D08 — Prima prova autorizzata

**Confermato dall'utente, 2 novembre 2026.** Eseguire i primi tre ticket e salvare il CSV nella cartella del progetto. Aggiungere una breve ricognizione di progetti GitHub per il futuro; il lavoro resta una prova e non autorizza i ticket successivi.

**Attuazione verificata.** Ambiente dedicato e kernel locale; TXT originali e copie CSV identiche in data/raw/, ignorati da Git; prima esplorazione in notebook. Fonte UNB consultata per descrizione/condizioni, file acquisiti da mirror fissato a commit con hash verificati. Nessun codice di terzi copiato, dato trasformato o modello addestrato. Dettagli in DATA_SOURCE.md, DATA_MANIFEST.json e PROGRESS.md.

## D09 — Completare T04–T09 separando i passaggi

**Confermato dall’utente, 2 novembre 2026.** Dopo la prima prova eseguire tutti i ticket restanti;
invertire T05/T06 per definire prima feature/encoding e poi target/split. Questa nuova autorizzazione
supera i limiti storici di D08. Il fit resta rigorosamente dopo lo split e sul solo train pertinente.

**Attuazione.** Cleaning conservativo documentato; 41 feature esplicite, tre categoriche one-hot,
numeriche invariate, target/difficulty esclusi. Mapping UCI per il train, estensioni MIT e convenzioni
test-only in LABEL_MAPPING.md. Sei vettori feature discordanti condivisi nello split interno: limite
misurato, protocollo non cambiato. Baseline e albero senza tuning sullo stesso split seed42.
Risultati, supporti e limiti in FIRST_MODEL_RESULTS.md. Nessun commit/push o metrica del test ufficiale.

## D10 — API originali e prove didattiche leggibili

**Richiesto dall'utente, 2 novembre 2026.** Rendere visibili training e train_test_split
con le API pandas/sklearn originali, evitando wrapper locali; massimo tre profondità
(scelte3/5/10), grafico dell'albero e valutazione con confusion matrix.

**Attuazione.** Notebook02/03 importano da src/ solo costanti; riferimento depth10 invariato
nei risultati. Prova delle profondità sulla sola validation, separata dalle misure iniziali.
La confusion matrix descrive errori fra classi, non correlazioni fra feature. Per una prima
eliminazione motivata, unica colonna costante nel train (num_outbound_cmds) esclusa in un
nuovo fit separato depth10; confronto completo in FIRST_MODEL_RESULTS.md. Nessuna selezione
basata su correlazioni lineari arbitrarie col target o sui risultati del test ufficiale.

## D11 — Confrontare 10/13/15 e rimuovere la prova con 40 feature

**Richiesto dall'utente, 2 novembre 2026.** D11 supera il confronto 3/5/10 e la prova
di rimozione di D10: conservare tutte le 41 feature, confrontare solo 10/13/15 e dare
priorità alle confusion matrix normalizzate per riga. Alberi brevi solo come vista grafica.
Attuazione: nessun fit breve aggiuntivo; disegno dei primi tre livelli dell'albero completo.
Stesso split/seed/preprocessing, due esecuzioni ripetibili. R2L migliora, U2R resta 3/10
errori; precision U2R peggiora a 13, recupera a 15. Report attuale in FIRST_MODEL_RESULTS.md.
Le decisioni e misure precedenti sono storia del progetto, non il protocollo corrente.
Fermarsi al confronto richiesto e attendere la revisione prima di altre modifiche al modello.

## D12 — Dieci ripetizioni con casualità diversa e media dei risultati

**Richiesto dall'utente, 2 novembre 2026.** Ripetere dieci volte per evitare che
lo stesso random_state produca misure identiche. Scelta operativa resa esplicita:
dieci seed diversi e registrati, 42–51, per split e albero; tre profondità abbinate
dentro ciascuna run. Tutte le 41 feature e preprocessing train-only conservati.
Notebook04 dedicato, senza sostituire il riferimento del singolo seed42 in notebook03.
Media/DS campionaria/min/max, matrici normalizzate medie e predizioni salvate.
Dieci holdout sovrapposti non sono campioni indipendenti: non garantire affidabilità
o generalizzazione, né dedurre significatività dalla sola media. Risultati e limiti
in REPEATED_VALIDATION_RESULTS.md. Nessun altro metodo, test o tuning autorizzato.

## D13 — Prossima fase: diagnosi U2R e pochi modelli (planning)

L'utente ha scelto diagnosi U2R e confronto limitato, poi ha richiesto grill-me.
Bozze in superpowers/specs/2026-11-02-classi-rare-design.md e relativo piano T10–T14.
Proposte: profilo classi rare, diagnosi errori, albero15 balanced, RF100alberi15 balanced,
confronto finale; seed42–51 e41feature conservati. Modelli e criterio di giudizio da
discutere prima di avviare il blocco. Nessun nuovo esperimento autorizzato o eseguito dal planning.

## D14 — Conferma grill-me e scelta delle cinque prove correnti

L'utente conferma Q1 e Q2: precision/recall insieme, nessuna promozione automatica;
riferimento albero15, albero15 balanced e RF100alberi15 balanced. Dopo la rilevazione
dei cinque seed1–5 correnti sceglie esplicitamente quel protocollo: dieci nuovi fit totali,
nessun riaddestramento del riferimento. Questo supera i venti fit/seed42–51 del piano iniziale.

T10–T14 completati. Risultati in RARE_CLASS_COMPARISON.md. Snapshot rigenerabile senza fit
in artifacts/rare_class_reference/, correggendo solo la copia delle statistiche obsolete.
Notebook04 e risultati originali preservati. RF promettente ma non promossa automaticamente;
U2R ancora difficile. Qualsiasi nuova configurazione, dato o benchmark finale va concordato.

## D15 — Un nuovo modello per notebook: GaussianNB e SVM RBF

L'utente rifiuta altri approfondimenti RF, chiede un modello alla volta e un file
per ciascuno, sceglie Gaussian Naive Bayes e SVM e autorizza l'esecuzione dopo il
riepilogo. Due notebook09/10, cinque split80/20 seed1–5, dieci nuovi fit totali.
Fit/predict separati, API originali, tutte41feature, confronto da predizioni storiche.

Scelte operative dichiarate prima del training nella spec nb-svm: numeriche scalate
train-only per entrambi, categoriche one-hot dense; NB priorsNone/var_smoothing1e-9;
SVC RBF C1/gamma scale/senza pesi/probabilityFalse, no tuning. GaussianNB e SVC così
configurati sono deterministici a split fissato: variano gli split, non seed fittizi
del classificatore. Il70/30 resta sensibilità separata. RF resta riferimento esistente.
Risultati in NB_SVM_RESULTS.md; nessun automatico vincitore, test ufficiale o altra prova.


## D16 — Copertura dei sei modelli e confronto abbinato

Mandato utente: aggiungere i rimanenti metodi del benchmark allo stesso modo.
Notebook11 MLP100 poi12 KMeans300+voto;13 confronto senza fit. Cinque split80/20
seed1–5 esistenti,41feature, nessun test ufficiale/tuning. Scelte implementatore
fissate prima del training:100ReLU/Adam/max300/noearlystopping;300cluster/n_init10/
Lloyd/max300, voto train-only, parità FAMILY_ORDER, vuoti maggioranza training.
Preprocessing numerico standardizzato/one-hot train-only; inizializzazione variata
con seed. Non riproduzione numerica esatta; conservare precision/recall/FP e limiti.
Confronto principale sei metodi, albero balanced come variante. Report completo
BENCHMARK_MODEL_COMPARISON.md; nessun approfondimentoRF o vecchiofit aggiunto.

## D17 — T27: fonte autore verificata, profilo test da scegliere

Mandato limitato dell'utente: «si fai solo t27». Sola ricerca/analisi statica,
zero fit e nessuna modifica a modelli, notebook o target applicativi.
Fonte GitLab id4055141, master75b8f8b1ca6bdb3a9a96736c0c623d984d8d6bb9;
cinque sorgenti NSL identici nei blob alla revisione master2017 e al branch alternativo.
Documentati mapping40label (due differenze:worm e httptunnel), parametri espliciti,
MiniBatchKMeans, selezione per varianza, ingresso binario e ricampionamento multiclasse.
Il codice non certifica una replica completa delle righe della TabellaIV.
Non adottata automaticamente la tassonomia autore: il profilo della futura
valutazione sul test va fissato prima delle metriche. T28–T30 non avviati.
Report AUTHOR_CODE_AUDIT.md; hash/fonti in AUTHOR_CODE_MANIFEST.json.


## D18 — Test ufficiale con protocollo separato (5 novembre 2026)

Autorizzati T28–T30. Conserviamo configurazioni e 41 feature; prepariamo training
completo e test ufficiale, con profilo di etichette del codice autore. Lo storico
rimane invariato. Un fit futuro per modello, seed 1 dove applicabile; niente tuning,
SMOTE o selezione sul test. È una baseline adattata, non replica numerica del paper.
Dettagli e metriche predefinite in OFFICIAL_TEST_PROTOCOL.md e JSON associato.
Gli split precedenti 80/20 di KDDTrain+ sono training/validation interna; KDDTest+
rimane la valutazione finale. I modelli finali saranno riaddestrati da zero sul
training completo, non continuati a partire dai modelli degli holdout.


## D19 — T31 come prova singola prima di estendere (5 novembre 2026)

L'utente limita l'esecuzione a Decision Tree15 sul training completo e test ufficiale.
Manteniamo invariato official_test_v1. Non avviamo automaticamente T32–T37.
Il test ufficiale è ora consultato; eventuali cambiamenti guidati dall'esito saranno
esplorativi. Il divario rispetto agli holdout non isola l'effetto di più training.


## D20 — Estensione del protocollo completo e report prima del PDF

5 novembre 2026: utente autorizza tutti gli altri modelli, confronto con benchmark
e report. Nuovi esperimenti senza split80/20: training completo e test ufficiale.
Le vecchie valutazioni rimangono storiche, nessun risultato viene riscritto.
Manteniamo tutte le configurazioni congelate prima di T31, senza tuning sul test.
Report Markdown e notebook pronti alla revisione; PDF da aggiornare soltanto dopo
approvazione esplicita dell'utente. Nessun nuovo esperimento oltre T37 autorizzato.


## D21 — Diagnosi per presenza nel training e sottotipo

7 novembre 2026. Eseguiti solo T38 e T39 autorizzati, su predizioni salvate.
"Presente" significa nome specifico osservato nel training; Normal è distinto.
Il confronto separa famiglia corretta da qualsiasi attacco rilevato e presenta
anche risultati entro famiglia, senza confondere correlazione con causalità.
R2L/U2R: tutti i sottotipi del test inclusi, con denominatori espliciti e cautela
per supporti minimi. Nessun nuovo fit, tuning, modifica target o aggiornamento PDF.


## 7 novembre 2026 — T40 e T41

Completata diagnosi dei falsi allarmi: notebook24 e FALSE_ALARMS_AND_CONCLUSIONS.md.
Predizioni storiche verificate, nessun nuovo fit. NB:3813/9711 falsi allarmi,
3642 esclusivi; HTTP3276/6673, ftp_data295/320. Conteggi e tassi distinti.
Proposta: chiudere il primo confronto NSL-KDD; ulteriori esperimenti da concordare,
scelte soltanto su validation del training. Test ufficiale già consultato.
Verifica: kernel pulito e audit indipendente su tutti i gruppi/destinazioni/accordo.
PDF invariato in questo blocco; contiene già T38–T39 prima della bibliografia.
