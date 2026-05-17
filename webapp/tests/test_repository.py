import pytest
from sqlite3 import IntegrityError
from webapp.repositories import product_repository

def test_product_save_and_find(app):
    # Verifica il ciclo CRUD base di inserimento e lettura di un prodotto.
    with app.app_context():
        data = {
            "code": "120111",
            "name": "Fabbricato rurale",
            "scale": "H0",
            "availability": "In Stock",
            "product_link": "https://www.faller.de/en/120111"
        }
        product_repository.save_product(data)
        
        found = product_repository.find_by_code("120111")
        assert found is not None
        assert found['name'] == "Fabbricato rurale"

def test_get_all_products(app):
    # Verifica il recupero della lista completa di prodotti.
    with app.app_context():
        products = product_repository.get_all_products()
        assert isinstance(products, list)

def test_sqlite_unique_constraint(app):
    # Verifica che l'inserimento di un codice esistente aggiorni l'elemento senza bloccare l'app.
    with app.app_context():
        data1 = {
            "code": "999999", "name": "Kit Vecchio", "scale": "H0",
            "availability": "Available", "product_link": "http://link"
        }
        data2 = {
            "code": "999999", "name": "Kit Aggiornato", "scale": "N",
            "availability": "Out of Stock", "product_link": "http://link"
        }
        
        # Salva la prima volta
        product_repository.save_product(data1)
        # Il secondo salvataggio dello stesso codice effettua un UPSERT/aggiornamento coerente
        product_repository.save_product(data2)
        
        found = product_repository.find_by_code("999999")
        assert found is not None
        assert found['name'] == "Kit Aggiornato"