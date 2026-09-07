"""
RF-06 - TRANSFORM
Transforms official Colombian open-data records into
the internal RiskGuard English data model.

IMPORTANT:
- EXTRACT keeps the original source field names.
- TRANSFORM maps them to RiskGuard internal names.
- LOAD is intentionally NOT performed here.
"""

from datetime import datetime
import json
from pathlib import Path


SOURCE_NAME = "Datos Abiertos Colombia - Estadísticas Riesgos Laborales Positiva 2026"
SOURCE_URL = "https://www.datos.gov.co/resource/kwqa-xugj.json"

# ---------------------------------------------------------
# SOURCE -> RISKGUARD MAPPING
# ---------------------------------------------------------

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
    "incapermaparciar_el": "permanent_partial_disability_occupational_disease",
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
    """Normalize text without changing the source meaning."""
    if value is None:
        return None

    value = str(value).strip()

    return value if value else None


def normalize_integer(value):
    """Convert numeric source values to integers."""
    if value is None or value == "":
        return None

    return int(float(str(value).strip()))


def transform_record(source_record):
    """
    Transform ONE official source record into
    the RiskGuard internal English model.
    """

    transformed = {
        "source": SOURCE_NAME,
        "source_url": SOURCE_URL,
    }

    # -----------------------------------------------------
    # FIELD MAPPING
    # -----------------------------------------------------

    for source_field, internal_field in FIELD_MAPPING.items():

        value = source_record.get(source_field)

        if internal_field in INTEGER_FIELDS:
            value = normalize_integer(value)

        elif internal_field in TEXT_FIELDS:
            value = normalize_text(value)

        transformed[internal_field] = value

    # -----------------------------------------------------
    # BASIC VALIDATION
    # -----------------------------------------------------

    year = transformed["report_year"]
    month = transformed["report_month"]

    if year is None:
        raise ValueError("report_year is required")

    if year < 1990 or year > 2100:
        raise ValueError(f"Invalid report_year: {year}")

    if month is not None and not 1 <= month <= 12:
        raise ValueError(f"Invalid report_month: {month}")

    return transformed


def main():
    # -----------------------------------------------------
    # TEST SOURCE RECORD
    # This simulates the result returned by EXTRACT.
    # -----------------------------------------------------

    source_record = {
        "dpto": "ANTIOQUIA",
        "mpio": "MEDELLIN",
        "codigo_de_la_arl": "1423",
        "a_o_de_informe": "2026",
        "mes_de_informe": "6",
        "activec": "1131201",
        "rela_dep": "27",
        "rela_indep": "0",
        "presuaccidetrasuce": "0",
        "muertes_repor_at": "0",
        "nuevapensioinva_r_at": "0",
        "nuevapensioinva_r_el": "0",
        "incapermaparciar_at": "0",
        "incapermaparciar_el": "0",
    }

    transformed = transform_record(source_record)

    # -----------------------------------------------------
    # CONSOLE EVIDENCE
    # -----------------------------------------------------

    print()
    print("=================================================")
    print(" RF-06 — TRANSFORMACION ETL")
    print("=================================================")

    print()
    print("FUENTE:")
    print(SOURCE_NAME)
    print(SOURCE_URL)

    print()
    print("MAPEO SOURCE -> RISKGUARD")
    print("-----------------------------------------------")

    for source_field, internal_field in FIELD_MAPPING.items():

        source_value = source_record.get(source_field)
        internal_value = transformed.get(internal_field)

        print(
            f"{source_field:35} -> "
            f"{internal_field:50} "
            f"| {source_value!r} -> {internal_value!r}"
        )

    print()
    print("=================================================")
    print(" RESULTADO TRANSFORM")
    print("=================================================")

    print(json.dumps(
        transformed,
        indent=2,
        ensure_ascii=False
    ))

    # -----------------------------------------------------
    # SAVE EVIDENCE
    # -----------------------------------------------------

    evidence_dir = Path("evidence/RF-06")
    evidence_dir.mkdir(parents=True, exist_ok=True)

    evidence_file = evidence_dir / "transform_sample.json"

    evidence = {
        "timestamp": datetime.now().isoformat(),
        "source": SOURCE_NAME,
        "source_url": SOURCE_URL,
        "mapping": FIELD_MAPPING,
        "source_record": source_record,
        "transformed_record": transformed,
    }

    evidence_file.write_text(
        json.dumps(
            evidence,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    print()
    print("Evidencia generada:")
    print(evidence_file)

    print()
    print("TRANSFORM: OK")
    print("LOAD: NO EJECUTADO")


if __name__ == "__main__":
    main()
