# repositories/__init__.py
# -------------------------------------------------------
# Proveedor de conexión SQLite y utilidades simples.
# Uso: from repositories import db, query_one, query_all, execute
# -------------------------------------------------------
import sqlite3
import threading

_DB_PATH = "postobon.db"
_lock = threading.Lock()
_conn = None

def get_connection():
    """
    Retorna una conexión SQLite única por proceso (simple singleton).
    Configura row_factory para dict-like rows.
    """
    global _conn
    if _conn is None:
        with _lock:
            if _conn is None:
                _conn = sqlite3.connect(_DB_PATH, check_same_thread=False)
                _conn.row_factory = sqlite3.Row
    return _conn

def query_all(sql, params=()):
    """
    Devuelve lista de dicts (rows) para SELECTs.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    return [dict(r) for r in rows]

def query_one(sql, params=()):
    """
    Devuelve un solo registro o None.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params)
    row = cur.fetchone()
    return dict(row) if row else None

def execute(sql, params=()):
    """
    Ejecuta INSERT/UPDATE/DELETE y retorna lastrowid si aplica.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    return cur.lastrowid
