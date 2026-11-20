# Etichette grezze e target a cinque famiglie

Ordine di report e matrici: **Normal, DoS, Probe, R2L, U2R**. `attack_label` originale resta
intatta; `family` è un target derivato in memoria, mai una feature. `difficulty` è esclusa da X.
Implementazione: `src/targets.py`. Non normalizziamo punti finali, maiuscole o spazi di nascosto:
etichette mancanti o ignote causano ValueError; nessuna assegnazione generica e nessuna riga scartata.

## Mappa completa adottata

| Famiglia | Normal e attacchi nel training | Attacchi presenti soltanto nel test |
|---|---|---|
| Normal | normal | — |
| DoS | back, land, neptune, pod, smurf, teardrop | apache2, mailbomb, processtable, udpstorm, worm |
| Probe | ipsweep, nmap, portsweep, satan | mscan, saint |
| R2L | ftp_write, guess_passwd, imap, multihop, phf, spy, warezclient, warezmaster | httptunnel, named, sendmail, snmpgetattack, snmpguess, xlock, xsnoop |
| U2R | buffer_overflow, loadmodule, perl, rootkit | ps, sqlattack, xterm |

Copertura verificata sulle label effettive: tutte le 40 etichette dell’unione train/test coperte,
incluse le 17 test-only. Non è un confronto di distribuzioni o una valutazione del test ufficiale.

## Provenienza e incertezza

| Ambito | Fonte e grado di certezza |
|---|---|
| 22 attacchi train | Associazioni esplicite della fonte primaria [UCI training_attack_types](https://kdd.ics.uci.edu/databases/kddcup99/training_attack_types). `normal→Normal` è l’etichetta di traffico normale. |
| apache2, mailbomb, processtable, udpstorm | Sezione DoS del [database attacchi DARPA, MIT Lincoln Laboratory](https://archive.ll.mit.edu/ideval/docs/attackDB.html); Process Table corrisponde alla label processtable. |
| mscan, saint | Sezione Probes dello stesso database primario MIT. |
| httptunnel, named, sendmail, xlock, xsnoop | Sezione Remote to Local del database MIT; adottiamo quindi R2L, esplicitamente. Altre tassonomie pubblicate possono classificare httptunnel diversamente: non presumiamo l’equivalenza di tutti i benchmark. |
| ps, xterm | Sezione User to Root del database MIT. |
| worm→DoS, snmpgetattack/snmpguess→R2L, sqlattack→U2R | **Convenzioni operative del progetto, da confermare prima del benchmark sul test.** Le fonti primarie consultate non danno una tabella completa che determini queste quattro label. Non le presentiamo come associazioni certificate da UNB/Divekar. |

Questa incertezza riguarda solo attacchi assenti dal training e non influisce sulle metriche
train/validation di questo traguardo. Conserviamo le label grezze, così una futura convenzione
verificata non richiederà di ricostruire i dati. Il confronto futuro dovrà fissare esplicitamente
le famiglie delle etichette test-only prima di misurare il test e confrontarsi con Divekar.

## Verifica T27 — convenzione del codice autore

Il 5 novembre 2026 è stato verificato il dizionario NSL del repository Divekar,
fissato a un commit e confrontato su tutte le 40 etichette del progetto.
Le quattro associazioni inizialmente da chiarire sono esplicite nel codice autore:
worm→R2L, snmpgetattack/snmpguess→R2L, sqlattack→U2R. Sono differenze rispetto alla
mappa attuale worm (DoS nel progetto) e httptunnel (R2L nel progetto, U2R autore).
Gli altri 38 mapping coincidono. La famiglia MIT di httptunnel resta R2L:
convenzione autore e tassonomia del produttore vanno distinte.

La tabella adottata e src/targets.py restano quelli degli esperimenti precedenti.
T27 è documentale: non applica una nuova mappa al test. Prima della futura
valutazione va dichiarata la convenzione scelta; non sceglierla dalle metriche.
Fonti puntuali, grado di certezza e limiti in [AUTHOR_CODE_AUDIT.md](AUTHOR_CODE_AUDIT.md).


## Profilo autore per il test ufficiale — T29

`AUTHOR_ATTACK_TO_FAMILY` in src/targets.py è una copia separata: worm → R2L,
httptunnel → U2R. `ATTACK_TO_FAMILY` e attack_to_family restano quelli storici.
Notebook 14 applica il profilo autore con Series.map dopo il controllo delle label.
Training invariato; nel test cambiano 2 worm e 133 httptunnel. Totali autore:
Normal 9711, DoS 7458, Probe 2421, R2L 2754, U2R 200.
Fonte e limiti della convenzione: AUTHOR_CODE_AUDIT.md. Nessuna certificazione
di tassonomia universale; il profilo è dichiarato per il confronto con gli autori.
