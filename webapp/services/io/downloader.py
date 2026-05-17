import os
import requests
from webapp.config import Config

def download_file(url, folder_path, filename):
    # Scarica un file da URL e lo salva nella cartella indicata.
    # - Normalizza gli URL relativi (// e /)
    # - Evita i download duplicati se il file esiste già
    # - Usa stream=True per non caricare tutto in RAM
    # - Scarta i file troppo piccoli (icone, placeholder, errori HTML)
    # - Restituisce il nome del file salvato oppure None in caso di errore

    # Verifica dell'input valido
    if not url or not isinstance(url, str):
        return None

    # 1. NORMALIZZAZIONE URL
    # Gestione URL che iniziano con "//" → aggiunge protocollo https
    if url.startswith("//"):
        url = "https:" + url

    # Gestione URL relativi "/path" → li aggancia alla BASE_URL del sito
    elif url.startswith("/"):
        url = Config.BASE_URL + url

    # 2. COSTRUZIONE PERCORSO DI SALVATAGGIO
    file_path = os.path.join(folder_path, filename)

    # Se il file esiste già, evita download inutili
    if os.path.exists(file_path):
        return filename

    # Crea la cartella se non esiste
    os.makedirs(folder_path, exist_ok=True)

    # 3. DOWNLOAD DEL FILE
    try:
        # Header dinamico con User-Agent randomizzato
        headers = Config.get_random_headers()

        # stream=True → scarica a blocchi, utile per PDF e immagini grandi
        r = requests.get(url, headers=headers, timeout=15, stream=True)

        # Se il server risponde con errore, si interrompe
        if r.status_code != 200:
            return None

        # Controllo della dimensione minima per evitare file inutili (es. 1x1 pixel)
        content_length = int(r.headers.get("content-length", 0))
        if 0 < content_length < 1024:
            return None

        # Scrittura sul disco a chunk per evitare un uso eccessivo della RAM
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk: # Evita chunk vuoti
                    f.write(chunk)

        return filename

    except Exception as e:
        # Log minimale per il debugging (non interrompe il flusso)
        print(f"[Downloader] Errore scaricando {url}: {e}")
        return None