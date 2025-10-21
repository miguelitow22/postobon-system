# app.py
# -------------------------------------------------------
# Punto de entrada Flask. Ejecuta el servidor completo:
# - API (backend lógico)
# - Frontend (vistas HTML con Bootstrap)
# -------------------------------------------------------
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from api import bp as api_bp
import logging

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(api_bp, url_prefix="/api")

    # ------------------------------
    # VISTAS FRONTEND
    # ------------------------------
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/envases")
    def envases():
        return render_template("envases.html")

    @app.route("/lotes")
    def lotes():
        return render_template("lotes.html")

    @app.route("/movimientos")
    def movimientos():
        return render_template("movimientos.html")

    # ------------------------------
    # MANEJO DE ERRORES Y LOGGING
    # ------------------------------
    logging.basicConfig(level=logging.INFO)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Ruta no encontrada"}), 404

    # ------------------------------
    # API DE PRUEBA
    # ------------------------------
    @app.route("/api/saludo")
    def saludo():
        return jsonify({"mensaje": "Hola Miguel, tu API Postobón está viva 💪"})

    return app

# ------------------------------
# Creamos el objeto WSGI para Gunicorn
# ------------------------------
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)