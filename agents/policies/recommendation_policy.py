class RecommendationPolicy:
    """Builds the final recommendation from agent analyses."""

    def generate(self, risk, control, incident):
        priority = self._priority(risk, control, incident)

        recommendations = self._recommendations(
            risk,
            control,
            incident,
        )

        justification = self._justification(
            risk,
            control,
            incident,
        )

        summary = self._summary(priority)

        return {
            "risk_code": risk["code"],
            "risk_name": risk["name"],
            "risk_level": risk["level"],
            "risk_score": risk["score"],
            "priority": priority,
            "summary": summary,
            "recommendations": recommendations,
            "justification": justification,
        }

    @staticmethod
    def _priority(risk, control, incident):
        priorities = [
            control["recommendation_level"],
            incident["incident_priority"],
        ]

        if (
            risk["level"] == "Critical"
            or "Urgent" in priorities
        ):
            return "Urgent"

        if (
            risk["level"] == "High"
            or "High" in priorities
        ):
            return "High"

        if "Moderate" in priorities:
            return "Moderate"

        return "Normal"

    @staticmethod
    def _recommendations(risk, control, incident):
        recommendations = []

        if risk["level"] == "Critical":
            recommendations.append(
                "Perform immediate review of the critical risk."
            )

        if control["control_gap"]:
            recommendations.append(
                "Review and strengthen the controls "
                "associated with the risk."
            )

        if control["administrative_controls"] > 0:
            recommendations.append(
                "Evaluate the implementation of controls "
                "higher in the control hierarchy."
            )

        if control["average_effectiveness"] < 70:
            recommendations.append(
                "Improve the effectiveness of existing controls."
            )

        if incident["high_severity_incidents"] > 0:
            recommendations.append(
                "Investigate the high-severity incident "
                "associated with the risk."
            )

        if incident["open_incidents"] > 0:
            recommendations.append(
                "Establish corrective actions for open incidents."
            )

        if not recommendations:
            recommendations.append(
                "Continue monitoring the risk and its controls."
            )

        return recommendations

    @staticmethod
    def _justification(risk, control, incident):
        justification = []

        if risk["score"] >= 17:
            justification.append(
                "Risk score is within the critical range."
            )

        if control["control_gap"]:
            justification.append(
                "A control gap was detected."
            )

        if incident["high_severity_incidents"] > 0:
            justification.append(
                "A high-severity incident was detected."
            )

        if incident["open_incidents"] > 0:
            justification.append(
                "An associated incident remains open."
            )

        if not justification:
            justification.append(
                "No critical conditions were detected."
            )

        return justification

    @staticmethod
    def _summary(priority):
        summaries = {
            "Urgent": (
                "Immediate intervention is recommended "
                "because the risk presents critical or "
                "urgent conditions."
            ),
            "High": (
                "Priority intervention is recommended "
                "to reduce the identified risk conditions."
            ),
            "Moderate": (
                "Preventive actions and continued monitoring "
                "are recommended."
            ),
        }

        return summaries.get(
            priority,
            "Continue monitoring the risk and maintaining "
            "existing controls.",
        )
