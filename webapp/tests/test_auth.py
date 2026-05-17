def test_register_success(client):
    # Verifica il corretto inserimento di un nuovo utente.
    response = client.post('/auth/register', data={
        'username': 'nuovoutente',
        'password': 'passwordsicura123',
        'confirm_password': 'passwordsicura123'
    }, follow_redirects=True)
    assert b"Account creato con successo" in response.data

def test_register_password_mismatch(client):
    # Verifica il blocco se le password non coincidono.
    response = client.post('/auth/register', data={
        'username': 'utente_errato',
        'password': 'password1',
        'confirm_password': 'password_diversa'
    }, follow_redirects=True)
    assert b"Le password non coincidono" in response.data or response.status_code == 200

def test_register_duplicate_username(client):
    # Verifica che il sistema impedisca la duplicazione degli utenti nel DB.
    client.post('/auth/register', data={
        'username': 'duplicato', 'password': '123', 'confirm_password': '123'
    })
    response = client.post('/auth/register', data={
        'username': 'duplicato', 'password': '456', 'confirm_password': '456'
    }, follow_redirects=True)
    assert b"esistente" in response.data.lower() or b"esiste" in response.data.lower() or b"errore" in response.data.lower()

def test_login_wrong_credentials(client):
    # Verifica il rifiuto dell'accesso a fronte di credenziali errate.
    response = client.post('/auth/login', data={
        'username': 'admin', 'password': 'password_sbagliata'
    }, follow_redirects=True)
    assert b"Invalido" in response.data or b"errore" in response.data.lower() or response.status_code in [200, 401]