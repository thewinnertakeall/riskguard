"""
RF-07 - Análisis por actividad económica.

Responsabilidad única:
    Agrupar trabajadores, accidentes y muertes
    por actividad económica.
"""


def group_by_activity(records):
    result = {}

    for record in records:
        activity = record.economic_activity_code or "SIN ACTIVIDAD"

        if activity not in result:
            result[activity] = {
                "economic_activity_code": activity,
                "workers": 0,
                "reported_accidents": 0,
                "reported_work_deaths": 0,
            }

        result[activity]["workers"] += (
            (record.dependent_workers or 0)
            + (record.independent_workers or 0)
        )

        result[activity]["reported_accidents"] += (
            record.reported_accidents or 0
        )

        result[activity]["reported_work_deaths"] += (
            record.reported_work_deaths or 0
        )

    return sorted(
        result.values(),
        key=lambda item: item["reported_accidents"],
        reverse=True,
    )
