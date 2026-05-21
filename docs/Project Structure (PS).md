# Project Structure (PS)

Questa sezione presenta in modo chiaro e organizzato la struttura del progetto **Faller Web Harvester**, evidenziando la funzione delle principali cartelle e dei file che compongono l’applicazione.  

La struttura è progettata secondo criteri di modularità, separazione delle responsabilità e aderenza ai pattern architetturali tipici delle applicazioni Flask.

---

## Root del progetto

```text
faller-web-harvester/                                      # Root principale del progetto (Faller Web Harvester)
│
├── docs/                                                  # Documentazione tecnica e diagrammi del progetto
│   ├── images/                                            # Diagrammi esportati in formato immagine (.png, .jpg)
│   │   ├── architecture_overview.png                      # Diagramma visuale dell'architettura N-Tier del sistema
│   │   ├── classDiagram.png                               # Diagramma delle classi UML
│   │   ├── erDiagram.png                                  # Diagramma Entità-Relazione (ERD) per il database
│   │   ├── Gantt.JPG                                      # Pianificazione e cronoprogramma delle attività (Gantt)
│   │   └── usecase.png                                    # Diagramma dei Casi d'Uso
│   │
│   ├── mermaid/                                           # File sorgente in codice Mermaid per la generazione dei diagrammi
│   │   ├── architecture_overview.mmd                      # Codice Mermaid del diagramma architetturale a livelli
│   │   ├── classDiagram.mmd                               # Codice Mermaid del diagramma delle classi
│   │   ├── concept_map.mmd                                # Codice Mermaid della mappa concettuale
│   │   ├── erDiagram.mmd                                  # Codice Mermaid del diagramma Entità-Relazione
│   │   └── gantt.mmd                                      # Codice Mermaid del diagramma di Gantt
│   │
│   ├── Cross-Disciplinary Mapping (CDM).md                # Documento di mappatura interdisciplinare delle competenze
│   ├── Executive Summary (ES).md                          # Sintesi esecutiva e obiettivi di alto livello del progetto
│   ├── Project Postmortem (PP).md                         # Analisi critica dell'evoluzione del software e bilancio finale
│   ├── Project Structure (PS).md                          # Descrizione dell'albero delle directory
│   ├── Software Requirements Specification (SRS).md       # Specifica dei requisiti software (funzionali e non)
│   ├── Test Suite.md                                      # Guida alla validazione e configurazione dei test unitari (Pytest)
│   └── usecase.puml                                       # Sorgente PlantUML del diagramma dei Casi d'Uso
│   
├── webapp/                                                # Core directory contenente il codice sorgente dell'applicazione Flask
│   ├── __init__.py                                        # Inizializzazione del pacchetto e configurazione dell'Application Factory
│   ├── config.py                                          # File di configurazione delle variabili d'ambiente (lingua, DB, secret key)
│   ├── db.py                                              # Logica di gestione, apertura e chiusura delle connessioni al database
│   ├── extensions.py                                      # Definizione delle estensioni Flask esterne istanziate globalmente
│   ├── pytest.ini                                         # File di configurazione globale per il framework di testing pytest
│   ├── schema.sql                                         # Script SQL di inizializzazione per la creazione delle tabelle del database
│   │
│   ├── blueprints/                                        # Moduli isolati dell'applicazione per una gestione pulita delle rotte
│   │   ├── admin/                                         # Blueprint dedicato all'amministrazione del sistema
│   │   │   ├── __init__.py                                # Inizializzazione e registrazione del Blueprint Admin
│   │   │   └── routes.py                                  # Gestione delle rotte per la dashboard amministratore
│   │   │
│   │   ├── api/                                           # Blueprint per gli endpoint API REST dell'applicazione
│   │   │   ├── __init__.py                                # Inizializzazione e registrazione del Blueprint API
│   │   │   ├── scraping_api                               # Rotte API asincrone per monitorare e avviare l'estrazione dati
│   │   │   └── export_api.py                              # Rotte API per il download e l'esportazione dei report
│   │   │
│   │   ├── auth/                                          # Blueprint per la gestione dell'autenticazione utenti
│   │   │   ├── __init__.py                                # Inizializzazione e registrazione del Blueprint Auth
│   │   │   └── routes.py                                  # Rotte per login, registrazione utente e logout
│   │   │
│   │   ├── errors/                                        # Blueprint centralizzato per la gestione degli errori HTTP
│   │   │   ├── __init__.py                                # Inizializzazione e registrazione del Blueprint Errors
│   │   │   └── handlers.py                                # Funzioni di intercettazione ed elaborazione degli errori (es. 404, 500)
│   │   │
│   │   ├── harvester/                                     # Blueprint per la gestione del core di scraping e ricerca prodotti
│   │   │   ├── __init__.py                                # Inizializzazione e registrazione del Blueprint Harvester
│   │   │   └── routes.py                                  # Rotte per le interfacce di scraping e i filtri di ricerca
│   │   │
│   │   └── main/                                          # Blueprint principale per le pagine statiche e di atterraggio
│   │       ├── __init__.py                                # Inizializzazione e registrazione del Blueprint Main
│   │       └── routes.py                                  # Rotte per la homepage e la dashboard utente generica
│   │
│   ├── models/                                            # Classi che mappano le entità del database (Modelli DTO/POJO)
│   │   ├── __init__.py                                    # Inizializzazione del pacchetto dei modelli
│   │   ├── product.py                                     # Modello per la struttura dati dei codici e prodotti Faller
│   │   └── user.py                                        # Modello per la gestione delle credenziali e dei ruoli degli utenti
│   │
│   ├── repositories/                                      # Pattern Repository per l'isolamento delle query SQL dal livello business
│   │   ├── __init__.py                                    # Inizializzazione del pacchetto repository
│   │   └── product_repository.py                          # Query specifiche CRUD e filtri complessi per la tabella prodotti
│   │
│   ├── services/                                          # Livello dei servizi per l'implementazione della logica di business
│   │   ├── __init__.py                                    # Inizializzazione del pacchetto servizi
│   │   ├── auth_logic.py                                  # Logica applicativa di validazione credenziali e sessioni utente
│   │   │
│   │   ├── io/                                            # Sotto-servizi dedicati alla gestione dell'I/O, export e file system
│   │   │   ├── __init__.py                                # Inizializzazione del modulo I/O
│   │   │   ├── archiver.py                                # Logica per la compressione in file .ZIP di media e dati estratti
│   │   │   ├── downloader.py                              # Logica per scaricare in locale i media (immagini, istruzioni PDF)
│   │   │   ├── excel_builder.py                           # Generazione dinamica di fogli di calcolo Excel con i dati strutturati
│   │   │   └── validators.py                              # Controlli di integrità e validazione dei file in ingresso/uscita
│   │   │
│   │   └── scraper/                                       # Core engine del web crawler e parser del catalogo Faller
│   │       ├── __init__.py                                # Inizializzazione del modulo di scraping
│   │       ├── client.py                                  # Gestione delle richieste HTTP, sessioni e gestione degli errori di rete
│   │       ├── parser.py                                  # Estrazione dei dati testuali grezzi e strutturazione delle informazioni
│   │       └── selectors.py                               # Definizione centralizzata dei selettori CSS/XPath (configurati solo per l'inglese)
│   │
│   ├── static/                                            # Asset statici serviti direttamente dal server web Flask
│   │   ├── css/                                           # Fogli di stile CSS per il layout grafico
│   │   │   ├── admin_dashboard.css                        # Stili dedicati ed esclusivi per il pannello di controllo admin
│   │   │   ├── style.css                                  # Layout e regole di stile globali per l'intera applicazione
│   │   │   └── user_dashboard.css                         # Interfaccia grafica personalizzata per le dashboard utente
│   │   │
│   │   ├── gif/                                           # Icone animate in formato GIF per l'interfaccia utente
│   │   │   ├── DATABASE_icon.gif                          # Icona animata per la sezione dello stato del database
│   │   │   ├── IMAGE_icon.gif                             # Icona animata per i box relativi alle immagini dei prodotti
│   │   │   ├── INFO_icon.gif                              # Elemento grafico per i dettagli o tooltip informativi
│   │   │   ├── PDF_icon.gif                               # Icona animata per i link ai manuali d'istruzione PDF
│   │   │   ├── SCRAPER_icon.gif                           # Feedback visivo per lo stato del processo di scraping in esecuzione
│   │   │   ├── TRASH_icon.gif                             # Elemento grafico di animazione per l'eliminazione dei record
│   │   │   └── ZIP_icon.gif                               # Icona animata per la sezione download degli archivi compressi
│   │   │
│   │   ├── img/                                           # Risorse grafiche e immagini statiche (.png, .jpg, .ico)
│   │   │   ├── EXCEL_icon.png                             # Icona pulsante per l'esportazione in foglio Excel
│   │   │   ├── FALLER_logo.jpg                            # Logo ufficiale della Gebr. Faller GmbH usato nella UI
│   │   │   ├── WEB_HARVESTER.jpg                          # Immagine o banner principale dell'applicazione
│   │   │   └── favicon.ico                                # Icona del sito visualizzata nella scheda del browser
│   │   │
│   │   └── js/                                            # Script JavaScript per la logica lato client e chiamate AJAX
│   │       ├── admin_dashboard.js                         # Logica JS per i grafici e la gestione utenti lato amministratore
│   │       ├── change_password.js                         # Validazione in tempo reale e invio form cambio password
│   │       ├── login.js                                   # Gestione form di autenticazione e messaggi di errore
│   │       ├── register.js                                # Controlli sui requisiti di sicurezza password in fase di registrazione
│   │       ├── scraper_range.js                           # Script per gestire la selezione o lo slider del range di codici prodotto
│   │       ├── scraper.js                                 # Chiamate AJAX asincrone per avviare il processo di harvester senza ricaricare la pagina
│   │       └── user_dashboard.js                          # Gestione della tabella dinamica e dei download dell'utente
│   │
│   ├── templates/                                         # Modelli HTML strutturati tramite il motore di templating Jinja2
│   │   ├── base.html                                      # Template scheletro globale contenente Navbar, Footer e script comuni
│   │   │
│   │   ├── admin/                                         # Viste riservate al ruolo di amministratore
│   │   │   └── dashboard.html                             # Pagina di monitoraggio dei log di sistema e delle metriche DB
│   │   │
│   │   ├── auth/                                          # Viste per i form dei flussi di autenticazione
│   │   │   ├── change_password.html                       # Pagina per la modifica delle proprie credenziali
│   │   │   ├── login.html                                 # Pagina di accesso al portale
│   │   │   └── register.html                              # Pagina per la creazione di un nuovo account
│   │   │
│   │   ├── errors/                                        # Pagine di errore personalizzate destinate agli utenti
│   │   │   ├── 404.html                                   # Interfaccia user-friendly per risorsa o pagina non trovata
│   │   │   └── 500.html                                   # Interfaccia di cortesia in caso di errore interno del server
│   │   │
│   │   ├── harvester/                                     # Viste operative del sistema di estrazione dati
│   │   │   ├── scraper.html                               # Pannello di controllo per configurare e lanciare l'harvester
│   │   │   └── search.html                                # Pagina di consultazione avanzata e filtri del catalogo archiviato
│   │   │
│   │   └── main/                                          # Viste pubbliche o di atterraggio standard
│   │       ├── dashboard.html                             # Riepilogo delle attività e storico download dell'utente
│   │       └── index.html                                 # Landing page di presentazione del software
│   │
│   ├── tests/                                             # Suite di test automatizzati per garantire la stabilità del codice
│   │   ├── __init__.py                                    # Inizializzazione del pacchetto dei test unitari ed e2e
│   │   ├── conftest.py                                    # Configurazione dell'ambiente e delle fixture (App e Client)
│   │   ├── test_archiver.py                               # Test per la creazione degli archivi ZIP
│   │   ├── test_auth.py                                   # Test di registrazione, login ed edge cases
│   │   ├── test_export.py                                 # Test per l'esportazione dei report in Excel
│   │   ├── test_media.py                                  # Test per il download e l'organizzazione dei media
│   │   ├── test_repository.py                             # Test del DB SQLite e dei vincoli di integrità
│   │   ├── test_scraper.py                                # Test del parser (versione Inglese) con Mocking di rete
│   │   ├── test_routes.py                                 # Test di accesso alle pagine e protezione dei Blueprint
│   │   ├── test_security.py                               # Test delle funzioni di hashing e cifratura password
│   │   └── test_validators.py                             # Test per i controlli di integrità sui file e input
│   │
│   └── utils/                                             # Script di utilità generale riutilizzabili nel progetto
│       ├── __init__.py                                    # Inizializzazione del modulo utility
│       └── security.py                                    # Funzioni di hashing delle password (es. scrypt/bcrypt) e sanificazione input
│
├── .gitignore                                             # File per escludere file non necessari da Git
├── .gitattributes                                         # Configurazione degli attributi dei tracciamenti dei file su Git
├── LICENSE                                                # Licenza del progetto
├── README.md                                              # Descrizione generale e istruzioni
├── requirements.txt                                       # Elenco delle dipendenze Python
└── run.py                                                 # Entry point per avviare l'applicazione
```

