import pytest
from app import create_app
from app.extensions import db
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_health_check(client):
    """Uji endpoint health-check"""
    res = client.get('/api/health')
    assert res.status_code == 200
    assert res.get_json()['status'] == 'success'

def test_user_crud_and_validation(client):
    """Uji Create, Read, Update, Delete & Validasi Error pada User"""
    # 1. Create User valid
    res = client.post('/api/users', json={
        "username": "analyst_budi",
        "email": "budi@cyberguard.id",
        "password": "password123",
        "role": "analyst"
    })
    assert res.status_code == 201
    user_id = res.get_json()['data']['id']

    # 2. Uji Validasi Input Salah (email tidak valid & password terlalu pendek)
    bad_res = client.post('/api/users', json={
        "username": "ab",
        "email": "bukan-email",
        "password": "123"
    })
    assert bad_res.status_code == 400

    # 3. Get All & Get by ID
    assert client.get('/api/users').status_code == 200
    assert client.get(f'/api/users/{user_id}').status_code == 200

    # 4. Update User
    upd = client.put(f'/api/users/{user_id}', json={"role": "admin"})
    assert upd.status_code == 200
    assert upd.get_json()['data']['role'] == 'admin'

    # 5. Delete User & pastikan 404 setelah dihapus
    assert client.delete(f'/api/users/{user_id}').status_code == 200
    assert client.get(f'/api/users/{user_id}').status_code == 404

def test_full_security_workflow(client):
    """Uji relasi penuh: User -> Asset -> Vulnerability -> Incident -> IncidentResponse"""
    # Buat User
    u_res = client.post('/api/users', json={
        "username": "sec_admin",
        "email": "admin@cyberguard.id",
        "password": "secretpassword",
        "role": "admin"
    })
    user_id = u_res.get_json()['data']['id']

    # Buat Asset
    a_res = client.post('/api/assets', json={
        "asset_name": "Core-DB-Server",
        "ip_address": "10.0.1.50",
        "asset_type": "Database Server",
        "criticality": "critical",
        "owner_department": "IT Infrastructure"
    })
    assert a_res.status_code == 201
    asset_id = a_res.get_json()['data']['id']

    # Buat Vulnerability terkait Asset
    v_res = client.post('/api/vulnerabilities', json={
        "asset_id": asset_id,
        "cve_code": "CVE-2026-1024",
        "title": "SQL Injection on Legacy Endpoint",
        "cvss_score": 9.1,
        "severity": "critical"
    })
    assert v_res.status_code == 201

    # Buat Incident terkait Asset & User
    i_res = client.post('/api/incidents', json={
        "asset_id": asset_id,
        "reported_by": user_id,
        "title": "Unauthorized DB Query Spike",
        "incident_type": "Intrusion",
        "severity": "high",
        "description": "Terdeteksi query mencurigakan dari IP eksternal."
    })
    assert i_res.status_code == 201
    incident_id = i_res.get_json()['data']['id']

    # Buat Incident Response terkait Incident & User
    r_res = client.post('/api/incident-responses', json={
        "incident_id": incident_id,
        "responder_id": user_id,
        "action_taken": "Isolasi segment jaringan & blokir IP sumber",
        "notes": "Patch dijadwalkan malam ini."
    })
    assert r_res.status_code == 201