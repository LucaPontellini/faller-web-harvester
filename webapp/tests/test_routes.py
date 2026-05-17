def test_landing_page_accessible(client):
    # Verifica che la Home Page risponda correttamente.
    response = client.get('/')
    assert response.status_code == 200

def test_dashboard_redirects_if_anonymous(client):
    # Verifica che un utente non loggato venga reindirizzato provando ad accedere all'area admin.
    response = client.get('/admin/')
    assert response.status_code in [302, 401] 

def test_api_status_endpoint_before_auth(client):
    # Verifica il comportamento di sicurezza sull'endpoint del progresso dello scraper.
    response = client.get('/admin/scraper-progress')
    assert response.status_code == 200