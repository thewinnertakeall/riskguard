class ControlPolicy:
    """Calculates control-related metrics and decisions."""

    def analyze(self, risk, controls, incidents, inferred):
        total_controls = len(controls)

        average_effectiveness = self._average_effectiveness(controls)
        administrative_controls = self._count_administrative(controls)
        higher_hierarchy_controls = (
            total_controls - administrative_controls
        )
        high_severity_incidents = self._count_high_severity(incidents)

        control_status = self._control_status(
            total_controls,
            average_effectiveness,
        )

        control_gap, gap_reasons = self._detect_gap(
            total_controls,
            average_effectiveness,
            high_severity_incidents,
            administrative_controls,
        )

        recommendation_level = self._recommendation_level(
            control_gap,
            inferred,
        )

        return {
            "risk_code": risk["code"],
            "risk_level": risk["level"],
            "risk_score": risk["score"],
            "total_controls": total_controls,
            "average_effectiveness": round(
                average_effectiveness,
                2,
            ),
            "administrative_controls": administrative_controls,
            "higher_hierarchy_controls": higher_hierarchy_controls,
            "high_severity_incidents": high_severity_incidents,
            "control_status": control_status,
            "control_gap": control_gap,
            "gap_reasons": gap_reasons,
            "recommendation_level": recommendation_level,
        }

    @staticmethod
    def _average_effectiveness(controls):
        values = [
            control.get("effectiveness")
            for control in controls
            if control.get("effectiveness") is not None
        ]

        return sum(values) / len(values) if values else 0.0

    @staticmethod
    def _count_administrative(controls):
        return sum(
            1
            for control in controls
            if (
                "administrative"
                in (control.get("hierarchy") or "").lower()
                or
                "administrative"
                in (control.get("type") or "").lower()
            )
        )

    @staticmethod
    def _count_high_severity(incidents):
        return sum(
            1
            for incident in incidents
            if (incident.get("severity") or "").lower() == "high"
        )

    @staticmethod
    def _control_status(total_controls, average_effectiveness):
        if total_controls == 0:
            return "No controls associated"

        if average_effectiveness >= 80:
            return "High effectiveness"

        if average_effectiveness >= 50:
            return "Moderate effectiveness"

        return "Low effectiveness"

    @staticmethod
    def _detect_gap(
        total_controls,
        average_effectiveness,
        high_severity_incidents,
        administrative_controls,
    ):
        reasons = []

        if total_controls == 0:
            reasons.append(
                "No control is associated with the risk."
            )

        if average_effectiveness < 70:
            reasons.append(
                "Control effectiveness is below 70%."
            )

        if (
            high_severity_incidents > 0
            and total_controls > 0
        ):
            reasons.append(
                "High-severity incident exists despite "
                "the presence of controls."
            )

        if (
            administrative_controls == total_controls
            and total_controls > 0
        ):
            reasons.append(
                "Controls are exclusively administrative."
            )

        return bool(reasons), reasons

    @staticmethod
    def _recommendation_level(control_gap, inferred):
        if not control_gap:
            return "Normal"

        if inferred.get("priority_attention", False):
            return "Urgent"

        return "High"
