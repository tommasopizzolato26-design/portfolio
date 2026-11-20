# NF-ToN-IoT-v3 per lo studio temporale del traffico

Per il prossimo esperimento ho scelto **NF-ToN-IoT-v3**. Contiene **27,5 milioni di flussi**, con un flusso per riga, nove tipi di attacco oltre al traffico benigno e timestamp di inizio e fine. Da byte, pacchetti e indirizzi si possono costruire serie per host a intervalli regolari. [Dataset ufficiale](https://rdm.uq.edu.au/files/343e2e8c-6e6e-4a0c-813d-a46acea1b7f4) · [Paper di Luay et al.](https://doi.org/10.1109/ACCESS.2026.3688204)

La prova proposta confronta lo stesso classificatore sugli stessi flussi futuri, con e senza le statistiche del traffico precedente. Le metriche distinguerebbero il riconoscimento dei tipi già osservati, il rilevamento binario di quelli nuovi e i falsi allarmi.

La cattura è di laboratorio. In cinque blocchi cronologici analizzati da Li e Zhou, Scanning, DDoS e XSS ricompaiono in più blocchi. Gli altri sei tipi sono concentrati in un solo blocco ciascuno. Prima del training andranno verificate la copertura delle classi e la continuità delle finestre per host. [Analisi cronologica, tabella A19](https://www.mdpi.com/2079-9292/15/20/4854)
