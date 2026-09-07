"""
RF-06
TRANSFORM: convierte registros de la fuente pública
al modelo interno de RiskGuard.
"""

from scripts.rf06.config import (
    SOURCE_NAME,
    SOURCE_URL,
)


FIELD_MAPPING = {
    "dpto": "department",
    "mpio": "municipality",
    "codigo_de_la_arl": "arl_code",
    "a_o_de_informe": "report_year",
    "mes_de_informe": "report_month",
    "activec": "economic_activity_code",
    "rela_dep": "dependent_workers",
    "rela_indep": "independent_workers",
    "presuaccidetrasuce": "reported_accidents",
    "muertes_repor_at": "reported_work_deaths",
    "nuevapensioinva_r_at": "disability_pension_accident",
    "nuevapensioinva_r_el": "disability_pension_occupational_disease",
    "incapermaparciar_at": "permanent_partial_disability_accident",
    "incapermaparciar_el": (
        "permanent_partial_disability_occupational_disease"
    ),
}


INTEGER_FIELDS = {
    "report_year",
    "report_month",
    "dependent_workers",
    "independent_workers",
    "reported_accidents",
    "reported_work_deaths",
    "disability_pension_accident",
    "disability_pension_occupational_disease",
    "permanent_partial_disability_accident",
    "permanent_partial_disability_occupational_disease",
}


TEXT_FIELDS = {
    "department",
    "municipality",
    "arl_code",
    "economic_activity_code",
}


def normalize_text(value):
    if value is None:
        return None

    value = str(value).strip()

    return value if value else None


def normalize_integer(value):
    if value is None or value == "":
        return None

    return int(float(str(value).strip()))


def transform_record(source_record):
    """
    Transforma un único registro original.
    No accede a la base de datos.
    No realiza HTTP.
    """

    transformed = {
        "source": SOURCE_NAME,
        "source_url": SOURCE_URL,
    }

    for source_field, internal_field in FIELD_MAPPING.items():

        value = source_record.get(source_field)

        if internal_field in INTEGER_FIELDS:
            value = normalize_integer(value)

        elif internal_field in TEXT_FIELDS:
            value = normalize_text(value)

        transformed[internal_field] = value

    validate_record(transformed)

    return transformed


def validate_record(record):
    """
    Valida únicamente las reglas necesarias
    para el modelo externo de RiskGuard.
    """

    year = record["report_year"]

    if year is None:
        raise ValueError(
            "report_year es obligatorio"
        )

    if year < 1990 or year > 2100:
        raise ValueError(
            f"report_year inválido: {year}"
        )

    month = record["report_month"]

    if month is not None and not 1 <= month <= 12:
        raise ValueError(
            f"report_month inválido: {month}"
        )


def transform_records(source_records):
    """
    Transforma una colección de registros.
    """

    return [
        transform_record(record)
        for record in source_records
    ]
