"""
RF-07 - Resumen estadístico.

Responsabilidad única:
    Calcular totales generales de los datos públicos.
"""


def build_summary(records):
    dependent = sum(r.dependent_workers or 0 for r in records)
    independent = sum(r.independent_workers or 0 for r in records)

    return {
        "records": len(records),
        "dependent_workers": dependent,
        "independent_workers": independent,
        "total_workers": dependent + independent,
        "reported_accidents": sum(
            r.reported_accidents or 0
            for r in records
        ),
        "reported_work_deaths": sum(
            r.reported_work_deaths or 0
            for r in records
        ),
    }
