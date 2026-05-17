import os
from webapp.services.io.validators import (
    validate_product_code, 
    validate_allowed_file, 
    get_file_hash, 
    is_duplicate
)

def test_product_code_validation():
    # Testa che il sistema accetti codici Faller di qualsiasi lunghezza numerica (>= 3 cifre).
    assert validate_product_code("1201") is True       # Vecchi codici / accessori (4 cifre)
    assert validate_product_code("13016") is True      # Codici intermedi (5 cifre)
    assert validate_product_code("110115") is True     # Standard attuale (6 cifre)
    assert validate_product_code("1809001") is True    # Parti speciali / varianti (7 cifre)
    assert validate_product_code("99912345") is True   # Codici estesi / ricambi (8 cifre)
    
    # Casi non validi (devono fallire)
    assert validate_product_code("12") is False        # Troppo corto per essere un codice valido
    assert validate_product_code("abc115") is False    # Contiene lettere
    assert validate_product_code("110a15") is False    # Alfanumerico misto
    assert validate_product_code("") is False          # Campo vuoto

def test_allowed_file_extensions():
    # Verifica che il sistema filtri correttamente i file in base all'estensione.
    assert validate_allowed_file("catalogo.xlsx") is True
    assert validate_allowed_file("immagine.jpg") is True
    assert validate_allowed_file("script.sh") is False

def test_file_hash_calculation(tmp_path):
    # Verifica che il calcolo dell'hash MD5 sia corretto e coerente.
    test_file = tmp_path / "test_hash.txt"
    with open(test_file, "w") as f:
        f.write("Faller Scraper 2026")
        
    hash_1 = get_file_hash(str(test_file))
    hash_2 = get_file_hash(str(test_file))
    
    assert hash_1 is not None
    assert hash_1 == hash_2

def test_is_duplicate_detection(tmp_path):
    # Verifica l'individuazione di file duplicati basata sul contenuto (MD5).
    dir_existing = tmp_path / "existing"
    dir_existing.mkdir()
    
    file_creato = dir_existing / "file_esistente.xlsx"
    with open(file_creato, "w") as f:
        f.write("contenuto duplicato finto")
        
    assert is_duplicate(str(file_creato), str(dir_existing)) is True