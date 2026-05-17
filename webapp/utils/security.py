from flask import abort
from flask_login import current_user
from functools import wraps

# Decoratore per proteggere una route e permettere l'accesso
# solo agli utenti con ruolo "admin".
# Se l'utente non è autenticato o non è admin → 403 Forbidden.
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403) # Accesso negato
        return f(*args, **kwargs)
    return decorated_function

# Funzione di utilità per verificare rapidamente se l'utente corrente è un amministratore.
def is_admin():
    return current_user.is_authenticated and current_user.role == "admin"



# ================================================================================================================================================
# Un decoratore in Python è una funzione che "avvolge" un'altra funzione per aggiungere comportamenti extra senza modificarne il codice interno.
# Si usa con la sintassi @decoratore sopra la funzione da estendere.
# ================================================================================================================================================