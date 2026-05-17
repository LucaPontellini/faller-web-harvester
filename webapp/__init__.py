import os
from flask import Flask
from flask_login import LoginManager
from .config import Config
from . import db

# La factory function che crea e configura l'app Flask
def create_app(test_config=None):
    # instance_relative_config=True → Flask usa la cartella /instance per file runtime (DB, ecc.)
    app = Flask(__name__, instance_relative_config=True)
    
    # Caricamento configurazione:
    # - Se test_config è passato, usa quella (utile per pytest)
    # - Altrimenti carica la Config standard
    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(test_config)

    # 1. CREAZIONE AUTOMATICA DELLA CARTELLA INSTANCE (solo in produzione)
    # Flask richiede che esista per contenere database e file runtime
    if not app.config.get('TESTING'):
        try:
            os.makedirs(app.instance_path)
        except OSError:
            # Se esiste già, ignora l'errore
            pass

    # Inizializza le cartelle di output (immagini, pdf, zip)
    # Solo se non si è in test, per evitare side-effects nei test
    if hasattr(Config, 'init_app') and test_config is None:
        Config.init_app(app)
        
    # Inizializza il database (connessione + setup)
    db.init_app(app)

    # 2. CONFIGURAZIONE FLASK-LOGIN
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # redirect automatico se non autenticato
    login_manager.init_app(app)

    # Funzione che Flask-Login usa per caricare un utente dalla sessione
    from webapp.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id, db.get_db())

    # 3. CREAZIONE AUTOMATICA DEL DB + CREAZIONE ADMIN DI DEFAULT
    with app.app_context():
        db_path = app.config.get('DATABASE')

        # Se il DB non esiste, lo crea
        if db_path and not os.path.exists(db_path):
            db.init_db()

        # Creazione dell'utente admin se non è presente
        from werkzeug.security import generate_password_hash
        conn = db.get_db()

        admin = conn.execute(
            "SELECT id FROM user WHERE username = ?",
            ("admin",)
        ).fetchone()

        if not admin:
            conn.execute(
                "INSERT INTO user (username, password_hash, role) VALUES (?, ?, ?)",
                (
                    "admin",
                    generate_password_hash("admin123"),  # password di default
                    "admin"
                )
            )
            conn.commit()
            print("Admin creato: admin / admin123")

    # 4. REGISTRAZIONE DEI BLUEPRINTS
    # Ogni blueprint gestisce una sezione dell'app
    from .blueprints.main.routes import main_bp
    from .blueprints.harvester.routes import harvester_bp
    from .blueprints.api.scraping_api import scraping_api_bp
    from .blueprints.api.export_api import export_api_bp
    from .blueprints.auth.routes import auth_bp
    from .blueprints.errors.handlers import errors_bp
    from .blueprints.admin.routes import admin_bp

    # Registrazione con eventuali prefissi degli URL
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(harvester_bp, url_prefix='/harvester')
    app.register_blueprint(scraping_api_bp, url_prefix='/api/scraping')
    app.register_blueprint(export_api_bp, url_prefix='/api/export')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(errors_bp)

    return app