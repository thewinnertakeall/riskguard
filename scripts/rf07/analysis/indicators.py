"""
RF-07 - Indicadores de riesgos laborales.

Responsabilidad única:
    Calcular indicadores generales a partir
    de los datos públicos ya cargados por RF-06.

No modifica la base de datos.
No modifica controles.
No expone endpoints.
"""


def build_indicators(records):
    dependent_workers = sum(
        record.dependent_workers or 0
        for record in records
    )

    independent_workers = sum(
        record.independent_workers or 0
        for record in records
    )

    total_workers = (
        dependent_workers
        + independent_workers
    )

    reported_accidents = sum(
        record.reported_accidents or 0
        for record in records
    )

    reported_work_deaths = sum(
        record.reported_work_deaths or 0
        for record in records
    )

    disability_pension_accident = sum(
        record.disability_pension_accident or 0
        for record in records
    )

    disability_pension_occupational_disease = sum(
        record.disability_pension_occupational_disease or 0
        for record in records
    )

    permanent_partial_disability_accident = sum(
        record.permanent_partial_disability_accident or 0
        for record in records
    )

    permanent_partial_disability_occupational_disease = sum(
        record.permanent_partial_disability_occupational_disease or 0
        for record in records
    )

    return {
        "dependent_workers": dependent_workers,
        "independent_workers": independent_workers,
        "total_workers": total_workers,
        "reported_accidents": reported_accidents,
        "reported_work_deaths": reported_work_deaths,
        "disability_pension_accident": disability_pension_accident,
        "disability_pension_occupational_disease": (
            disability_pension_occupational_disease
        ),
        "permanent_partial_disability_accident": (
            permanent_partial_disability_accident
        ),
        "permanent_partial_disability_occupational_disease": (
            permanent_partial_disability_occupational_disease
        ),
    }
