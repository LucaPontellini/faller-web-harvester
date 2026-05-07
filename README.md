# Faller Web Harvester

Sistema di web harvesting per il catalogo Faller, progettato per estrarre automaticamente dati tecnici, immagini e documentazione dal sito ufficiale [Gebr. Faller GmbH](https://www.faller.de/en/). L’architettura è modulare e predisposta per future integrazioni con un database SQLite, un’interfaccia web basata su Flask e l’estensione verso altri siti di modellismo ferroviario.

---

## Funzionalità principali

- Estrazione automatica dei dati dei prodotti dal sito Faller  
- Download di immagini, manuali, schede di sicurezza e layout PDF  
- Esportazione in Excel con anteprime delle immagini e link cliccabili  
- Sistema di cache JSON per ridurre richieste ripetute  
- Generazione di archivi ZIP per facilitare la conservazione e il trasporto dei dati  
- Architettura modulare, pensata per:
  - interfaccia web Flask  
  - integrazione con database SQLite  
  - supporto multi‑catalogo (futuro)

---

## Struttura del progetto

La struttura completa del progetto è documentata nel file dedicato: [Project Structure (PS)](./docs/Project%20Structure%20(PS).md)

---

## Installazione

> ⚠️ *Il progetto è attualmente in sviluppo. La struttura potrebbe evolvere.*

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

```bash
pip install -r requirements.txt
```

### 4. Eseguire lo scraper (quando il file principale sarà aggiunto)

```bash
python faller_scraper.py
```

---

## Utilizzo (stato attuale)

> ⚠️ *Il modulo principale non è ancora stato implementato.  
> Questa sezione descrive il flusso di utilizzo previsto e verrà aggiornata quando il codice sarà disponibile.*

Il funzionamento atteso del sistema, una volta completato, seguirà queste fasi:

1. **Fornire un input di prodotti**, che potrà essere:
   - una lista di codici prodotto (es. `180600`, `130470`, `120290`)
   - una lista di URL diretti alle pagine Faller
   - un *range* di codici (es. `180000–181000`) per scraping massivo

2. **Avviare il processo di scraping**, che includerà:
   - ricerca del prodotto
   - parsing della pagina
   - estrazione dei dati tecnici
   - download di immagini e documenti

3. **Generazione automatica degli output**:
   - **Excel** contenente tutti i dati estratti (testi, specifiche tecniche, immagini in anteprima e link cliccabili)
   - **Archivio ZIP** (opzionale) contenente immagini, PDF e file generati
   - **Cache JSON** per evitare richieste ripetute

Una volta implementato il modulo principale, questa sezione verrà ampliata con:
- esempi pratici  
- screenshot  
- comandi CLI  
- file di input di esempio  

---

## Documentazione

- [Executive Summary (ES)](./docs/Executive%20Summary%20(ES).md)
- [Software Requirements Specification (SRS)](./docs/Software%20Requirements%20Specification%20(SRS).md)
- [Project Structure (PS)](./docs/Project%20Structure%20(PS).md)
- [Cross-Disciplinary Mapping (CDM)](./docs/Cross-Disciplinary%20Mapping%20(CDM).md)
- Manuale utente (User Guide) *(da creare)*
- Test Suite *(da creare)*

---

## Sviluppi futuri

Gli sviluppi futuri previsti per il progetto riguardano principalmente il miglioramento dell’esperienza d’uso e l’estensione delle funzionalità già presenti:

- Interfaccia web basata su Flask per avviare e monitorare lo scraping
- Integrazione con un database SQLite per la memorizzazione dei dati estratti
- Miglioramento del logging e della gestione degli errori
- Ottimizzazione del download di immagini e documenti

Queste funzionalità saranno valutate e implementate in base all’evoluzione del progetto. 

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