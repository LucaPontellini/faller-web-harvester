import os
import sqlite3
import threading
from flask import Blueprint, render_template, jsonify, current_app, make_response
from flask_login import login_required
import pandas as pd
from webapp.utils.security import admin_required
from io import BytesIO
from webapp.config import Config

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# STATO GLOBALE DELLO SCRAPER
# Usato per monitorare avanzamento, log e stato dei processi in background.
# Protetto da un lock per evitare race condition.
SCRAPER_STATE = {
    "running": False,
    "progress": 0,
    "log": []
}
state_lock = threading.Lock()

# Connessione al database SQLite dell'app.
# Usa instance_path per compatibilità con Flask
def get_db_connection():
    db_path = os.path.join(current_app.instance_path, 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# DASHBOARD ADMIN
# Carica le statistiche iniziali e mostra la pagina admin
@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    stats = _calculate_stats_logic()
    return render_template(
        "admin/dashboard.html",
        total_products=stats['total_products'],
        total_photos=stats['total_photos'],
        total_pdfs=stats['total_pdfs']
    )

# REST API: stato dello scraper (polling AJAX)
@admin_bp.route("/scraper-progress")
def scraper_progress():
    with state_lock:
        return jsonify(SCRAPER_STATE)

# REST API: statistiche aggiornate
@admin_bp.route('/get-stats')
@login_required
def get_stats():
    return jsonify(_calculate_stats_logic())

# LOGICA CALCOLO STATISTICHE
# Conta prodotti, foto uniche e PDF unici
def _calculate_stats_logic():
    conn = get_db_connection()

    # Totale dei prodotti
    total_products = conn.execute('SELECT COUNT(*) FROM product').fetchone()[0]

    # Colonne delle foto + layout
    photo_columns = (
        ['image_main'] +
        [f'photo_{i}' for i in range(1, 11)] +
        [f'layout_{i}' for i in range(1, 11)]
    )

    # Raccolta dei nomi dei file unici
    all_photos = set()
    for col in photo_columns:
        res = conn.execute(
            f'SELECT DISTINCT "{col}" FROM product WHERE "{col}" IS NOT NULL'
        ).fetchall()
        for r in res:
            all_photos.add(r[0])

    total_photos = len(all_photos)

    # PDF unici (manuale + safety)
    manuals = conn.execute(
        'SELECT DISTINCT manual_pdf FROM product WHERE manual_pdf IS NOT NULL'
    ).fetchall()
    safeties = conn.execute(
        'SELECT DISTINCT safety_pdf FROM product WHERE safety_pdf IS NOT NULL'
    ).fetchall()

    unique_pdfs = {r[0] for r in manuals} | {r[0] for r in safeties}
    total_pdfs = len(unique_pdfs)

    conn.close()

    return {
        'total_products': total_products,
        'total_photos': total_photos,
        'total_pdfs': total_pdfs
    }

# RESET COMPLETO DEL CATALOGO
# Cancella il DB + elimina fisicamente immagini e PDF
@admin_bp.route("/reset-catalog", methods=["POST"])
@login_required
@admin_required
def reset_catalog():

    # Reset dello stato dello scraper
    with state_lock:
        SCRAPER_STATE.update({
            "running": False,
            "progress": 0,
            "log": ["[INFO] Avvio reset totale catalogo..."]
        })

    try:
        # Svuota la tabella dei prodotti
        conn = get_db_connection()
        conn.execute('DELETE FROM product')
        conn.commit()
        conn.close()

        # Elimina fisicamente file, immagini e PDF
        for folder_path in [Config.IMG_DIR, Config.PDF_DIR]:
            if os.path.exists(folder_path):
                for f in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, f)
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    except:
                        pass

        msg = "[OK] Database svuotato e cartelle fisiche pulite."

    except Exception as e:
        msg = f"[ERR] Errore reset: {str(e)}"

    # Aggiornamento dello stato finale
    with state_lock:
        SCRAPER_STATE.update({
            "progress": 100,
            "log": SCRAPER_STATE["log"] + [msg]
        })

    return jsonify({"status": "success"})