## Analisi delle Scelte Architetturali

A seguito dell'analisi della struttura del file-tree, si evidenziano tre scelte fondamentali che rispondono ai requisiti di qualità del software, manutenibilità e scalabilità:

* **Adozione del Pattern Application Factory & Blueprints:** L'inizializzazione dell'applicazione all'interno di `webapp/__init__.py` evita riferimenti circolari e permette di isolare i contesti operativi. La suddivisione in moduli (`admin`, `api`, `auth`, `errors`, `harvester`, `main`) garantisce che ogni macro-funzionalità gestisca in autonomia le proprie rotte e la propria logica visiva.
* **Separazione Netta dei Livelli (Separation of Concerns):** Il livello dei **Modelli** (`models/`) definisce puramente la struttura dei dati.
  * Il livello dei **Repository** (`repositories/`) isola le query SQL grezze (`schema.sql`), impedendo alla logica di business di comunicare direttamente con la persistenza.
  * Il livello dei **Servizi** (`services/`) centralizza l'algoritmo core dell'harvester, del parser e della gestione I/O, mantenendo i controllori delle rotte (i file `routes.py`) estremamente snelli e focalizzati solo sulle risposte HTTP.
* **Isolamento dell'Infrastruttura di Testing:** La presenza di una cartella `tests/` speculare alla struttura dei servizi, supportata dalla configurazione centralizzata di `pytest.ini` e `conftest.ini`, garantisce la possibilità di eseguire test di unità e di integrazione (mockando il database e le risposte HTTP del server target) senza sporcare l'ambiente di produzione o il codice sorgente.

