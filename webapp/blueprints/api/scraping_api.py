import time
import traceback
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from webapp.services.scraper.client import search_code
from webapp.services.scraper.parser import parse_product_page
from webapp.repositories import product_repository

scraping_api_bp = Blueprint('scraping_api', __name__)

@scraping_api_bp.route('/start', methods=['POST'])
@login_required
def start_scraping():
    # AVVIO PROCESSO DI SCRAPING
    # Accetta:
    #   - lista di codici
    #   - range numerico (start/end)
    # Include la protezione role-based e salvataggio nel DB.

    # Solo gli utenti normali possono avviare lo scraping
    if current_user.role == 'admin':
        return jsonify({
            "error": "Accesso negato: l'amministratore ha permessi di sola lettura."
        }), 403

    data = request.json
    codes_to_process = []

    # Input: lista di codici
    if 'codes' in data:
        codes_to_process = data.get('codes', [])

    # Input: range numerico
    elif 'start' in data and 'end' in data:
        try:
            s, e = int(data['start']), int(data['end'])
            codes_to_process = [str(i) for i in range(s, e + 1)]
        except ValueError:
            return jsonify({"error": "Codici inizio/fine non validi"}), 400

    if not codes_to_process:
        return jsonify({"error": "Nessun dato fornito"}), 400

    results = []

    # LOOP PRINCIPALE DI SCRAPING
    for code_str in codes_to_process:

        # Evita duplicati nel DB
        if product_repository.find_by_code(code_str):
            print(f"[SKIP] Codice {code_str} già presente nel database.")
            results.append({"code": code_str, "status": "already_in_db"})
            continue

        try:
            print(f"\n[START] Inizio ricerca per codice: {code_str}")

            # Cerca un URL del prodotto tramite l'API della Faller
            product_url = search_code(code_str)

            # Normalizzazione degli URL relativi
            if product_url and not product_url.startswith("http"):
                product_url = "https://www.faller.de" + product_url

            if product_url:
                print(f"[FOUND] Prodotto trovato! URL: {product_url}")

                # Parsing della pagina del prodotto
                product_data = parse_product_page(product_url, code_str)

                if product_data:
                    product_repository.save_product(product_data)
                    results.append({"code": code_str, "status": "success"})
                else:
                    results.append({"code": code_str, "status": "error", "message": "Dati vuoti"})
            else:
                print(f"[NOT_FOUND] Codice {code_str} non trovato sul sito")
                results.append({"code": code_str, "status": "not_found"})

            # Delay per il rispetto del server della Faller
            time.sleep(1)

        except Exception as e:
            print(f"[FATAL ERROR] Fallimento durante lo scraping di {code_str}: {str(e)}")
            traceback.print_exc()
            results.append({"code": code_str, "status": "error", "message": str(e)})

    return jsonify({
        "status": "completed",
        "processed": len(results),
        "details": results
    })

# ELIMINAZIONE DEL SINGOLO PRODOTTO
@scraping_api_bp.route('/delete_product/<codeSlot>', methods=['DELETE'])
def delete_product_route(codeSlot):
    try:
        product_repository.delete_by_code(codeSlot)
        return jsonify({"status": "success", "message": f"Prodotto {codeSlot} eliminato"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ELIMINAZIONE MULTIPLA PRODOTTI + PULIZIA EXPORT
@scraping_api_bp.route('/delete_selected', methods=['POST'])
def delete_selected():
    try:
        data = request.json
        codes = data.get('codes', [])

        if not codes:
            return jsonify({"status": "error", "message": "Nessun codice fornito"}), 400

        # Elimina i prodotti uno per uno
        for code in codes:
            product_repository.delete_by_code(code)

        # Pulizia dei file Excel/ZIP obsoleti
        product_repository.clear_export_folders()

        return jsonify({
            "status": "success",
            "message": f"Eliminati {len(codes)} prodotti e puliti i file di export"
        }), 200

    except Exception as e:
        print(f"Errore durante l'eliminazione multipla: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500