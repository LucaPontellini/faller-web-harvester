## Executive Summary (ES)

Il progetto *Faller Web Harvester* è un sistema sviluppato in Python per automatizzare la raccolta, l’estrazione e l’organizzazione dei dati relativi ai prodotti del catalogo [Gebr. Faller GmbH](https://www.faller.de/en/). Nasce per sostituire un processo manuale lento e soggetto a errori, utilizzato per mantenere aggiornato il catalogo del plastico ferroviario di famiglia (vedi [Contesto](./Software%20Requirements%20Specification%20(SRS).md#12-contesto)).

Il sistema esegue automaticamente il **web scraping** delle pagine prodotto, recuperando informazioni tecniche, immagini e documentazione PDF. I dati vengono salvati in modo persistente e organizzati in formati facilmente consultabili, come tabelle relazionali, fogli di calcolo **Excel** e **archivi ZIP** compressi, garantendo una gestione efficiente, rapida e strutturata dell'inventario (vedi [Requisiti Funzionali](./Software%20Requirements%20Specification%20(SRS).md#4-requisiti-funzionali)).

L’obiettivo principale è azzerare il lavoro manuale, garantire aggiornamenti costanti del catalogo e migliorare drasticamente la qualità, l'integrità e la coerenza delle informazioni raccolte.

### Vincoli di Ambito e Internazionalizzazione

A livello strategico e architetturale, **il sistema è configurato per operare esclusivamente sulla versione in lingua inglese del catalogo ufficiale Faller**. Questa scelta risponde a due esigenze precise:

1. **Normalizzazione del Dato:** Evita la ridondanza, i conflitti e l'incoerenza informativa derivanti dal parsing simultaneo di più lingue, garantendo un database standardizzato con terminologie tecniche uniformi ed universalmente riconosciute nel settore del modellismo ferroviario.
2. **Integrità del Parser:** Mitiga le anomalie strutturali, i refusi e i disallineamenti occasionali presenti nel codice HTML delle versioni localizzate del sito web target, garantendo una stabilità assoluta dei selettori CSS/XPath centralizzati nel software.

### Architettura del Sistema

Il progetto è stato realizzato seguendo un’architettura modulare a strati basata sul micro-framework **Flask**, che separa nettamente le responsabilità tra scraping, memorizzazione e presentazione (vedi [Project Structure (PS)](./Project%20Structure%20(PS).md)):

- **Interfaccia Web (Flask Blueprints):** Un pannello di controllo intuitivo diviso in moduli isolati per gestire l'autenticazione degli utenti (`auth`), configurare i range di codici per l'harvester (`harvester`) e monitorare lo stato del sistema.
- **Persistenza Dati (SQLite & Repository Pattern):** Un database relazionale locale per l'indicizzazione rapida dei prodotti archiviati, completamente isolato dalla logica di business tramite repository dedicati per garantire massima manutenibilità.
- **Core Engine (Scraper/Parser & I/O):** Moduli specializzati nella gestione asincrona delle richieste HTTP, nella validazione dei flussi di dati e nella generazione dinamica dei report Excel e degli archivi multimediali.

Tali specifiche tecniche e i relativi vincoli sono descritti approfonditamente nella [Software Requirements Specification (SRS)](./Software%20Requirements%20Specification%20(SRS).md).

---

## Riferimenti ai file del progetto

- [**Script principale**](../run.py)
- [**README del progetto**](../README.md)
- [**Software Requirements Specification (SRS)**](./Software%20Requirements%20Specification%20(SRS).md)
- [**Project Structure (PS)**](./Project%20Structure%20(PS).md)
- [**Cross-Disciplinary Mapping (CDM)**](./Cross-Disciplinary%20Mapping%20(CDM).md)
- [**Project Postmortem (PP).md**](../docs/Project%20Postmortem%20(PP).md)
- [**Test Suite.md**](../docs/Test%20Suite.md)

---

## Ambito del documento

Questo Executive Summary fornisce una panoramica generale del progetto *Faller Web Harvester* e delle sue linee guida strategiche; non sostituisce in alcun modo il contenuto tecnico dettagliato presente nella [Software Requirements Specification (SRS)](./Software%20Requirements%20Specification%20(SRS).md).