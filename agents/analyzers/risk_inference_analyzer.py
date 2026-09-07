class RiskInferenceAnalyzer:
    """
    Responsible for interpreting inferred semantic risk status.
    """

    @staticmethod
    def analyze(inferred):
        inferred = inferred or {}

        return {
            "critical": bool(
                inferred.get("critical", False)
            ),
            "priority": bool(
                inferred.get("priority", False)
            ),
            "priority_attention": bool(
                inferred.get("priority_attention", False)
            ),
        }
