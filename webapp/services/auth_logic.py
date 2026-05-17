from werkzeug.security import generate_password_hash, check_password_hash
from webapp.db import get_db

# Crea un nuovo utente con password hashata
def create_user(username, password, role='user'):
    db = get_db()
    hash_pwd = generate_password_hash(password) # Hash sicuro della password

    try:
        db.execute(
            'INSERT INTO user (username, password_hash, role) VALUES (?, ?, ?)',
            (username, hash_pwd, role)
        )
        db.commit()
        return True
    except db.IntegrityError:
        # Username già esistente
        return False

# Verifica le credenziali dell'utente
def verify_user(username, password):
    db = get_db()

    # Recupera l'utente tramite username
    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    # Controlla che l'utente esista e che la password sia corretta
    if user and check_password_hash(user['password_hash'], password):
        return user

    return None

# Aggiorna la password dell'utente (hashata)
def update_password(user_id, new_password):
    db = get_db()
    hash_pwd = generate_password_hash(new_password) # Nuovo hash

    db.execute(
        'UPDATE user SET password_hash = ? WHERE id = ?',
        (hash_pwd, user_id)
    )
    db.commit()
    return True