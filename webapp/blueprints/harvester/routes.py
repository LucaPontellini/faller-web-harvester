from flask import Blueprint, render_template
from flask_login import login_required

harvester_bp = Blueprint('harvester', __name__)

# ROUTE PRINCIPALE DELLO SCRAPER
@harvester_bp.route('/harvester')
@login_required
def scraper():
    # Mostra la pagina principale dello scraper (inserimento codici)
    return render_template('harvester/scraper.html')

# ROUTE PER LA RICERCA PER INTERVALLO NUMERICO
# Questa pagina permette di inserire un range di codici da processare.
@harvester_bp.route('/search')
@login_required
def search():
    # Mostra la pagina dedicata alla ricerca per l'intervallo
    return render_template('harvester/search.html')