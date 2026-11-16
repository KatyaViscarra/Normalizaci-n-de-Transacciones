
import json
from pathlib import Path
from datetime import datetime
from decimal import Decimal, InvalidOperation


# Equivalencias de campos según la fuente
MAPEO_CAMPOS = {
    "paypal": {
        "id": "transaction_id",
        "monto": "amount",
        "moneda": "currency",
        "estado": "status",
        "fecha": "created_at",
        "descripcion": "description"
    },
    "stripe": {
        "id": "id",
        "monto": "total",
        "moneda": "currency_code",
        "estado": "payment_status",
        "fecha": "created",
        "descripcion": "description"
    },
    "banco": {
        "id": "referencia",
        "monto": "monto",
        "moneda": "moneda",
        "estado": "estado",
        "fecha": "fecha_operacion",
        "descripcion": "detalle"
    }
    
}

FIRMAS_FUENTE = {
    "paypal": "transaction_id",
    "stripe": "payment_status",
    "banco": "referencia",
}

def detectar_fuente(transaccion):
    """Usa el campo 'fuente'; si falta, la infiere por los campos propios."""
    fuente = str(transaccion.get("fuente", "")).strip().lower()
    if fuente:
        return fuente
    for nombre, campo in FIRMAS_FUENTE.items():
        if campo in transaccion:
            return nombre
    return fuente


def cargar_reglas(ruta="config/reglas.json"):
    """Carga las reglas de normalización desde el archivo JSON."""

    ruta_completa = Path(__file__).parent / ruta

    with ruta_completa.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def normalizar_monto(valor):
    """Convierte un monto válido a Decimal."""

    if valor is None or isinstance(valor, bool):
        return None

    try:
        monto = Decimal(str(valor).strip())

        if not monto.is_finite():
            return None

        return monto

    except (InvalidOperation, ValueError, TypeError):
        return None


def normalizar_fecha(valor, formatos):
    """Convierte diferentes formatos de fecha a AAAA-MM-DD."""

    if not isinstance(valor, str) or not valor.strip():
        return None

    for formato in formatos:
        try:
            fecha = datetime.strptime(valor.strip(), formato)
            return fecha.strftime("%Y-%m-%d")

        except ValueError:
            continue

    return None


def normalizar_transaccion(transaccion, reglas):
    """Transforma una transacción al modelo de datos común."""

    if not isinstance(transaccion, dict):
        transaccion = {}

    fuente = detectar_fuente(transaccion)

    mapeo = MAPEO_CAMPOS.get(fuente, {})

    def obtener_campo(nombre):
        campo_original = mapeo.get(nombre)
        return transaccion.get(campo_original) if campo_original else None

    monto = normalizar_monto(obtener_campo("monto"))

    moneda_original = obtener_campo("moneda")
    moneda = (
        str(moneda_original).strip().upper()
        if moneda_original is not None
        else None
    )

    estado_original = obtener_campo("estado")
    estado_clave = (
        str(estado_original).strip().lower()
        if estado_original is not None
        else ""
    )

    estado = reglas["estados"].get(estado_clave)

    fecha = normalizar_fecha(
        obtener_campo("fecha"),
        reglas["formatos_fecha"]
    )

    identificador = obtener_campo("id")
    descripcion = obtener_campo("descripcion")

    return {
        "id": (
            str(identificador).strip()
            if identificador is not None
            else None
        ),
        "fuente": fuente,
        "monto": monto,
        "moneda": moneda,
        "estado": estado,
        "fecha": fecha,
        "descripcion": (
            str(descripcion).strip()
            if descripcion is not None
            else None
        ),
        "valida": True,
        "errores": [],
        "raw_data": transaccion
    }


def normalizar_transacciones(transacciones, reglas=None):
    """Normaliza una lista completa de transacciones."""

    if reglas is None:
        reglas = cargar_reglas()

    return [
        normalizar_transaccion(transaccion, reglas)
        for transaccion in transacciones
    ]
