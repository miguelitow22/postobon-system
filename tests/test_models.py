# tests/test_models.py
import pytest
from models import Envase, EstadoEnvase

def test_envase_cambio_estado_valido():
    e = Envase(id_envase="E_TEST", tipo="PET", capacidad_ml=1500)
    assert e.estado == EstadoEnvase.EN_PLANTA.value

    # cambiar a EnVenta
    e.cambiar_estado(EstadoEnvase.EN_VENTA.value)
    assert e.estado == EstadoEnvase.EN_VENTA.value

def test_envase_no_cambiar_desde_retirado():
    e = Envase(id_envase="E_TEST2", tipo="VIDRIO", capacidad_ml=500)
    # forzamos estado retirado
    e.estado = EstadoEnvase.RETIRADO.value
    with pytest.raises(ValueError):
        e.cambiar_estado(EstadoEnvase.EN_VENTA.value)
