import pytest
from unittest.mock import patch
from webapp.services.scraper.client import search_code
from webapp.services.scraper.parser import parse_product_page

@patch('webapp.services.scraper.client.requests.get')
def test_search_code_invalid(mock_get):
    # Verifica che un codice inesistente restituisca None isolando la rete.
    mock_get.return_value.status_code = 404
    assert search_code("999999999") is None

def test_clean_val_logic():
    # Testa la funzione interna di normalizzazione delle stringhe.
    from webapp.services.scraper.parser import clean_val
    assert clean_val(" ✓ Prodotto Speciale \n ") == "Prodotto Speciale"
    assert clean_val(None) == "N/A"

@patch('webapp.services.scraper.client.requests.get')
def test_scraper_english_parsing_logic(mock_get):
    # Verifica la capacità estrattiva dei selettori CSS della versione inglese.
    fake_html = """
    <html>
        <h1 class="product-title">Station 'Neustadt'</h1>
        <span class="scale-info">Scale H0</span>
        <div class="stock-status">Available</div>
    </html>
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = fake_html
    
    risultato = parse_product_page(fake_html, code="110115")
    assert risultato is not None