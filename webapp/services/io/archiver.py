import zipfile
import os
from datetime import datetime
from flask import current_app
from flask.ctx import has_app_context
from webapp.config import Config

def create_archive(specific_codes=None, mode='all'):
    # Crea un archivio ZIP contenente:
    # - immagini (image_main, photo_X, layout_X)
    # - PDF (manuali e sicurezza)

    # Modalità:
    #   mode='all' → include foto + pdf
    #   mode='photos' → solo immagini
    #   mode='docs' → solo pdf

    # Se specific_codes è None → estrae automaticamente i codici dai file presenti in IMG_DIR
    # Restituisce il percorso completo dello ZIP generato.

    # 1. Recupero dei percorsi da Flask (se disponibile) o da Config
    if has_app_context():
        # Se si usa dentro Flask, usa la configurazione dell'app
        export_dir = current_app.config['EXPORT_DIR']
        img_dir = current_app.config['IMG_DIR']
        pdf_dir = current_app.config['PDF_DIR']
    else:
        # Fallback per esecuzioni CLI o script esterni
        export_dir = Config.EXPORT_DIR
        img_dir = Config.IMG_DIR
        pdf_dir = Config.PDF_DIR

    # 2. Nome ZIP con timestamp (evita conflitti)
    zip_name = f"faller_export_{mode}_{datetime.now().strftime('%H%M%S')}.zip"
    zip_path = os.path.join(export_dir, zip_name)

    # Assicura che la cartella export esista
    os.makedirs(export_dir, exist_ok=True)

    # 3. Creazione ZIP
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:

        # Se non sono stati passati codici, li estrae dai file delle immagini
        if not specific_codes:
            if os.path.exists(img_dir):
                # Estrae il codice dal nome file (es: "123456_photo_1.jpg" → "123456")
                specific_codes = list(set([
                    f.split('_')[0].split('.')[0]
                    for f in os.listdir(img_dir)
                    if f and f[0].isdigit() # evita file non validi
                ]))

        # Se ancora non ci sono codici → ZIP vuoto ma valido
        if not specific_codes:
            return zip_path

        # 4. Inserimento dei file per ogni codice
        for code in specific_codes:

            # FOTO + LAYOUT (IMG_DIR)
            if mode in ['all', 'photos'] and os.path.exists(img_dir):
                for f in os.listdir(img_dir):
                    if f.startswith(str(code)):
                        # Struttura interna dello ZIP: <codice>/images/<file>
                        zipf.write(
                            os.path.join(img_dir, f),
                            f"{code}/images/{f}"
                        )

            # PDF (manuali + sicurezza)
            if mode in ['all', 'docs'] and os.path.exists(pdf_dir):
                for f in os.listdir(pdf_dir):
                    if f.startswith(str(code)):
                        # Struttura interna dello ZIP: <codice>/docs/<file>
                        zipf.write(
                            os.path.join(pdf_dir, f),
                            f"{code}/docs/{f}"
                        )

    # Restituisce il percorso completo dello ZIP generato
    return zip_path