import sqlite3

# ==========================
# 1️⃣ Conexión a la base de datos
# ==========================
conn = sqlite3.connect('postobon.db')
cursor = conn.cursor()

# ==========================
# 2️⃣ Eliminamos tablas previas (si existen)
# ==========================
tablas = [
    "registros_movimientos", "envases", "lotes", "puntos_venta",
    "centros_reciclaje", "rutas", "transportistas", "usuarios"
]
for tabla in tablas:
    cursor.execute(f"DROP TABLE IF EXISTS {tabla};")

# ==========================
# 3️⃣ Creación de tablas principales
# ==========================
cursor.execute("""
CREATE TABLE usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    rol TEXT NOT NULL CHECK(rol IN ('Admin', 'Operador', 'PuntoVenta', 'Auditor')),
    correo TEXT UNIQUE NOT NULL,
    contraseña TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE transportistas (
    id_transportista TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    licencia TEXT NOT NULL,
    vehiculo TEXT
);
""")

cursor.execute("""
CREATE TABLE puntos_venta (
    id_punto TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    direccion TEXT,
    zona TEXT,
    contacto TEXT
);
""")

cursor.execute("""
CREATE TABLE centros_reciclaje (
    id_centro TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    capacidad_max INTEGER,
    zona TEXT,
    contacto TEXT
);
""")

cursor.execute("""
CREATE TABLE lotes (
    id_lote TEXT PRIMARY KEY,
    fecha_salida TEXT,
    punto_origen_id TEXT,
    estado TEXT,
    FOREIGN KEY (punto_origen_id) REFERENCES puntos_venta (id_punto)
);
""")

cursor.execute("""
CREATE TABLE envases (
    id_envase TEXT PRIMARY KEY,
    tipo TEXT CHECK(tipo IN ('PET', 'VIDRIO')),
    capacidad_ml INTEGER,
    estado TEXT CHECK(estado IN ('EnPlanta','EnDistribucion','EnVenta','Devuelto','EnTransito','EnReciclaje','Retirado')),
    fecha_fabricacion TEXT,
    lote_id TEXT,
    FOREIGN KEY (lote_id) REFERENCES lotes (id_lote)
);
""")

cursor.execute("""
CREATE TABLE rutas (
    id_ruta TEXT PRIMARY KEY,
    transportista_id TEXT,
    fecha TEXT,
    estado TEXT,
    FOREIGN KEY (transportista_id) REFERENCES transportistas (id_transportista)
);
""")

cursor.execute("""
CREATE TABLE registros_movimientos (
    id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
    id_envase TEXT,
    tipo_movimiento TEXT CHECK(tipo_movimiento IN ('Salida','Devolucion','Transferencia')),
    origen_id TEXT,
    destino_id TEXT,
    fecha TEXT,
    operador TEXT,
    observaciones TEXT,
    FOREIGN KEY (id_envase) REFERENCES envases (id_envase)
);
""")

# ==========================
# 4️⃣ Insertar datos de ejemplo
# ==========================
cursor.execute("INSERT INTO usuarios (nombre, rol, correo, contraseña) VALUES ('Admin General', 'Admin', 'admin@postobon.com', '1234');")

cursor.execute("INSERT INTO transportistas VALUES ('T001', 'Carlos Restrepo', 'LIC12345', 'Camión 1');")
cursor.execute("INSERT INTO puntos_venta VALUES ('PV001', 'Tienda La 33', 'Calle 33 #45-67', 'Medellín', 'Juan Pérez');")
cursor.execute("INSERT INTO centros_reciclaje VALUES ('CR001', 'Centro Reciclaje Norte', 10000, 'Medellín', 'Ana Gómez');")
cursor.execute("INSERT INTO lotes VALUES ('L001', '2025-10-20', 'PV001', 'EnDistribucion');")
cursor.execute("INSERT INTO envases VALUES ('E001', 'PET', 1500, 'EnVenta', '2025-10-01', 'L001');")
cursor.execute("INSERT INTO rutas VALUES ('R001', 'T001', '2025-10-20', 'Activa');")
cursor.execute("INSERT INTO registros_movimientos (id_envase, tipo_movimiento, origen_id, destino_id, fecha, operador, observaciones) VALUES ('E001', 'Salida', 'Planta Principal', 'PV001', '2025-10-20', 'Operador1', 'Salida de envase PET 1500ml.');")

# ==========================
# 5️⃣ Confirmar cambios
# ==========================
conn.commit()
conn.close()

print("✅ Base de datos creada exitosamente: postobon.db")
