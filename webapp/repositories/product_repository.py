import os
import shutil
from webapp.config import Config
from webapp.db import get_db

# Recupera un prodotto dal database tramite il codice
def find_by_code(code):
    db = get_db()
    return db.execute(
        "SELECT * FROM product WHERE code = ?",
        (code,)
    ).fetchone()

# Salva o aggiorna un prodotto nel database.
# La query è allineata allo schema SQL (40 campi).
def save_product(data):
    db = get_db()

    sql = """
        INSERT OR REPLACE INTO product (
            code, "exists", scale_image, name, availability, price,
            kit_contains, dimensions, epoch, lighting_or_electronics,
            construction_instruction, difficulty, delivery_date,
            category, ean, description, image_main,
            photo_1, photo_2, photo_3, photo_4, photo_5,
            photo_6, photo_7, photo_8, photo_9, photo_10,
            layout_1, layout_2, layout_3, layout_4, layout_5,
            layout_6, layout_7, layout_8, layout_9, layout_10,
            manual_pdf, safety_pdf, product_link
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """

    # Costruzione della lista valori (totale: 40 elementi)
    values = [
        data.get("code"),
        data.get("exists", 1),
        data.get("scale_image"),
        data.get("name"),
        data.get("availability"),
        data.get("price"),
        data.get("kit_contains"),
        data.get("dimensions"),
        data.get("epoch"),
        data.get("lighting_or_electronics"),
        data.get("construction_instruction"),
        data.get("difficulty"),
        data.get("delivery_date"),
        data.get("category"),
        data.get("ean"),
        data.get("description"),
        data.get("image_main"),
    ]

    # Foto gallery (1–10)
    for i in range(1, 11):
        values.append(data.get(f"photo_{i}"))

    # Layout / piante (1–10)
    for i in range(1, 11):
        values.append(data.get(f"layout_{i}"))

    # PDF + link prodotto
    values.extend([
        data.get("manual_pdf"),
        data.get("safety_pdf"),
        data.get("product_link")
    ])

    # Esecuzione delle query
    db.execute(sql, values)
    db.commit()

# Restituisce tutti i prodotti ordinati dal più recente
def get_all_products():
    db = get_db()
    return db.execute(
        "SELECT * FROM product ORDER BY id DESC"
    ).fetchall()

# Cancella un prodotto dal DB e rimuove i file associati (immagini, layout, PDF)
def delete_by_code(code):
    db = get_db()

    # Recupera i dati del prodotto prima della cancellazione
    product = db.execute(
        "SELECT * FROM product WHERE code = ?", (code,)
    ).fetchone()

    if product:
        p = dict(product)

        # Mappatura colonne → cartelle
        file_mapping = {
            Config.IMG_DIR: [
                'image_main',
                'photo_1', 'photo_2', 'photo_3', 'photo_4', 'photo_5',
                'photo_6', 'photo_7', 'photo_8', 'photo_9', 'photo_10',
                'layout_1', 'layout_2', 'layout_3', 'layout_4', 'layout_5',
                'layout_6', 'layout_7', 'layout_8', 'layout_9', 'layout_10'
            ],
            Config.PDF_DIR: [
                'manual_pdf'
            ]
        }

        # Eliminazione fisica dei file
        for folder, columns in file_mapping.items():
            for col in columns:
                filename = p.get(col)

                # Ignora campi vuoti o "N/A"
                if filename and filename != 'N/A' and isinstance(filename, str):
                    file_path = os.path.join(folder, filename)

                    if os.path.exists(file_path):
                        try:
                            os.remove(file_path)
                            print(f"DEBUG: Eliminato file {file_path}")
                        except Exception as e:
                            print(f"ERRORE eliminazione {file_path}: {e}")

    # Cancella il record dal database
    db.execute("DELETE FROM product WHERE code = ?", (code,))
    db.commit()

# Pulisce le cartelle di export (Excel, ZIP, ecc.)
def clear_export_folders():
    folders_to_clean = [
        Config.EXPORT_DIR,
    ]

    for folder in folders_to_clean:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)

                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path) # Elimina i file
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path) # Elimina la cartella
                    print(f"DEBUG: Pulizia export - eliminato {file_path}")
                except Exception as e:
                    print(f"ERRORE pulizia export {file_path}: {e}")