---

## Guida alla Lettura e Navigazione della Documentazione

Per i revisori o gli sviluppatori che si interfacciano con il progetto **Faller Web Harvester** per la prima volta, si consiglia di consultare i file presenti nella cartella `docs/` seguendo questo ordine logico e propedeutico:

1. **[Executive Summary (ES)](./Executive%20Summary%20(ES).md):** Il punto di partenza ideale. Offre una panoramica ad alto livello degli obiettivi di business, del contesto di applicazione (automazione del catalogo del plastico ferroviario) e delle scelte strategiche del sistema.
2. **[Software Requirements Specification (SRS)](./Software%20Requirements%20Specification%20(SRS).md):** Fornisce un'analisi dettagliata e formale dei requisiti funzionali (funzionamento dello scraping, export, download dei media) e non funzionali (sicurezza delle password, performance, vincoli tecnologici di Flask e SQLite).
3. **[Project Structure (PS)](./Project%20Structure%20(PS).md):** *Questo documento.* Illustra come i requisiti definiti nell'SRS si traducono fisicamente in file e cartelle sul file system, rispettando i pattern architetturali di modularità.
4. **[Cross-Disciplinary Mapping (CDM)](./Cross-Disciplinary%20Mapping%20(CDM).md):** Collega le componenti tecniche del software con le competenze interdisciplinari e gestionali, mostrando l'impatto organizzativo del progetto.
5. **[Test Suite](./Test%20Suite.md)**: Documentazione dei test unitari (Pytest) per la validazione dello scraper. La suite garantisce l'integrità del codice ed è composta dai seguenti moduli di verifica:
    * [Configurazione e Fixture (`conftest.py`)](../webapp/tests/conftest.py): Gestione del ciclo di vita del database SQLite di test e isolamento delle cartelle multimediali.
    * [Validazione Input (`test_validators.py`)](../webapp/tests/test_validators.py): Verifica dei codici prodotto Faller (da 4 a 8 cifre), estensioni consentite e integrità tramite hash MD5.
    * [Logica di Autenticazione (`test_auth.py`)](../webapp/tests/test_auth.py): Controllo dei flussi di registrazione, credenziali errate e gestione degli utenti duplicati.
    * [Motore di Scraping (`test_scraper.py`)](../webapp/tests/test_scraper.py): Testing isolato dalla rete tramite mock per la verifica del parsing della versione inglese del catalogo.
    * [Strato di Persistenza (`test_repository.py`)](../webapp/tests/test_repository.py): Convalida delle query CRUD e della gestione della logica di `UPSERT` sui vincoli di unicità di SQLite.
    * [Sicurezza e Ruoli (`test_security.py`)](../webapp/tests/test_security.py): Verifica dei permessi di accesso basati sui ruoli (RBAC) per la protezione dell'area `/admin/`.
    * [Rotte e Endpoint (`test_routes.py`)](../webapp/tests/test_routes.py): Controllo del routing di Flask, accessibilità della Landing Page e degli endpoint di progresso.
    * [Gestione File Multimediali (`test_media.py`)](../webapp/tests/test_media.py): Controllo del salvataggio locale e dell'organizzazione su disco di immagini (`_main.jpg`) e PDF.
    * [Generazione Report (`test_export.py`)](../webapp/tests/test_export.py): Validazione della struttura e della corretta scrittura dei file report Excel (`.xlsx`).
    * [Modulo di Compressione (`test_archiver.py`)](../webapp/tests/test_archiver.py): Verifica della creazione automatica degli archivi compressi ZIP per il download.

---

*Nota: Tutti i diagrammi visivi a supporto della comprensione architettonica (UML, ERD, Casi d'Uso e diagramma di Gantt per la pianificazione temporale) sono disponibili sia in formato sorgente testuale modificabile nella cartella `docs/mermaid/` sia come esportazioni grafiche pronte alla consultazione in `docs/images/`.*