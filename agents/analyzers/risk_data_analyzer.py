class RiskDataAnalyzer:
    """
    Responsible for extracting and normalizing risk-related data.

    This class does not coordinate agents and does not expose API endpoints.
    """

    @staticmethod
    def normalize_risk(data):
        if not data:
            return None

        return {
            "uri": data.get("uri"),
            "code": data.get("code"),
            "name": data.get("name"),
            "description": data.get("description"),
            "category": data.get("category"),
            "probability": data.get("probability"),
            "impact": data.get("impact"),
            "score": data.get("score"),
            "level": data.get("level"),
            "status": data.get("status"),
        }

    @staticmethod
    def normalize_causes(causes):
        return [
            {
                "uri": cause.get("uri"),
                "name": cause.get("name"),
                "type": cause.get("type"),
            }
            for cause in causes or []
        ]

    @staticmethod
    def normalize_controls(controls):
        return [
            {
                "uri": control.get("uri"),
                "name": control.get("name"),
                "type": control.get("type"),
                "hierarchy": control.get("hierarchy"),
                "effectiveness": control.get("effectiveness"),
            }
            for control in controls or []
        ]

    @staticmethod
    def normalize_incidents(incidents):
        return [
            {
                "uri": incident.get("uri"),
                "title": incident.get("title"),
                "type": incident.get("type"),
                "severity": incident.get("severity"),
                "status": incident.get("status"),
                "date": incident.get("date"),
            }
            for incident in incidents or []
        ]