# CANCELLAZIONE ASSET (solo immagini o solo PDF)
@admin_bp.route("/delete-assets/<type>", methods=["POST"])
@login_required
@admin_required
def delete_assets(type):

    # Determina cosa eliminare
    if type == 'images':
        path = Config.IMG_DIR
        db_cols = ['image_main'] + [f'photo_{i}' for i in range(1, 11)] + [f'layout_{i}' for i in range(1, 11)]
        label = "Immagini/Layout"
    else:
        path = Config.PDF_DIR
        db_cols = ['manual_pdf', 'safety_pdf', 'construction_instruction']
        label = "PDF e Istruzioni"

    count = 0

    # Reset dello stato dello scraper
    with state_lock:
        SCRAPER_STATE.update({
            "running": False,
            "progress": 0,
            "log": [f"[INFO] Pulizia totale {label}..."]
        })

    # Eliminazione fisica dei file
    if os.path.exists(path):
        for f in os.listdir(path):
            try:
                os.remove(os.path.join(path, f))
                count += 1
            except Exception as e:
                print(f"Errore rimozione file {f}: {e}")

    # Reset delle colonne del DB
    try:
        conn = get_db_connection()
        set_clause = ", ".join([f'"{col}" = NULL' for col in db_cols])
        conn.execute(f'UPDATE product SET {set_clause}')
        conn.commit()
        conn.close()

    except Exception as e:
        # Log di errore nel DB
        with state_lock:
            SCRAPER_STATE["log"].append(f"[ERR] Errore Database: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

    # Stato finale
    with state_lock:
        SCRAPER_STATE["log"].append(
            f"[OK] Eliminati {count} file e resettate {len(db_cols)} colonne nel DB."
        )
        SCRAPER_STATE["progress"] = 100

    return jsonify({"status": "success"})

# AVVIO SCANSIONE (IMMAGINI o PDF)
# Lancia un thread in background
@admin_bp.route("/scan-<mode>")
@login_required
@admin_required
def start_scan(mode):

    # Aggiorna lo stato
    with state_lock:
        SCRAPER_STATE.update({
            "running": True,
            "progress": 0,
            "log": [f"[INFO] Avvio scansione {mode}..."]
        })

    # Avvio del thread
    app = current_app._get_current_object()
    threading.Thread(target=lambda: run_scan_thread(mode, app)).start()

    return jsonify({"status": "iniziato"})

# THREAD DI SCANSIONE
# Ricostruisce i riferimenti nel DB in base ai file fisici presenti
def run_scan_thread(mode, app):

    with app.app_context():
        try:
            conn = get_db_connection()

            # Determina quali colonne azzerare
            if mode == 'images':
                cols_to_null = ['image_main'] + [f'photo_{i}' for i in range(1, 11)] + [f'layout_{i}' for i in range(1, 11)]
            else:
                cols_to_null = ['manual_pdf', 'safety_pdf']

            # Reset delle colonne
            set_null_clause = ", ".join([f'"{c}" = NULL' for c in cols_to_null])
            conn.execute(f'UPDATE product SET {set_null_clause}')
            conn.commit()

            # Carica i prodotti
            products = conn.execute('SELECT id, code FROM product').fetchall()
            total = len(products)

            # Percorsi ed estensioni del target
            path_base = Config.IMG_DIR if mode == 'images' else Config.PDF_DIR
            ext_target = '.jpg' if mode == 'images' else '.pdf'

            # Loop dei prodotti
            for i, p in enumerate(products):

                # Filtra i file per codice + estensione
                all_files = sorted([
                    f for f in os.listdir(path_base)
                    if f.startswith(str(p['code'])) and f.lower().endswith(ext_target)
                ])

                updates = {}
                found_types = []

                # LOGICA DELLE IMMAGINI
                if mode == 'images':

                    # Foto principali + secondarie
                    photo_files = [f for f in all_files if "_photo_" in f or "_m" in f]
                    if photo_files:
                        updates['image_main'] = photo_files[0]
                        found_types.append("Foto")

                    for idx in range(1, 11):
                        updates[f"photo_{idx}"] = photo_files[idx] if len(photo_files) > idx else None

                    # Layout
                    layout_files = [f for f in all_files if "_layout_" in f]
                    if layout_files:
                        found_types.append("Layout")

                    for idx in range(1, 11):
                        updates[f"layout_{idx}"] = layout_files[idx-1] if len(layout_files) >= idx else None

                # LOGICA DEI PDF
                else:
                    manual_files = [
                        f for f in all_files
                        if "_manual" in f or str(p['code']) == f.replace('.pdf', '')
                    ]

                    if manual_files:
                        updates['manual_pdf'] = manual_files[0]
                        found_types.append("Manuale")

                    # Safety PDF statico
                    safety_filename = os.path.basename(Config.STATIC_SAFETY_PDF)
                    if os.path.exists(os.path.join(Config.PDF_DIR, safety_filename)):
                        updates['safety_pdf'] = safety_filename
                        if "Safety" not in found_types:
                            found_types.append("Safety")

                # Aggiornamento del DB
                if updates:
                    set_clause = ", ".join([f'"{k}" = ?' for k in updates.keys()])
                    params = list(updates.values()) + [p['id']]
                    conn.execute(f'UPDATE product SET {set_clause} WHERE id = ?', params)

                # Log dinamico
                if found_types:
                    msg = f"[OK] {p['code']}: trovati {len(found_types)} tipologie di asset ({', '.join(found_types)})."
                else:
                    msg = f"[WARN] {p['code']}: nessun file {mode.upper()} trovato."

                # Aggiorna lo stato globale
                with state_lock:
                    SCRAPER_STATE["log"].append(msg)
                    SCRAPER_STATE["progress"] = int(((i + 1) / total) * 100)

            conn.commit()
            conn.close()

            # Fine della scansione
            with state_lock:
                SCRAPER_STATE["running"] = False
                SCRAPER_STATE["log"].append(f"--- SCANSIONE {mode.upper()} COMPLETATA ---")

        except Exception as e:
            with state_lock:
                SCRAPER_STATE["running"] = False
                SCRAPER_STATE["log"].append(f"[ERR] Errore: {str(e)}")

# CONTROLLO DEI DUPLICATI NEL DATABASE
@admin_bp.route("/check-duplicates")
@login_required
@admin_required
def check_duplicates():

    with state_lock:
        SCRAPER_STATE.update({
            "running": False,
            "progress": 0,
            "log": ["[INFO] Controllo duplicati..."]
        })

    try:
        conn = get_db_connection()
        duplicates = conn.execute(
            'SELECT code, COUNT(*) as c FROM product GROUP BY code HAVING c > 1'
        ).fetchall()
        conn.close()

        with state_lock:
            if duplicates:
                for d in duplicates:
                    SCRAPER_STATE["log"].append(
                        f"[WARN] Codice {d['code']} duplicato {d['c']} volte."
                    )
            else:
                SCRAPER_STATE["log"].append("[OK] Nessun duplicato trovato.")

            SCRAPER_STATE["progress"] = 100

    except Exception as e:
        with state_lock:
            SCRAPER_STATE["log"].append(f"[ERR] {str(e)}")

    return jsonify({"status": "done"})

# ESPORTAZIONE EXCEL COMPLETO DEL DATABASE
@admin_bp.route("/export-excel")
@login_required
@admin_required
def export_excel():

    conn = get_db_connection()
    df = pd.read_sql_query('SELECT * FROM product', conn)
    conn.close()

    if df.empty:
        return jsonify({"error": "Database vuoto"}), 400

    # Scrittura dell'Excel in memoria
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Catalogo')

    output.seek(0)

    # Restituisce un file Excel come risposta HTTP
    return make_response(output.getvalue(), {
        "Content-Disposition": "attachment; filename=catalogo.xlsx",
        "Content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    })