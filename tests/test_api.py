# tests/test_api.py
import os
import sqlite3
import json
import pytest
import repositories
from app import create_app

TEST_DB = "test_postobon.db"

# Crea una base de datos temporal para pruebas
def create_test_db(path=TEST_DB):
    if os.path.exists(path):
        os.remove(path)
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE envases (
        id_envase TEXT PRIMARY KEY,
        tipo TEXT,
        capacidad_ml INTEGER,
        estado TEXT,
        fecha_fabricacion TEXT,
        lote_id TEXT
    );
    """)
    cur.execute("""
    CREATE TABLE registros_movimientos (
        id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
        id_envase TEXT,
        tipo_movimiento TEXT,
        origen_id TEXT,
        destino_id TEXT,
        fecha TEXT,
        operador TEXT,
        observaciones TEXT
    );
    """)
    cur.execute("INSERT INTO envases VALUES ('E_INIT','PET',1500,'EnVenta','2025-10-01',NULL);")
    conn.commit()
    conn.close()

@pytest.fixture(scope="module")
def client():
    # Crear DB temporal
    create_test_db()
    repositories._DB_PATH = TEST_DB
    repositories._conn = None
    app = create_app()
    app.testing = True
    client = app.test_client()
    yield client
    try:
        os.remove(TEST_DB)
    except OSError:
        pass

def test_get_envases_iniciales(client):
    rv = client.get("/api/envases")
    assert rv.status_code == 200
    data = rv.get_json()
    assert any(e["id_envase"] == "E_INIT" for e in data)

def test_crear_envase_y_listar(client):
    payload = {"id_envase": "E002", "tipo": "PET", "capacidad_ml": 1500}
    rv = client.post("/api/envases", data=json.dumps(payload), content_type="application/json")
    assert rv.status_code == 201
    created = rv.get_json()
    assert created["id_envase"] == "E002"

    rv2 = client.get("/api/envases")
    data = rv2.get_json()
    assert any(e["id_envase"] == "E002" for e in data)

def test_registrar_devolucion_actualiza_estado(client):
    payload = {"id_envase": "E003", "tipo": "PET", "capacidad_ml": 1000}
    client.post("/api/envases", data=json.dumps(payload), content_type="application/json")

    mov = {
        "id_envase": "E003",
        "tipo_movimiento": "Devolucion",
        "origen_id": "PV001",
        "destino_id": "CR001",
        "operador": "Oper1"
    }
    rv = client.post("/api/movimientos", data=json.dumps(mov), content_type="application/json")
    assert rv.status_code == 201

    rv2 = client.get("/api/envases")
    envs = rv2.get_json()
    e = next((x for x in envs if x["id_envase"] == "E003"), None)
    assert e is not None
    assert e["estado"] == "Devuelto"
