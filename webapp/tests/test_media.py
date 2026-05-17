import os
from unittest.mock import patch
from webapp.services.io.archiver import create_archive

def test_download_and_zip_flow(app):
    # Verifica che l'applicazione sposti e organizzi correttamente immagini e PDF.
    with app.app_context():
        test_code = "130160"
        
        img_dir = app.config['IMG_DIR']
        pdf_dir = app.config['PDF_DIR']
        
        os.makedirs(img_dir, exist_ok=True)
        os.makedirs(pdf_dir, exist_ok=True)
        
        img_path = os.path.join(img_dir, f"{test_code}_main.jpg")
        pdf_path = os.path.join(pdf_dir, f"{test_code}_manual.pdf")

        with open(img_path, 'wb') as f:
            f.write(b"fake_binary_jpeg_data")
        with open(pdf_path, 'wb') as f:
            f.write(b"%PDF-1.4 fake_pdf_data")

        with patch('webapp.services.io.archiver.Config', app.config):
            zip_creato = create_archive(specific_codes=[test_code], mode='all')

            assert os.path.exists(img_path)
            assert os.path.exists(pdf_path)
            assert os.path.exists(zip_creato)
            assert os.path.getsize(zip_creato) > 0