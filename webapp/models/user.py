class User:
    # Rappresenta un utente autenticato nel sistema
    def __init__(self, id, username, role):
        self.id = id             # ID univoco nel database
        self.username = username # Nome dell'utente
        self.role = role         # Ruolo (user/admin)

    # Metodi richiesti da Flask-Login
    def is_authenticated(self): return True # L'utente è autenticato
    def is_active(self): return True        # L'account è attivo
    def is_anonymous(self): return False   # Non è un utente anonimo
    def get_id(self): return str(self.id)             # Restituisce l'ID come stringa

    @staticmethod
    def get(user_id, db):
        # Recupera un utente dal database tramite l'ID
        user_row = db.execute(
            'SELECT id, username, role FROM user WHERE id = ?', (user_id,)
        ).fetchone()

        # Se trovato, restituisce un oggetto User
        if user_row:
            return User(
                user_row['id'],
                user_row['username'],
                user_row['role']
            )

        # Se non esiste, restituisce None
        return None