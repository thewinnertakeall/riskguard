class RiskResultBuilder:
    """
    Builds the final result returned by RiskAnalysisAgent.
    """

    @staticmethod
    def build(
        risk,
        causes,
        controls,
        incidents,
        inferred,
    ):
        return {
            "risk": risk,
            "causes": causes,
            "controls": controls,
            "incidents": incidents,
            "inferred": inferred,
        }
