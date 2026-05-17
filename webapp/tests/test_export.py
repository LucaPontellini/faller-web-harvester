import os
from webapp.services.io.excel_builder import save_to_excel

def test_excel_creation(tmp_path):
    # Verifica la creazione fisica e l'integrità del file Excel.
    d = tmp_path / "test_dir"
    d.mkdir()
    excel_file = d / "test.xlsx"
    
    test_data = [
        {"code": "110115", "name": "Stazione di Scambio", "scale": "H0", "image_main": "110115.jpg"}
    ]
    
    save_to_excel(test_data, str(excel_file))
    assert os.path.exists(excel_file)
    assert os.path.getsize(excel_file) > 0