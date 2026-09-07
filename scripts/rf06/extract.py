"""
RF-06
EXTRACT: obtiene registros desde la fuente pública oficial.

Responsabilidad:
    - consultar la API pública
    - paginar los resultados
    - devolver registros originales

Este módulo NO:
    - transforma campos
    - carga la base de datos
    - calcula indicadores
"""

import requests

from scripts.rf06.config import (
    SOURCE_URL,
    API_LIMIT,
)


def fetch_page(offset, limit):
    """
    Obtiene una página de registros desde la API pública.
    """

    response = requests.get(
        SOURCE_URL,
        params={
            "$limit": limit,
            "$offset": offset,
        },
        timeout=30,
    )

    response.raise_for_status()

    records = response.json()

    if not isinstance(records, list):
        raise ValueError(
            "La respuesta de la API no es una lista"
        )

    return records


def extract_records():
    """
    Obtiene todos los registros disponibles mediante paginación.

    API_LIMIT define el tamaño de cada página.
    """

    records = []
    offset = 0

    while True:
        page = fetch_page(
            offset=offset,
            limit=API_LIMIT,
        )

        if not page:
            break

        records.extend(page)

        if len(page) < API_LIMIT:
            break

        offset += API_LIMIT

    return records
