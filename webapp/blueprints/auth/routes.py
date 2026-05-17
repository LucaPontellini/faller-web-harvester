from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from webapp.models.user import User
from webapp.services.auth_logic import verify_user
from webapp.db import get_db

auth_bp = Blueprint('auth', __name__)

# REGISTRAZIONE UTENTE
# Gestisce sia GET (mostra form) che POST (crea nuovo utente).
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Import locale per evitare dipendenze circolari
        from webapp.services.auth_logic import create_user

        # Tentativo di creazione utente
        if create_user(username, password):
            flash('Account creato con successo! Ora puoi accedere.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Errore: lo username potrebbe essere già esistente.', 'danger')

    # GET → mostra la form di registrazione
    return render_template('auth/register.html', title='Registrati')

# LOGIN UTENTE
# Verifica credenziali, normalizza il ruolo e gestisce redirect intelligenti.
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Verifica delle credenziali tramite la logica centralizzata
        user_row = verify_user(username, password)

        if user_row:

            # Normalizzazione del ruolo (evita problemi con spazi o maiuscole)
            role = (user_row['role'] or '').strip().lower()

            # Creazione dell'oggetto User compatibile con Flask-Login
            user_obj = User(
                user_row['id'],
                user_row['username'],
                role
            )

            login_user(user_obj)
            flash('Login effettuato con successo!', 'success')

            # Debug utile in fase di sviluppo
            print("LOGIN DEBUG ROLE:", role)

            # Redirect basato sul ruolo
            if role == "admin":
                return redirect(url_for('admin.dashboard'))

            return redirect(url_for('main.dashboard'))

        else:
            flash('Credenziali non valide. Riprova.', 'danger')

    # GET → mostra la form di login
    return render_template('auth/login.html', title='Accedi')

# LOGOUT UTENTE
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ti sei disconnesso.', 'info')
    return redirect(url_for('main.index'))

# CAMBIO PASSWORD
# Richiede l'autenticazione e la verifica della password attuale.
@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():

    if request.method == 'POST':

        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')

        # Validazione minima della nuova password
        if not new_password:
            flash('Inserisci una nuova password.', 'warning')
            return redirect(url_for('auth.change_password'))

        if len(new_password) < 8:
            flash('La password deve avere almeno 8 caratteri.', 'warning')
            return redirect(url_for('auth.change_password'))

        # Import locale per evitare dipendenze circolari
        from webapp.services.auth_logic import verify_user, update_password

        # Verifica la password attuale
        user_row = verify_user(current_user.username, old_password)

        if not user_row:
            flash('Password attuale non corretta.', 'danger')
            return redirect(url_for('auth.change_password'))

        # Aggiornamento della password
        update_password(current_user.id, new_password)

        flash('Password aggiornata con successo!', 'success')
        return redirect(url_for('main.dashboard'))

    # GET → mostra la form di cambio password
    return render_template('auth/change_password.html', title='Cambia Password')