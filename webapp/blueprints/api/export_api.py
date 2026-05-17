from flask import Flask, Blueprint, send_file, current_app, request, flash, redirect, url_for
from webapp.repositories import product_repository
from webapp.services.io import excel_builder, archiver
import os

export_api_bp = Blueprint('export_api', __name__)

# DOWNLOAD DELL'EXCEL COMPLETO DEL CATALOGO
@export_api_bp.route('/download/excel')
def download_excel():

    # Recupera tutti i prodotti dal DB
    products = product_repository.get_all_products()

    # Se il DB è vuoto → mostra un messaggio e torna alla dashboard
    if not products:
        flash("Nessun dato disponibile nel database per l'esportazione.")
        return redirect(url_for('main.dashboard'))

    # Converte i RowObject in dict per ExcelBuilder
    data_list = [dict(p) for p in products]

    # Percorso del file Excel finale
    excel_path = os.path.join(
        current_app.config['EXPORT_DIR'],
        current_app.config['EXCEL_FILENAME']
    )

    # Assicura che la cartella export esista
    os.makedirs(current_app.config['EXPORT_DIR'], exist_ok=True)

    # Genera l'Excel tramite il servizio dedicato
    excel_builder.save_to_excel(data_list, excel_path)

    # Restituisce il file come download
    return send_file(excel_path, as_attachment=True)

# DOWNLOAD ZIP DI IMMAGINI/PDF PER CODICI SELEZIONATI
@export_api_bp.route('/download/zip')
def download_zip():

    # Recupera la lista dei codici dalla query string
    codes_raw = request.args.get('codes')

    # Nessun codice selezionato → avvisa l'utente
    if not codes_raw:
        flash("Seleziona dei prodotti prima di scaricare lo ZIP.", "warning")
        return redirect(url_for('main.dashboard'))

    # Converte la stringa "123,456,789" in lista ["123","456","789"]
    specific_codes = codes_raw.split(',')

    try:
        # Crea l'archivio ZIP tramite il servizio archiver
        zip_path = archiver.create_archive(specific_codes=specific_codes)

        # Se il file esiste → invia il download
        if zip_path and os.path.exists(zip_path):
            return send_file(zip_path, as_attachment=True)

        # Nessun file trovato per quei codici
        flash("Nessun file multimediale trovato per i codici selezionati.", "info")
        return redirect(url_for('main.dashboard'))

    except Exception as e:
        # Errore di generazione dello ZIP
        flash(f"Errore creazione archivio: {str(e)}", "danger")
        return redirect(url_for('main.dashboard'))