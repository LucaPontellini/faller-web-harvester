import logging
import os

def init_extensions(app):
    # Configura il logging per vedere errori nel terminale di Flask
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s'
    )
    
    # Verifica che la cartella 'instance' esista per il database
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)