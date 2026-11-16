
import json
from pathlib import Path


def cargar_transacciones(ruta_archivo="data/transacciones.json"):
    """
    Lee las transacciones desde un archivo JSON.

    Retorna:
        list: Lista de transacciones obtenidas del archivo.
    """

    ruta = Path(ruta_archivo)

    try:
        with ruta.open("r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, list):
            raise ValueError(
                "El archivo debe contener una lista de transacciones."
            )

        return datos

    except FileNotFoundError:
        raise FileNotFoundError(
            f"No se encontró el archivo: {ruta}"
        )

    except json.JSONDecodeError as error:
        raise ValueError(
            f"El archivo JSON contiene errores de formato: {error}"
        )
