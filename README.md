# Faller Web Harvester

Sistema di web harvesting per il catalogo Faller, progettato per estrarre automaticamente dati tecnici, immagini e documentazione dal sito ufficiale [Gebr. Faller GmbH](https://www.faller.de/en/). L'architettura è full-stack e modulare, basata su un'interfaccia web in Flask e un database SQLite gestito tramite Repository Pattern. Il sistema garantisce una netta separazione tra la logica di scraping, la persistenza dei dati e la presentazione utente.

---

## Funzionalità principali

- **Estrazione automatica dei dati**: Web scraping avanzato delle pagine prodotto del sito Faller per recuperare informazioni tecniche, codici EAN, scale, epoche, ecc. .
- **Gestione Multi-media**: Download e organizzazione sistematica di immagini, manuali d'istruzione, schede di sicurezza e layout in formato PDF.
- **Persistenza su Database**: Archiviazione strutturata dei dati tramite SQLite, implementata con il Repository Pattern per una gestione efficiente delle entità prodotto.
- **Dashboard Web**: Interfaccia di controllo basata su Flask per la gestione dei processi di scraping, la ricerca filtrata dei prodotti e la visualizzazione della cache.
- **Esportazione Professionale**: Generazione di file Excel dettagliati (con anteprime immagini e link) e creazione di archivi ZIP per la portabilità dei dati.
- **Ottimizzazione e Caching**: Sistema di cache per ridurre il numero di richieste al server e gestione delle eccezioni basata su un file di configurazione (config.py) raffinato iterativamente.

---

## Struttura del progetto

La struttura completa del progetto è documentata nel file dedicato: [Project Structure (PS)](./docs/Project%20Structure%20(PS).md)

---

## Installazione

### 1. Creare un ambiente virtuale (consigliato)

```bash
python -m venv venv
```

### 2. Attivare l’ambiente virtuale

| Sistema operativo | Comando |
|-------------------|---------|
| **Windows**       | `venv\Scripts\activate` |
| **macOS / Linux** | `source venv/bin/activate` |

### 3. Installare le dipendenze

Il progetto richiede le librerie elencate in [requirements.txt](requirements.txt) (tra cui Flask, Pandas, BeautifulSoup4, ecc.).

```bash
pip install -r requirements.txt
```

### 4. Avviare l'Applicazione

Il punto di ingresso del sistema è [run.py](run.py), che inizializza l'applicazione Flask e il server locale.

```bash
python run.py
```

Una volta avviato, apri il browser all'indirizzo http://127.0.0.1:5000 per accedere al progetto

---

## Utilizzo 

L'interazione con il sistema avviene attraverso una **Dashboard Web** centralizzata che permette di gestire l'intero ciclo di vita dei dati del catalogo Faller.

### 1. Flusso di Lavoro dell'Utente

L'utente può operare seguendo queste fasi principali:

* **Configurazione Input**: È possibile avviare lo scraping inserendo una lista di **codici prodotto** singoli o definendo un **range numerico** per l'estrazione massiva di intere serie di articoli.
* **Harvesting & Cleaning**: Il sistema esegue il parsing del sito ufficiale, scarica le immagini e la documentazione tecnica, applicando la pulizia dei dati tramite le regole per gestire le incongruenze dell'HTML originale.
* **Consultazione Avanzata**: Attraverso l'interfaccia, è possibile gestire i dati estratti utilizzando filtri specifici:
* **Ricerca e filtraggio per**: Codice Prodotto, EAN, Categoria o Nome Prodotto.
* **Generazione Output**: Esportazione dei dati in formato **Excel** (con anteprime immagini e link) e creazione di **archivi ZIP** pronti per l'uso offline.

### 2. Funzionalità Amministratore (Admin)

L'Amministratore ha accesso a strumenti di gestione per garantire l'integrità del catalogo, operando in modo simile all'utente ma con poteri di supervisione:

* **Manutenzione Dati**: Capacità di modificare o eliminare i dati estratti per correggere eventuali errori persistenti nel database.
* **Supervisione Sistema**: Monitoraggio dell'attività di harvesting e della coerenza tra il database SQLite e i file multimediali (immagini e PDF) salvati localmente.

---

## Documentazione e Risorse

Il progetto è accompagnato da una documentazione tecnica completa, pensata sia per l'analisi funzionale che per la mappatura multidisciplinare:

* **[Executive Summary (ES)](./docs/Executive%20Summary%20(ES).md)**: Visione d'insieme, obiettivi del progetto e contesto (il plastico di famiglia).
* **[Software Requirements Specification (SRS)](./docs/Software%20Requirements%20Specification%20(SRS).md)**: Analisi dettagliata dei requisiti funzionali, non funzionali e casi d'uso.
* **[Project Structure (PS)](./docs/Project%20Structure%20(PS).md)**: Descrizione dell'architettura modulare, dei Blueprints e dei Repository.
* **[Cross-Disciplinary Mapping (CDM)](./docs/Cross-Disciplinary%20Mapping%20(CDM).md)**: Collegamenti tra il progetto e le materie di indirizzo informatico (GPOI, Informatica, Sistemi e Reti, TPSIT e Lingua Inglese).

### Diagrammi e Progettazione

Nella cartella `docs/` sono disponibili i seguenti artefatti grafici:

* **[Diagramma dei Casi d'Uso (UML)](./docs/usecase.puml)**: Flussi Utente e Admin.
* **[Schema Entità-Relazione (ER)](./docs/mermaid/erDiagram.mmd)**: Struttura del database SQLite.
* **[Diagramma delle Classi](./docs/mermaid/classDiagram.mmd)**: Relazioni tra modelli e repository.
* **[Gantt](./docs/mermaid/gantt.mmd)**: Cronoprogramma dello sviluppo.
* **[Project Postmortem (PP)](./docs/Project%20Postmortem%20(PP).md)**: Analisi critica del processo di sviluppo, riflessione sugli obiettivi raggiunti (e le difficoltà incontrate), l'evoluzione architetturale (dalla Fase 0 al sistema attuale) e valutazione finale delle competenze acquisite.
* **[Test Suite](./docs/Test%20Suite.md)**: Documentazione dei test unitari (Pytest) per la validazione dello scraper. La suite garantisce l'integrità del codice ed è composta dai seguenti moduli di verifica:
    * [Configurazione e Fixture (`conftest.py`)](./webapp/tests/conftest.py): Gestione del ciclo di vita del database SQLite di test e isolamento delle cartelle multimediali.
    * [Validazione Input (`test_validators.py`)](./webapp/tests/test_validators.py): Verifica dei codici prodotto Faller (da 4 a 8 cifre), estensioni consentite e integrità tramite hash MD5.
    * [Logica di Autenticazione (`test_auth.py`)](./webapp/tests/test_auth.py): Controllo dei flussi di registrazione, credenziali errate e gestione degli utenti duplicati.
    * [Motore di Scraping (`test_scraper.py`)](./webapp/tests/test_scraper.py): Testing isolato dalla rete tramite mock per la verifica del parsing della versione inglese del catalogo.
    * [Strato di Persistenza (`test_repository.py`)](./webapp/tests/test_repository.py): Convalida delle query CRUD e della gestione della logica di `UPSERT` sui vincoli di unicità di SQLite.
    * [Sicurezza e Ruoli (`test_security.py`)](./webapp/tests/test_security.py): Verifica dei permessi di accesso basati sui ruoli (RBAC) per la protezione dell'area `/admin/`.
    * [Rotte e Endpoint (`test_routes.py`)](./webapp/tests/test_routes.py): Controllo del routing di Flask, accessibilità della Landing Page e degli endpoint di progresso.
    * [Gestione File Multimediali (`test_media.py`)](./webapp/tests/test_media.py): Controllo del salvataggio locale e dell'organizzazione su disco di immagini (`_main.jpg`) e PDF.
    * [Generazione Report (`test_export.py`)](./webapp/tests/test_export.py): Validazione della struttura e della corretta scrittura dei file report Excel (`.xlsx`).
    * [Modulo di Compressione (`test_archiver.py`)](./webapp/tests/test_archiver.py): Verifica della creazione automatica degli archivi compressi ZIP per il download.

---

## Licenza

Il **codice sorgente** di questo progetto è distribuito sotto licenza **MIT**. 

Ciò significa che il software può essere utilizzato, modificato e ridistribuito liberamente, nel rispetto dei termini della licenza.

Il testo completo della licenza è disponibile nel file [LICENSE](./LICENSE).

---

## Note legali

La licenza MIT si applica **esclusivamente al codice sorgente** del progetto.  
I contenuti estratti (immagini, testi, PDF, schede tecniche) rimangono di proprietà dei rispettivi autori e **non sono coperti dalla licenza MIT**.

L’estrazione dei dati avviene nel rispetto delle condizioni d’uso del sito Faller e delle normative vigenti.

Per approfondimenti su aspetti legali ed etici del web scraping, consultare:

- [Sito ufficiale Faller](https://www.faller.de/en/)
- [Informativa sulla privacy (Faller)](https://www.faller.de/en/data-protection)
- [Termini e condizioni d’uso (Faller)](https://www.faller.de/en/terms-and-conditions/)
- [File robots.txt – indicazioni per i crawler](https://www.faller.de/robots.txt)
- [Regolamento generale sulla protezione dei dati (GDPR)](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- [Direttiva UE sul diritto d'autore nel mercato unico digitale](https://eur-lex.europa.eu/eli/dir/2019/790/oj)

Il progetto **non è affiliato né approvato** da Gebr. Faller GmbH.

---

## ⚠️ Dichiarazione di responsabilità

**Il progetto non ha alcuno scopo commerciale.  
Non è destinato alla diffusione pubblica di contenuti protetti da copyright.  
È stato creato esclusivamente per uso personale e didattico.**

Chi utilizza questo software deve farlo **in modo etico e responsabile**, rispettando le condizioni d’uso del sito Faller e le normative europee sul trattamento dei dati e sul web scraping.