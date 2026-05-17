import os
from unittest.mock import patch
from webapp.services.io.archiver import create_archive

def test_create_zip_success(app):
    # Verifica che l'archivio ZIP venga creato correttamente se esistono file.
    with app.app_context():
        export_path = app.config['EXPORT_DIR']
        img_dir = app.config['IMG_DIR']
        
        os.makedirs(export_path, exist_ok=True)
        os.makedirs(img_dir, exist_ok=True)
        
        # Scrive un file finto contrassegnato da un numero iniziale (es. codice prodotto)
        with open(os.path.join(img_dir, "110115_main.jpg"), "w") as f:
            f.write("finti dati immagine")
            
        with patch('webapp.services.io.archiver.Config', app.config):
            zip_creato = create_archive(mode='all')
            
            assert zip_creato is not None
            assert os.path.exists(zip_creato)
            assert os.path.getsize(zip_creato) > 0