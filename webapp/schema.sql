-- database: ../instance/database.db



--  FALLER WEB HARVESTER — STRUTTURA DEL DATABASE

-- Questo database è stato progettato per rappresentare in modo completo e coerente i dati presenti nelle schede prodotto del sito ufficiale Faller (https://www.faller.de/en/). 
-- La struttura è neutrale rispetto alla lingua e permette di memorizzare tutte le informazioni rilevanti così come fornite dal sito.

-- Il sito Faller è disponibile in quattro lingue:
-- • Tedesco (DE)
-- • Inglese (EN)
-- • Francese (FR)
-- • Olandese (NL)

-- Anche se lo scraping attuale utilizza la versione inglese, il modello del database è già compatibile con tutte le varianti linguistiche senza richiedere modifiche aggiuntive.



DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS product;

--  TABELLA UTENTI
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,              -- ID interno dell'utente
    username TEXT UNIQUE NOT NULL,                     -- Nome dell'utente (unico)
    password_hash TEXT NOT NULL,                       -- Hash della password
    role TEXT CHECK(role IN ('user','admin'))          -- Ruolo: user | admin
         NOT NULL DEFAULT 'user'
);

--  TABELLA PRODOTTI
CREATE TABLE product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,              -- ID interno del DB
    code TEXT UNIQUE NOT NULL,                         -- Codice del prodotto (es. 130026)
    "exists" INTEGER DEFAULT 0,                        -- 1 = trovato sul sito Faller, 0 = non trovato
    scale_image TEXT,                                  -- URL dell'immagine della scala (H0, N, Z, G)
    name TEXT,                                         -- Nome del prodotto
    availability TEXT,                                 -- Disponibilità: immediately available | available with waiting time | not available
    price TEXT,                                        -- Prezzo (stringa perché Faller usa formati variabili)
    kit_contains TEXT,                                 -- Contenuto del kit
    dimensions TEXT,                                   -- Dimensioni del modello (mm)
    epoch TEXT,                                        -- Epoca ferroviaria (I, II, III, ...)
    lighting_or_electronics TEXT,                      -- Illuminazione/elettronica (se presente)
    construction_instruction TEXT,                     -- Link delle istruzioni (se non PDF)
    difficulty TEXT,                                   -- Livello di difficoltà
    delivery_date TEXT,                                -- Data di consegna prevista
    category TEXT,                                     -- Categoria del prodotto
    ean TEXT,                                          -- Codice EAN
    description TEXT,                                  -- Descrizione del prodotto
    image_main TEXT,                                   -- Immagine principale
    -- Foto gallery (da 1 fino a 10)
    photo_1 TEXT, photo_2 TEXT, photo_3 TEXT, photo_4 TEXT, photo_5 TEXT,
    photo_6 TEXT, photo_7 TEXT, photo_8 TEXT, photo_9 TEXT, photo_10 TEXT,
    -- Layout / Piante (da 1 fino a 10)
    layout_1 TEXT, layout_2 TEXT, layout_3 TEXT, layout_4 TEXT, layout_5 TEXT,
    layout_6 TEXT, layout_7 TEXT, layout_8 TEXT, layout_9 TEXT, layout_10 TEXT,
    -- PDF
    manual_pdf TEXT,                                   -- PDF delle istruzioni di montaggio
    safety_pdf TEXT,                                   -- PDF delle istruzioni di sicurezza (uguale per tutti i prodotti)
    product_link TEXT,                                 -- Link alla pagina del prodotto sul sito della Faller
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP    -- Timestamp dell'ultimo aggiornamento (utile per il monitoraggio dei cambiamenti)
);