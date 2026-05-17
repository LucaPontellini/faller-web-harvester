import requests
from bs4 import BeautifulSoup
import time
import re
from webapp.config import Config

# Effettua una richiesta HTTP con header randomizzati e timeout.
# Ritorna un oggetto BeautifulSoup oppure None in caso di errore.
# Include retry progressivi per maggiore stabilità.
def get_soup(url, retries=3):
    for i in range(retries):
        try:
            r = requests.get(
                url,
                headers=Config.get_random_headers(), # User-Agent rotation
                timeout=20
            )
            r.raise_for_status()

            # Usa lxml se disponibile, altrimenti html.parser
            return BeautifulSoup(
                r.text,
                "lxml" if "lxml" in str(BeautifulSoup) else "html.parser"
            )

        except Exception as e:
            # Attesa progressiva prima del retry
            if i < retries - 1:
                time.sleep((i + 1) * 2)
            else:
                print(f"Errore connessione: {url} -> {e}")
                return None

    return None

# Cerca un codice prodotto sul sito Faller.
# Restituisce l'URL del prodotto se trovato.
# Gestisce sia:
#   1) pagine di lista dei risultati
#   2) redirect diretto alla pagina del prodotto
def search_code(code):
    search_url = f"{Config.BASE_SEARCH}{code}"
    soup = get_soup(search_url)

    if not soup:
        return None

    try:
        # 1. CASO: LISTA RISULTATI
        products = soup.select(".product--box a")

        for link in products:
            href = link.get("href", "")
            text = link.get_text(strip=True)

            # Match affidabile: codice nel testo o nell'URL
            if code in text or re.search(rf"(-|/){code}(/|$|\?)", href):

                # Se è un link assoluto lo si usa direttamente
                if href.startswith("http"):
                    return href

                # Altrimenti costruisce l'URL completo
                return f"{Config.BASE_URL}/{href.lstrip('/')}"

        # 2. CASO: REDIRECT DIRETTO ALLA PAGINA PRODOTTO
        if soup.select_one("h1.product--title"):
            # La search URL spesso è già la pagina prodotto
            r = requests.get(
                search_url,
                headers=Config.get_random_headers(),
                allow_redirects=True,
                timeout=10
            )
            return r.url

    except Exception as e:
        print(f"Errore search_code({code}): {e}")

    return None