
from decimal import Decimal, InvalidOperation


def calcular_metricas(validas, invalidas):
    """
    Calcula las métricas generales de las transacciones.
    Los totales monetarios incluyen únicamente registros válidos.
    """

    total_procesadas = len(validas) + len(invalidas)

    # Conteo de transacciones por estado
    conteo_estados = {}

    for transaccion in validas:
        estado = transaccion["estado"]

        conteo_estados[estado] = (
            conteo_estados.get(estado, 0) + 1
        )

    # Totales netos por moneda
    totales_moneda = {}

    for transaccion in validas:
        moneda = transaccion["moneda"]
        monto = transaccion["monto"]

        try:
            monto = Decimal(str(monto))
        except (InvalidOperation, ValueError):
            continue

        totales_moneda[moneda] = (
            totales_moneda.get(moneda, Decimal("0")) + monto
        )

    # Porcentajes
    porcentaje_validas = (
        (len(validas) / total_procesadas) * 100
        if total_procesadas else 0
    )

    porcentaje_invalidas = (
        (len(invalidas) / total_procesadas) * 100
        if total_procesadas else 0
    )

    return {
        "total_procesadas": total_procesadas,
        "total_validas": len(validas),
        "total_invalidas": len(invalidas),
        "porcentaje_validas": round(porcentaje_validas, 2),
        "porcentaje_invalidas": round(porcentaje_invalidas, 2),
        "conteo_estados": conteo_estados,
        "totales_por_moneda": totales_moneda
    }
