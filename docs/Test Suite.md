# Guida alla Suite di Test con `pytest`

Questa documentazione descrive la struttura, l'architettura di isolamento e le modalità di esecuzione della suite di test per il progetto **Faller Web Harvester**. 

Il repository ufficiale del progetto è disponibile su: [GitHub - faller-web-harvester](https://github.com/LucaPontellini/faller-web-harvester.git)

---

## 1. Architettura e Isolamento dell'Ambiente (`conftest.py`)

Per evitare che l'esecuzione dei test vada a modificare i dati reali o a creare file persistenti all'interno delle cartelle di produzione, la suite sfrutta un sistema di **fixture** centralizzato nel file `conftest.py`. Questo meccanismo garantisce un ciclo di vita controllato e sicuro attraverso quattro fasi automatiche:

1. **Fase di Setup (Preparazione)**: All'avvio di `pytest`, l'applicazione crea automaticamente una cartella di test isolata denominata `faller_catalogo_test/` e genera una sottocartella temporanea `instance/`.
2. **Fase di Configurazione**: Viene istanziata un'applicazione Flask temporanea con la variabile `TESTING = True`. Le cartelle operative per il salvataggio dei file multimediali vengono temporaneamente mappate all'interno del percorso isolato.
3. **Fase di Inizializzazione**: Viene generato un database SQLite dedicato esclusivamente ai test (`test_database.db`) all'interno di `instance/`, richiamando la funzione `init_db()` per inserire la struttura delle tabelle pulita e l'utente amministratore nativo.
4. **Fase di Teardown (Pulizia finale)**: Una volta terminati tutti i test della suite, il sistema chiude le connessioni attive del database, elimina fisicamente il file `test_database.db` e rimuove l'intera cartella temporanea `faller_catalogo_test/` con tutti i file scaricati durante le simulazioni.

### Gestione dell'Autenticazione nei Test
All'interno di `conftest.py` è definita la classe helper **`AuthActions`**. Questa classe espone i metodi strutturati `login()` e `logout()` per inviare programmaticamente le richieste POST e GET alle rotte di autenticazione, evitando la duplicazione di codice e permettendo di testare i permessi d'accesso in modo pulito.

---

## 2. Copertura dei Moduli di Test

La suite è composta da **22 test automatici**. La tabella seguente associa ogni file di test al relativo obiettivo di validazione e alla logica di controllo implementata:

| File di Test | Obiettivo della Validazione | Logica e Dettagli del Controllo |
| :--- | :--- | :--- |
| **`test_validators.py`** | Validazione dell'Input | Controlla che i codici prodotto Faller siano accettati per lunghezze numeriche variabili da 4 a 8 cifre (es. `110115`, `1201`). Blocca formati non validi (vuoti o alfanumerici). Verifica l'estensione dei file (`.xlsx`, `.jpg`) e il calcolo dell'hash MD5 per identificare file duplicati. |
| **`test_scraper.py`** | Logica di Estrazione (Parsing) | Isola l'applicazione dalla rete esterna simulando le risposte HTTP tramite `unittest.mock.patch`. Verifica la corretta gestione degli errori 404 per codici inesistenti e testa i selettori CSS e la normalizzazione del testo sulla versione inglese del sito Faller. |
| **`test_repository.py`** | Strato di Persistenza (Database) | Convalida le operazioni CRUD sul database tramite il modulo `product_repository`. Verifica che l'inserimento di un codice già esistente non sollevi un blocco bloccante (`IntegrityError`), ma gestisca l'evento come un'operazione di `UPSERT` (aggiornamento dei dati). |
| **`test_security.py`** | Autenticazione e Sicurezza RBAC | Garantisce la protezione basata sui ruoli (Role-Based Access Control). Verifica che un utente con privilegi standard venga respinto (con errore `403` o reindirizzamento) dai percorsi `/admin/`, e che l'admin di sistema configurato acceda regolarmente. |
| **`test_routes.py`** | Endpoint e Routing di Flask | Controlla l'accessibilità della Landing Page pubblica e assicura che gli endpoint API per il tracciamento dello stato di avanzamento dello scraper siano raggiungibili in background. |
| **`test_media.py`** | Gestione degli Asset Multimediali | Simula la scrittura, lo spostamento e l'organizzazione dei file binari scaricati dallo scraper, assicurandosi che le immagini (`_main.jpg`) e i manuali PDF (`_manual.pdf`) siano salvati nei percorsi corretti. |
| **`test_export.py`** | Generazione dei Report Excel | Testa la corretta compilazione del file Excel finale (`.xlsx`) partendo dai metadati estratti (Scala, nome del kit, disponibilità), verificando che il file venga generato, salvato su disco e non risulti corrotto o vuoto. |
| **`test_archiver.py`** | Modulo di Compressione ZIP | Valida la creazione automatica degli archivi compressi `.zip` contenenti i dati esportati, pronti per essere distribuiti o scaricati dall'interfaccia amministrativa. |

---

## 3. Comandi Pratici per l'Esecuzione dei Test

Tutti i comandi elencati di seguito devono essere eseguiti dal terminale posizionato nella radice del progetto, assicurandosi di aver attivato l'ambiente virtuale (`venv`).

### Esecuzione Globale o Silenziosa
* **Eseguire l'intera suite con output dettagliato (Consigliato)**:

```bash
  pytest -v
```

*Mostra l'elenco completo di tutte le funzioni di test e l'esito singolo (`PASSED` o `FAILED`).*

* **Eseguire l'intera suite in modalità silenziosa**:

```bash
pytest -q
```


*Mostra solo un breve riepilogo finale con il conteggio dei test superati.*

### Isolamento ed Esecuzione Mirata

* **Eseguire i test di una specifica cartella**:

```bash
pytest webapp/tests/
```


* **Eseguire un singolo file di test specifico**:

```bash
pytest webapp/tests/test_scraper.py
```


* **Eseguire un singolo test specifico all'interno di un file**:

```bash
pytest webapp/tests/test_validators.py::test_product_code_validation
```


*Utile per concentrarsi sul debug di una singola funzione senza dover rieseguire gli altri controlli.*

### Filtro per Parola Chiave

* **Eseguire i test basandosi sul nome della funzione**:

```bash
pytest -k admin
```


*Esegue tutti i test che contengono la stringa "admin" nel loro nome (es. `test_admin_access_allowed`, `test_admin_restriction_for_normal_user`).*

---

## 4. Configurazione e Risoluzione dei Problemi

### Errore `ModuleNotFoundError: No module named 'webapp'`

Se l'esecuzione di `pytest` si interrompe immediatamente segnalando l'impossibilità di importare il modulo principale `webapp`, significa che l'ambiente Python non include la cartella di lavoro corrente all'interno del percorso di ricerca dei pacchetti.

**Soluzione:**
Assicurati che nella cartella radice del progetto (accanto alla cartella `webapp/`) sia presente il file di configurazione **`pytest.ini`** contenente esattamente le seguenti righe:

```ini
[pytest]
pythonpath = .
```

La direttiva `pythonpath = .` indica a `pytest` di aggiungere la cartella radice al `sys.path` all'avvio, risolvendo i problemi di importazione incrociata tra moduli di test e moduli applicativi.