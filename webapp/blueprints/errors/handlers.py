from flask import Blueprint, render_template
from webapp.db import get_db

errors_bp = Blueprint('errors', __name__)

# HANDLER ERRORE 404 — PAGINA NON TROVATA
# Viene mostrata una pagina HTML personalizzata.
@errors_bp.app_errorhandler(404)
def not_found_error(error):
    # Restituisce la pagina 404 con codice HTTP corretto
    return render_template('errors/404.html'), 404

# HANDLER ERRORE 500 — ERRORE INTERNO SERVER
# Se l'errore avviene durante una transazione DB, effettua un rollback per evitare che la connessione rimanga in stato inconsistente.
@errors_bp.app_errorhandler(500)
def internal_error(error):

    # Tentativo di rollback del database (se la connessione è attiva)
    try:
        db = get_db()
        db.rollback()
    except:
        # Se il DB non è accessibile o non esiste una transazione attiva, ignora l'errore per evitare ulteriori eccezioni.
        pass

    # Restituisce la pagina 500 con codice HTTP corretto
    return render_template('errors/500.html'), 500