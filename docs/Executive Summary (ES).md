## Executive Summary (ES)

Il progetto *Faller Scraper* è un sistema sviluppato in Python per automatizzare la raccolta, l’estrazione e l’organizzazione dei dati relativi ai prodotti del catalogo [Gebr. Faller GmbH](https://www.faller.de/en/).
Nasce per sostituire un processo manuale lento e soggetto a errori, utilizzato per mantenere aggiornato il catalogo del plastico ferroviario di famiglia (vedi [Contesto](./Software%20Requirements%20Specification%20(SRS).md#12-contesto)).

Il sistema esegue automaticamente il **web scraping** delle pagine prodotto, recuperando informazioni tecniche, immagini e documentazione PDF.  
I dati vengono poi organizzati in formati facilmente consultabili, come **Excel**, e **archivi ZIP**, garantendo una gestione più efficiente e strutturata del catalogo (vedi [Requisiti Funzionali](./Software%20Requirements%20Specification%20(SRS).md#4-requisiti-funzionali)).

L’obiettivo principale è ridurre il lavoro manuale, garantire aggiornamenti costanti e migliorare la qualità e la coerenza delle informazioni raccolte.

Il progetto è stato realizzato con un’architettura modulare che separa le responsabilità tra scraping, parsing, download, caching ed esportazione.  
Questa struttura rende il sistema robusto, estensibile e facilmente manutenibile. Sono inoltre previste future estensioni, tra cui:

- un’interfaccia web basata su **Flask**;  
- l’integrazione con un database **SQLite**;

Tali sviluppi sono descritti nei [Requisiti Non Funzionali](./Software%20Requirements%20Specification%20(SRS).md#5-requisiti-non-funzionali).

---

## Riferimenti ai file del progetto

- [**Script principale**](../run.py)
- [**README del progetto**](../README.md)
- [**Software Requirements Specification (SRS)**](./Software%20Requirements%20Specification%20(SRS).md)
- [**Project Structure (PS)**](./Project%20Structure%20(PS).md)
- [**Cross-Disciplinary Mapping (CDM)**](./Cross-Disciplinary%20Mapping%20(CDM).md)

---

## Ambito del documento

Questo Executive Summary fornisce una panoramica generale del progetto *Faller Scraper* e non sostituisce il contenuto tecnico dettagliato presente nella [Software Requirements Specification (SRS)](./Software%20Requirements%20Specification%20(SRS).md).