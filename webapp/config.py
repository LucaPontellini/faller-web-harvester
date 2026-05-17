import os
import random

class Config:
    
    # ===========================================================================================================================
    # Configurazione centrale del Faller Harvester.
    # Tutti i percorsi, le costanti e le impostazioni globali vengono centralizzate qui per garantire ordine e manutenibilità.
    # ===========================================================================================================================

    # 1. PERCORSI E STORAGE:
    # Percorso assoluto della root del progetto (cartella principale)
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Cartella principale dove verranno salvati immagini, PDF e export
    BASE_STORAGE = os.path.join(PROJECT_ROOT, "faller_catalogo")

    # Directory per immagini scaricate dai prodotti
    IMG_DIR = os.path.join(BASE_STORAGE, "immagini")

    # Directory per i PDF (manuali, istruzioni, documenti tecnici)
    PDF_DIR = os.path.join(BASE_STORAGE, "pdf")

    # Directory dove verranno generati gli ZIP esportati
    EXPORT_DIR = os.path.join(BASE_STORAGE, "export_zip")

    # Nome del file Excel generato dal sistema
    EXCEL_FILENAME = "catalogo_faller.xlsx"

    # Percorso del database SQLite
    DATABASE = os.path.join(PROJECT_ROOT, "instance", "database.db")


    # 2. GENERALI & URL:
    # Chiave segreta Flask (fallback se non impostata come variabile ambiente)
    SECRET_KEY = os.environ.get("SECRET_KEY", "faller-harvester-super-secret")

    # URL base del sito della Faller
    BASE_URL = "https://www.faller.de"

    # URL per la ricerca prodotti in lingua inglese
    BASE_SEARCH = "https://www.faller.de/en/search?sSearch="

    # PDF di sicurezza comune a tutti i prodotti (fornito da Faller)
    STATIC_SAFETY_PDF = (
        "https://medien.faller.de/xs_db/DOKUMENT_DB/www/allgemeines/"
        "FALLER_Sicherheitshinweise_1008010.pdf"
    )


    # 3. MAPPA DELLE LINGUE (EN, DE, FR e NL):
    # Mappatura delle etichette testuali → campi logici del parser.
    # Serve per riconoscere correttamente i campi nelle varie lingue.
    LANG_MAP = {
        "en": {
            "scale": ["track gauge", "gauge", "scale"],
            "epoch": ["epoch", "period"],
            "dimensions": ["dimensions"],
            "kit_contains": [
                "this building kit contains",
                "this kit contains",
                "kit contains",
                "contents"
            ],
            "lighting_or_electronics": ["lighting/electronics", "lighting"],
            "construction_instruction": ["construction instruction"],
            "category": ["category", "kategorie"],
            "ean": ["ean"],
            "difficulty": ["difficulty"],
            "delivery_date": ["delivery date"]
        },

        # Lingua tedesca (parziale, usata solo se necessario)
        "de": {
            "scale": ["spurweite"],
            "epoch": ["epoche"],
            "dimensions": ["maße"],
            "category": ["kategorie"],
            "ean": ["ean"]
        },

        # Francese
        "fr": {
            "scale": ["échelle"],
            "epoch": ["époque"],
            "dimensions": ["dimensions"],
            "category": ["catégorie"],
            "ean": ["ean"]
        },

        # Olandese
        "nl": {
            "scale": ["spoor"],
            "epoch": ["tijdperk"],
            "dimensions": ["afmetingen"],
            "category": ["categorie"],
            "ean": ["ean"]
        }
    }


    # 4. MAPPATURA CAMPI → COLONNE DATABASE:
    # Associazione tra i campi logici estratti dal parser e le colonne del DB
    FIELD_TO_DB_COLUMN = {
        "scale": "scale_image",
        "dimensions": "dimensions",
        "epoch": "epoch",
        "kit_contains": "kit_contains",
        "lighting_or_electronics": "lighting_or_electronics",
        "construction_instruction": "construction_instruction",
        "category": "category",
        "ean": "ean",
        "difficulty": "difficulty",
        "delivery_date": "delivery_date",
    }


    # 5. SELETTORI CSS:
    # Selettori CSS utilizzati dal parser per estrarre informazioni dal sito

    # Selettori CSS: pattern che indicano al parser quali elementi HTML individuare nella pagina per estrarre le informazioni necessarie.
    SELECTORS = {
        # Blocco descrizione prodotto (testo pulito)
        "description_clean": ".product--description-block",

        # Icone della scala (G, H0, N, Z)
        "gauge_icon": ".gauge--H0, .gauge--N, .gauge--Z, .gauge--G",

        # Link ai manuali PDF
        "manual_links": "a.link--download",

        # Prezzo (meta tag strutturato)
        "price_meta": "meta[itemprop='price']"
    }

    # 6. ANTI-BOT - USER AGENTS:
    # Lista di User-Agent realistici per evitare blocchi anti-bot

    # User-Agent: identificano browser, sistema operativo e dispositivo del client.
    # I server li usano per adattare il contenuto e rilevare traffico sospetto.
    # La lista seguente include UA per simulare:
    # - Chrome/Firefox/Edge su Windows
    # - Safari su macOS
    # - Chrome su Linux
    # - Safari su iPhone (mobile iOS)
    # - Chrome su Android (mobile)
    # La rotazione di questi UA riduce i blocchi anti-bot e rende le richieste più credibili.
    USER_AGENTS = [
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        ),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) "
            "Gecko/20100101 Firefox/124.0"
        ),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
        ),
        (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/17.0 Safari/605.1.15"
        ),
        (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        ),
        (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/17.2 Mobile/15E148 Safari/604.1"
        ),
        (
            "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Mobile Safari/537.36"
        )
    ]

    @staticmethod
    def get_random_headers():
        # Restituisce header HTTP con User-Agent casuale e lingua forzata in EN (Inglese)
        return {
            "User-Agent": random.choice(Config.USER_AGENTS),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Referer": Config.BASE_URL,
            "Connection": "keep-alive"
        }

    @staticmethod
    def init_app(app):
        # Crea automaticamente tutte le directory necessarie al funzionamento
        directories = [
            Config.IMG_DIR,
            Config.PDF_DIR,
            Config.EXPORT_DIR,
            os.path.dirname(Config.DATABASE)
        ]
        for directory in directories:
            if directory:
                os.makedirs(directory, exist_ok=True)

# ====================================================
# INFORMAZIONI SUL MULTILINGUA:
# Il sito Faller supporta 4 lingue: DE, EN, FR, NL.
# Il crawler è ottimizzato per l'inglese (/en/).
# Per cambiare lingua modificare:
#   - BASE_SEARCH
#   - Accept-Language in get_random_headers()
# ====================================================