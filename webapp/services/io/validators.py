import hashlib
import os

def get_file_hash(path):
    # Calcola l'hash MD5 di un file leggendo il contenuto a blocchi:
    # - Usa blocchi da 4096 byte per evitare di caricare file grandi in memoria.
    # - Restituisce l'hash esadecimale come stringa.
    # - Restituisce None se il file non esiste o se si verifica un errore.
    if not os.path.exists(path):
        return None # File inesistente → impossibile calcolare hash

    hasher = hashlib.md5()

    try:
        # Apertura in modalità binaria per evitare problemi con file non testuali
        with open(path, 'rb') as f:
            # Lettura iterativa a blocchi fino a EOF
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)

        return hasher.hexdigest()

    except Exception as e:
        # In caso di errore (permessi, file corrotto, ecc.)
        print(f"Errore durante il calcolo dell'hash: {e}")
        return None

def is_duplicate(new_file_path, existing_files_dir):
    # Verifica se un file è duplicato confrontando il suo hash con quelli presenti in una cartella:
    # - new_file_path: percorso del file appena caricato.
    # - existing_files_dir: directory dove sono presenti file già salvati.
    # - Restituisce True se trova un file con hash identico.
    new_hash = get_file_hash(new_file_path)
    if not new_hash:
        return False # Se non può calcolare l'hash, non lo si considera duplicato

    # Scorre tutti i file nella directory esistente
    for filename in os.listdir(existing_files_dir):
        existing_path = os.path.join(existing_files_dir, filename)

        # Considera solo file regolari (ignora sottocartelle)
        if os.path.isfile(existing_path):
            if get_file_hash(existing_path) == new_hash:
                return True # Trovato duplicato

    return False  # Nessun duplicato trovato

def validate_product_code(code):
    # Valida un codice prodotto Faller:
    # - Deve contenere solo cifre.
    # - Deve avere almeno 3 caratteri (copre articoli storici e moderni).
    # - Nessun limite massimo: alcuni codici speciali possono essere più lunghi.
    if not code:
        return False # Codice vuoto o None

    code_str = str(code).strip() # Normalizzazione input
    return code_str.isdigit() and len(code_str) >= 3

def validate_allowed_file(filename):
    # Controlla se l'estensione di un file è tra quelle consentite:
    # - Supporta immagini, PDF e file Excel.
    # - Case-insensitive (usa .lower()).
    # - Restituisce True solo se l'estensione è valida.
    ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'jpg', 'jpeg', 'png', 'pdf'}

    if '.' not in filename:
        return False # Nessuna estensione presente

    # Estrae l'estensione dopo l'ultimo punto
    ext = filename.rsplit('.', 1)[1].lower()

    return ext in ALLOWED_EXTENSIONS