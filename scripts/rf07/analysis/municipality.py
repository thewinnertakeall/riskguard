"""
RF-07 - Análisis por municipio.

Responsabilidad única:
    Agrupar trabajadores, accidentes y muertes por municipio.
"""


def group_by_municipality(records):
    result = {}

    for record in records:
        municipality = record.municipality or "SIN MUNICIPIO"

        if municipality not in result:
            result[municipality] = {
                "municipality": municipality,
                "workers": 0,
                "reported_accidents": 0,
                "reported_work_deaths": 0,
            }

        result[municipality]["workers"] += (
            (record.dependent_workers or 0)
            + (record.independent_workers or 0)
        )

        result[municipality]["reported_accidents"] += (
            record.reported_accidents or 0
        )

        result[municipality]["reported_work_deaths"] += (
            record.reported_work_deaths or 0
        )

    return sorted(
        result.values(),
        key=lambda item: item["reported_accidents"],
        reverse=True,
    )
