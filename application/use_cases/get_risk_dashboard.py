class GetRiskDashboardUseCase:
    """
    Aggregates the information required by the dashboard.
    """

    def __init__(
        self,
        risk_service,
        semantic_service,
        coordinator
    ):

        self.risk_service = risk_service
        self.semantic_service = semantic_service
        self.coordinator = coordinator

    def execute(self, risk_code: str):

        risk = self.risk_service.get_risk(
            risk_code
        )

        semantic = self.semantic_service.get_status()

        analysis = self.coordinator.analyze(
            risk_code
        )

        return {
            "risk": risk,
            "semantic": semantic,
            "analysis": analysis,
        }
