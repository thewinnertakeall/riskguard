"""
RF-07 - Worker de análisis concurrente.

Responsabilidad:
    Ejecutar una tarea de análisis sobre un conjunto de registros.

Este módulo NO:
    - accede directamente a SQLite
    - realiza HTTP
    - modifica la base de datos
    - conoce FastAPI
    - contiene lógica específica de municipios, actividades, etc.
"""


def run_analysis_worker(task_name, records, analysis_function):
    """
    Ejecuta una tarea de análisis.

    Parámetros:
        task_name:
            Nombre identificador de la tarea.

        records:
            Registros previamente obtenidos por el repository.

        analysis_function:
            Función especializada que realiza el análisis.

    Retorna:
        Tupla:
            (task_name, resultado)
    """

    result = analysis_function(records)

    return task_name, result
