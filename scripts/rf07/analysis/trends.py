"""
RF-07 - Análisis temporal.

Responsabilidad única:
    Agrupar accidentes y muertes por año y mes.
"""


def group_by_period(records):
    result = {}

    for record in records:
        year = record.report_year
        month = record.report_month or 0
        key = (year, month)

        if key not in result:
            result[key] = {
                "report_year": year,
                "report_month": month,
                "workers": 0,
                "reported_accidents": 0,
                "reported_work_deaths": 0,
            }

        result[key]["workers"] += (
            (record.dependent_workers or 0)
            + (record.independent_workers or 0)
        )

        result[key]["reported_accidents"] += (
            record.reported_accidents or 0
        )

        result[key]["reported_work_deaths"] += (
            record.reported_work_deaths or 0
        )

    return sorted(
        result.values(),
        key=lambda item: (
            item["report_year"],
            item["report_month"],
        ),
    )
