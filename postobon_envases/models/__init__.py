# models/__init__.py
# -------------------------------------------------------
# Clases de dominio simples (dataclasses) para el proyecto
# -------------------------------------------------------
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

class EstadoEnvase(Enum):
    EN_PLANTA = "EnPlanta"
    EN_DISTRIBUCION = "EnDistribucion"
    EN_VENTA = "EnVenta"
    DEVUELTO = "Devuelto"
    EN_TRANSITO = "EnTransito"
    EN_RECICLAJE = "EnReciclaje"
    RETIRADO = "Retirado"

@dataclass
class Envase:
    id_envase: str
    tipo: str             # 'PET' o 'VIDRIO'
    capacidad_ml: int
    estado: str = EstadoEnvase.EN_PLANTA.value
    fecha_fabricacion: str = None
    lote_id: str = None

    def to_dict(self):
        d = asdict(self)
        if not d.get("fecha_fabricacion"):
            d["fecha_fabricacion"] = datetime.now().isoformat()
        return d

    def cambiar_estado(self, nuevo_estado):
        """
        Cambia el estado del envase verificando reglas básicas.
        No permite cambiar el estado si ya está 'Retirado'.
        """
        if self.estado == EstadoEnvase.RETIRADO.value:
            raise ValueError("No se puede cambiar el estado de un envase retirado")
        self.estado = nuevo_estado

@dataclass
class Lote:
    id_lote: str
    fecha_salida: str = None
    punto_origen_id: str = None
    estado: str = None

    def to_dict(self):
        return asdict(self)

@dataclass
class RegistroMovimiento:
    id_registro: int = None
    id_envase: str = None
    tipo_movimiento: str = None  # 'Salida' / 'Devolucion' / 'Transferencia'
    origen_id: str = None
    destino_id: str = None
    fecha: str = None
    operador: str = None
    observaciones: str = None

    def to_dict(self):
        return asdict(self)
