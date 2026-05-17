import sqlite3
import click
from flask import current_app, g

def get_db():
    # Crea una connessione al database SQLite se non esiste già.
    # La connessione viene salvata in 'g' per essere riutilizzata durante l'intera richiesta senza aprire nuove connessioni.
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],      # Percorso al file DB
            detect_types=sqlite3.PARSE_DECLTYPES # Parsing automatico dei tipi
        )
        g.db.row_factory = sqlite3.Row           # Righe accessibili come dizionari
    return g.db

def close_db(e=None):
    # Chiude la connessione al database al termine della richiesta.
    # Flask richiama automaticamente questa funzione grazie a teardown.
    db = g.pop('db', None)
    if db is not None:
        db.close()  # Chiusura sicura della connessione

def init_db():
    # Inizializza il database leggendo ed eseguendo schema.sql.
    # Usato per creare o ricreare tutte le tabelle del progetto.
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))  # Esegue tutte le istruzioni SQL

@click.command('init-db')
# Comando CLI: permette di eseguire "flask init-db" per ricreare completamente il database.
def init_db_command():
    # Esegue l'inizializzazione del database leggendo schema.sql
    init_db()
    click.echo('Database inizializzato correttamente.')

def init_app(app):
    # Registra le funzioni di gestione del database nell'app Flask.
    app.teardown_appcontext(close_db)      # Chiude DB al termine della richiesta
    app.cli.add_command(init_db_command)   # Aggiunge comando "flask init-db"