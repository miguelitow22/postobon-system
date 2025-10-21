# api/__init__.py
# -------------------------------------------------------
# Blueprints Flask con endpoints REST completos.
# -------------------------------------------------------
from flask import Blueprint, jsonify, request
from services import (
    create_envase,
    get_envases,
    get_envase_by_id,
    update_envase_estado,
    registrar_movimiento,
    porcentaje_recuperacion,
)
from repositories import execute
from models import Envase, RegistroMovimiento

bp = Blueprint("api", __name__, url_prefix="/api")

# --- Envases ---
@bp.route("/envases", methods=["GET"])
def api_get_envases():
    envs = get_envases()
    return jsonify(envs), 200


@bp.route("/envases", methods=["POST"])
def api_create_envase():
    data = request.get_json()
    required = ("id_envase", "tipo", "capacidad_ml")
    if not data or not all(k in data for k in required):
        return jsonify({"error": "Faltan campos requeridos"}), 400
    env = Envase(
        id_envase=data["id_envase"],
        tipo=data["tipo"],
        capacidad_ml=int(data["capacidad_ml"]),
        fecha_fabricacion=data.get("fecha_fabricacion"),
        lote_id=data.get("lote_id"),
    )
    created = create_envase(env)
    return jsonify(created), 201


@bp.route("/envases/<string:id_envase>", methods=["PUT"])
def api_update_envase(id_envase):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Datos requeridos"}), 400

    sql = """
        UPDATE envases 
        SET tipo=?, capacidad_ml=?, estado=? 
        WHERE id_envase=?
    """
    execute(
        sql,
        (
            data.get("tipo"),
            data.get("capacidad_ml"),
            data.get("estado"),
            id_envase,
        ),
    )
    return jsonify({"message": "Envase actualizado"}), 200


@bp.route("/envases/<string:id_envase>", methods=["DELETE"])
def api_delete_envase(id_envase):
    execute("DELETE FROM envases WHERE id_envase=?", (id_envase,))
    return jsonify({"message": "Envase eliminado"}), 200


@bp.route("/envases/<string:id_envase>/estado", methods=["PUT"])
def api_update_estado(id_envase):
    data = request.get_json()
    if not data or "nuevo_estado" not in data:
        return jsonify({"error": "Falta 'nuevo_estado'"}), 400
    updated, err = update_envase_estado(id_envase, data["nuevo_estado"])
    if err:
        return jsonify({"error": err}), 400
    return jsonify(updated), 200


# --- Movimientos ---
@bp.route("/movimientos", methods=["POST"])
def api_registrar_movimiento():
    data = request.get_json()
    required = ("id_envase", "tipo_movimiento")
    if not data or not all(k in data for k in required):
        return jsonify({"error": "Faltan campos requeridos"}), 400
    mov = RegistroMovimiento(
        id_envase=data["id_envase"],
        tipo_movimiento=data["tipo_movimiento"],
        origen_id=data.get("origen_id"),
        destino_id=data.get("destino_id"),
        fecha=data.get("fecha"),
        operador=data.get("operador"),
        observaciones=data.get("observaciones"),
    )
    result = registrar_movimiento(mov)
    return jsonify(result), 201


# --- Reportes ---
@bp.route("/reportes/recuperacion", methods=["GET"])
def api_reporte_recuperacion():
    inicio = request.args.get("inicio")
    fin = request.args.get("fin")
    report = porcentaje_recuperacion(inicio, fin)
    return jsonify(report), 200


# --- Healthcheck ---
@bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

# --- LOTES ---
@bp.route("/lotes", methods=["GET"])
def api_get_lotes():
    from repositories import query_all
    lotes = query_all("SELECT * FROM lotes")
    return jsonify(lotes), 200


@bp.route("/lotes/<string:id_lote>", methods=["GET"])
def api_get_lote(id_lote):
    from repositories import query_one
    lote = query_one("SELECT * FROM lotes WHERE id_lote=?", (id_lote,))
    if not lote:
        return jsonify({"error": "Lote no encontrado"}), 404
    return jsonify(lote), 200


@bp.route("/lotes", methods=["POST"])
def api_create_lote():
    from repositories import execute
    data = request.get_json()
    if not data or "id_lote" not in data:
        return jsonify({"error": "Falta id_lote"}), 400
    execute(
        "INSERT INTO lotes (id_lote, fecha_salida, punto_origen_id, estado) VALUES (?, datetime('now'), ?, ?)",
        (data["id_lote"], data.get("punto_origen_id"), data.get("estado", "Pendiente")),
    )
    return jsonify({"message": "Lote creado"}), 201


@bp.route("/lotes/<string:id_lote>", methods=["PUT"])
def api_update_lote(id_lote):
    from repositories import execute
    data = request.get_json()
    execute(
        "UPDATE lotes SET punto_origen_id=?, estado=? WHERE id_lote=?",
        (data.get("punto_origen_id"), data.get("estado"), id_lote),
    )
    return jsonify({"message": "Lote actualizado"}), 200


@bp.route("/lotes/<string:id_lote>", methods=["DELETE"])
def api_delete_lote(id_lote):
    from repositories import execute
    execute("DELETE FROM lotes WHERE id_lote=?", (id_lote,))
    return jsonify({"message": "Lote eliminado"}), 200

# --- MOVIMIENTOS ---
@bp.route("/movimientos", methods=["GET"])
def api_get_movimientos():
    from repositories import query_all
    movimientos = query_all("SELECT * FROM registros_movimientos ORDER BY fecha DESC")
    return jsonify(movimientos), 200


@bp.route("/movimientos", methods=["POST"])
def api_create_movimiento():
    from repositories import execute
    data = request.get_json()
    required = ("id_envase", "tipo_movimiento", "origen_id", "destino_id", "operador")
    if not data or not all(k in data for k in required):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    execute(
        """
        INSERT INTO registros_movimientos (id_envase, tipo_movimiento, origen_id, destino_id, fecha, operador, observaciones)
        VALUES (?, ?, ?, ?, datetime('now'), ?, ?)
        """,
        (
            data["id_envase"],
            data["tipo_movimiento"],
            data["origen_id"],
            data["destino_id"],
            data["operador"],
            data.get("observaciones"),
        ),
    )
    return jsonify({"message": "Movimiento registrado exitosamente"}), 201
