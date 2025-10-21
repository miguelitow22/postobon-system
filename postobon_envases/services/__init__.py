# services/__init__.py
# -------------------------------------------------------
# Lógica de negocio (servicios) que usa repositories y models.
# -------------------------------------------------------
from models import Envase, RegistroMovimiento
from repositories import query_all, query_one, execute
from datetime import datetime

# ---------- Envío / CRUD Envases ----------
def create_envase(envase: Envase):
    sql = """
    INSERT INTO envases (id_envase, tipo, capacidad_ml, estado, fecha_fabricacion, lote_id)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    fecha = envase.fecha_fabricacion or datetime.now().isoformat()
    execute(sql, (envase.id_envase, envase.tipo, envase.capacidad_ml, envase.estado, fecha, envase.lote_id))
    return envase.to_dict()

def get_envases():
    return query_all("SELECT * FROM envases ORDER BY id_envase")

def get_envase_by_id(id_envase):
    return query_one("SELECT * FROM envases WHERE id_envase = ?", (id_envase,))

def update_envase_estado(id_envase, nuevo_estado):
    current = get_envase_by_id(id_envase)
    if not current:
        return None, "Envase no encontrado"
    if current["estado"] == "Retirado":
        return None, "No se puede cambiar el estado de un envase retirado"
    sql = "UPDATE envases SET estado = ? WHERE id_envase = ?"
    execute(sql, (nuevo_estado, id_envase))
    return get_envase_by_id(id_envase), None

# ---------- Movimientos / Auditoría ----------
def registrar_movimiento(mov: RegistroMovimiento):
    sql = """
    INSERT INTO registros_movimientos (id_envase, tipo_movimiento, origen_id, destino_id, fecha, operador, observaciones)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    fecha = mov.fecha or datetime.now().isoformat()
    last_id = execute(sql, (mov.id_envase, mov.tipo_movimiento, mov.origen_id, mov.destino_id, fecha, mov.operador, mov.observaciones))
    # Si es devolución, actualizamos estado del envase
    if mov.tipo_movimiento == "Devolucion":
        execute("UPDATE envases SET estado = ? WHERE id_envase = ?", ("Devuelto", mov.id_envase))
    return {"id_registro": last_id}

# ---------- Reportes simples ----------
def porcentaje_recuperacion(fecha_inicio=None, fecha_fin=None):
    # Query simple: (devueltos / totales) * 100 por zona (si zona disponible)
    # Para prototipo usamos consulta básica por fecha
    params = ()
    where = ""
    if fecha_inicio and fecha_fin:
        where = "WHERE fecha BETWEEN ? AND ?"
        params = (fecha_inicio, fecha_fin)
    sql_tot = f"SELECT COUNT(*) as total FROM envases {where}"
    sql_dev = f"SELECT COUNT(*) as devueltos FROM registros_movimientos {where} AND tipo_movimiento = 'Devolucion'"
    total = query_one(sql_tot, params)["total"] if query_one(sql_tot, params) else 0
    devueltos = query_one(sql_dev, params)["devueltos"] if query_one(sql_dev, params) else 0
    porcentaje = (devueltos / total * 100) if total else 0.0
    return {"total": total, "devueltos": devueltos, "porcentaje": round(porcentaje, 2)}
