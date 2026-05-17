import os
from flask import Blueprint, render_template, send_from_directory, current_app, abort, redirect, url_for
from flask_login import login_required, current_user
from webapp.repositories import product_repository

main_bp = Blueprint('main', __name__)

# ROUTE HOME
@main_bp.route('/')
def index():
    # Pagina iniziale minimale
    return render_template('main/index.html', title="Benvenuto - Faller Harvester")

# DASHBOARD UTENTE (con redirect automatico per admin)
@main_bp.route('/dashboard')
@login_required
def dashboard():

    # 1. REDIRECT AUTOMATICO PER ADMIN
    # Se l'utente è admin, non deve vedere la dashboard utente
    if current_user.role == 'admin':
        return redirect(url_for('admin.dashboard'))

    # 2. RECUPERO PRODOTTI DAL DATABASE
    all_products = product_repository.get_all_products()

    # 3. CONTEGGIO FILE IMMAGINI E PDF
    n_images = 0
    n_pdfs = 0

    img_dir = current_app.config.get('IMG_DIR')
    pdf_dir = current_app.config.get('PDF_DIR')

    try:
        # Conta solo i file reali, ignora le cartelle o i file corrotti
        if img_dir and os.path.exists(img_dir):
            n_images = len([
                f for f in os.listdir(img_dir)
                if os.path.isfile(os.path.join(img_dir, f))
            ])

        if pdf_dir and os.path.exists(pdf_dir):
            n_pdfs = len([
                f for f in os.listdir(pdf_dir)
                if os.path.isfile(os.path.join(pdf_dir, f))
            ])

    except Exception as e:
        # Log minimale per evitare crash della dashboard
        print(f"Errore nel conteggio file: {e}")

    # Statistiche da mostrare nella dashboard
    stats = {
        'total_products': len(all_products),
        'total_images': n_images,
        'total_pdfs': n_pdfs
    }

    # Rendering della pagina della dashboard dell'utente
    return render_template(
        'main/dashboard.html',
        stats=stats,
        products=all_products
    )

# SERVING FILE STATICI DEL CATALOGO (IMMAGINI)
@main_bp.route('/catalogo/immagini/<filename>')
def serve_catalogo_image(filename):
    # Validazione minima del nome file
    if not filename or filename in ["N/A", "None"]:
        abort(404)

    # Serve il file direttamente dalla cartella immagini
    return send_from_directory(
        current_app.config['IMG_DIR'],
        filename,
        as_attachment=False # Mostra l'immagine nel browser
    )

# SERVING FILE STATICI DEL CATALOGO (PDF)
@main_bp.route('/catalogo/pdf/<path:filename>')
def serve_pdfs(filename):

    # Normalizza il percorso per evitare traversal (../../)
    clean_filename = os.path.basename(filename)

    # Validazione minima
    if not clean_filename or clean_filename in ["N/A", "None"]:
        abort(404)

    # Verifica che il file esista realmente
    pdf_path = os.path.join(current_app.config['PDF_DIR'], clean_filename)
    if not os.path.exists(pdf_path):
        abort(404)

    # Serve il PDF con MIME-Type corretto
    return send_from_directory(
        current_app.config['PDF_DIR'],
        clean_filename,
        mimetype='application/pdf'
    )