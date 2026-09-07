"""
RF-06
Orquestador principal del ETL de datos públicos.

Responsabilidad:
    EXTRACT -> TRANSFORM -> LOAD

Este módulo NO contiene:
    - lógica HTTP
    - transformación de campos
    - lógica SQL
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from scripts.rf06.extract import extract_records
from scripts.rf06.transform import transform_records
from scripts.rf06.load import load_records


EVIDENCE_DIR = Path("evidence/RF-06")
EVIDENCE_FILE = EVIDENCE_DIR / "etl_run.json"


def run():
    print()
    print("=================================================")
    print(" RF-06 — ETL RUN")
    print("=================================================")

    # EXTRACT
    source_records = extract_records()

    print()
    print("EXTRACT:", len(source_records), "registros")

    # TRANSFORM
    transformed_records = transform_records(source_records)

    print(
        "TRANSFORM:",
        len(transformed_records),
        "registros"
    )

    # LOAD
    result = load_records(transformed_records)

    print()
    print("LOAD RESULT:")
    print("  Insertados :", result["inserted"])
    print("  Duplicados :", result["duplicates"])
    print("  Total      :", result["total"])

    evidence = {
        "rf": "RF-06",
        "executed_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "extract_records": len(source_records),
        "transform_records": len(transformed_records),
        "load": result,
    }

    EVIDENCE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with EVIDENCE_FILE.open(
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            evidence,
            file,
            indent=2,
            ensure_ascii=False
        )

    print()
    print("EVIDENCIA:", EVIDENCE_FILE)
    print()
    print("RF-06 ETL RUN: OK")

    return evidence


if __name__ == "__main__":
    run()
