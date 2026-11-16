
from decimal import Decimal


def validar_transaccion(transaccion, reglas):
    """
    Valida una transacción normalizada.

    Retorna la misma transacción con:
    - valida: True o False.
    - errores: lista de inconsistencias encontradas.
    """

    errores = []

    # 1. Validar identificador
    identificador = transaccion.get("id")

    if identificador is None or not str(identificador).strip():
        errores.append("Identificador faltante o vacío")

    # 2. Validar fuente
    fuente = transaccion.get("fuente")

    if fuente not in reglas["fuentes_soportadas"]:
        errores.append("Fuente no soportada")

    # 3. Validar monto
    monto = transaccion.get("monto")

    if monto is None or not isinstance(monto, Decimal):
        errores.append("Monto inválido o no numérico")

    elif not monto.is_finite():
        errores.append("El monto no es un número finito")

    elif monto == 0:
        errores.append("El monto no puede ser cero")

    elif monto < 0 and not reglas["permitir_montos_negativos"]:
        errores.append("Los montos negativos no están permitidos")

    # 4. Validar moneda
    moneda = transaccion.get("moneda")

    if moneda not in reglas["monedas_soportadas"]:
        errores.append("Moneda no soportada")

    # 5. Validar estado
    estado = transaccion.get("estado")

    estados_validos = set(reglas["estados"].values())

    if estado not in estados_validos:
        errores.append("Estado desconocido o no soportado")

    # 6. Validar fecha
    fecha = transaccion.get("fecha")

    if fecha is None:
        errores.append("Fecha inválida o faltante")

    # Actualizar el resultado de validación
    transaccion["valida"] = len(errores) == 0
    transaccion["errores"] = errores

    return transaccion


def validar_transacciones(transacciones, reglas):
    """
    Valida todas las transacciones normalizadas.

    Retorna:
        validas: lista de transacciones correctas.
        invalidas: lista de transacciones con errores.
    """

    validas = []
    invalidas = []

    for transaccion in transacciones:
        resultado = validar_transaccion(transaccion, reglas)

        if resultado["valida"]:
            validas.append(resultado)
        else:
            invalidas.append(resultado)

    return validas, invalidas
