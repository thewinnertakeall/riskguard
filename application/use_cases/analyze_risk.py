class AnalyzeRiskUseCase:
    """
    Application use case for risk analysis.
    """

    def __init__(self, coordinator):
        self.coordinator = coordinator

    def execute(self, risk_code: str):

        return self.coordinator.analyze(risk_code)
