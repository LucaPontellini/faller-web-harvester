import pytest

def test_admin_restriction_for_normal_user(client, auth):
    # Verifica che un utente normale venga respinto dall'area admin.
    # Il flusso rispetta la logica: prima fa l'account, poi il login, poi usa il sito.
    with client:
        # 1. L'utente normale deve PRIMA creare l'account (Registrazione)
        client.post('/auth/register', data={
            'username': 'utente_standard',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)

        # 2. DOPO aver fatto l'account, effettua il Login
        auth.login(username='utente_standard', password='password123')
        
        # 3. Tenta di usare il sito andando nell'area riservata all'admin -> Viene respinto
        response = client.get('/admin/')
        assert response.status_code in [403, 302]


def test_admin_access_allowed(client, auth):
    # Verifica che l'amministratore acceda correttamente alla sua Dashboard dopo il login.
    with client:
        # Usa l'account admin nativo creato automaticamente da init_db() con il ruolo amministrativo corretto già preimpostato.
        
        # 1. Il login esegue il POST usando le credenziali dell'admin di sistema
        auth.login(username='admin', password='admin123')
        
        # 2. Accede all'area admin verificando il successo della richiesta (200 OK)
        response = client.get('/admin/', follow_redirects=True)
        assert response.status_code == 200