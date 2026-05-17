import pytest
import os
import shutil
from webapp import create_app
from webapp.db import init_db, close_db

# Classe AuthActions per simulare le azioni di autenticazione (Login/Logout) all'interno del client di test di Flask. 
# Evita la duplicazione del codice nei test di sicurezza (RBAC) e di autenticazione.
class AuthActions:
    def __init__(self, client):
        self._client = client

    # Invia una richiesta POST alla rotta di login con le credenziali fornite.
    def login(self, username='admin', password='admin123'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password},
            follow_redirects=True
        )

    # Invia una richiesta GET alla rotta di logout.
    def logout(self):
        return self._client.get('/auth/logout', follow_redirects=True)

# Configura l'applicazione in modalità Testing e isola il database e i file system.
@pytest.fixture
def app():
    base_dir = "faller_catalogo_test"
    test_db_path = os.path.join("instance", "test_database.db")
    
    # 1. SETUP: Prepara le cartelle temporanee isolate per i test
    os.makedirs("instance", exist_ok=True)
    
    # 2. CONFIGURAZIONE: Applica le configurazioni di test
    app = create_app({
        'TESTING': True,
        'SECRET_KEY': 'test-key-temporanea-gpoi',
        'DATABASE': test_db_path,
        'IMG_DIR': os.path.join(base_dir, "immagini"),
        'PDF_DIR': os.path.join(base_dir, "pdf"),
        'EXPORT_DIR': os.path.join(base_dir, "export_zip"),
        'BASE_DIR': base_dir,
    })

    # 3. INIZIALIZZAZIONE: Crea le tabelle nel database SQLite di test
    with app.app_context():
        init_db()
    
    # Il comando 'yield' passa il controllo ai file di test (es. test_repository.py)
    yield app

    # 4. TEARDOWN (PULIZIA): Viene eseguito automaticamente alla fine di TUTTI i test
    with app.app_context():
        close_db()

    # Rimuove il database di test per non lasciare residui sporchi
    if os.path.exists(test_db_path):
        try:
            os.remove(test_db_path)
        except PermissionError:
            pass

    # Rimuove la cartella dei media temporanea creata per i test
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir, ignore_errors=True)

# Fixture per esporre il client di test di Flask
@pytest.fixture
def client(app):
    return app.test_client()

# Fixture per iniettare le azioni di autenticazione nei test
@pytest.fixture
def auth(client):
    return AuthActions(client)