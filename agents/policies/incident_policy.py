class IncidentPolicy:
    """Calculates incident-related metrics and decisions."""

    def analyze(self, risk, incidents, inferred):
        counts = self._count_incidents(incidents)

        status = self._incident_status(
            counts["total_incidents"],
            counts["high_severity_incidents"],
            counts["open_incidents"],
        )

        gap, gap_reasons = self._detect_gap(
            counts["total_incidents"],
            counts["high_severity_incidents"],
            counts["open_incidents"],
        )

        priority = self._priority(
            counts["total_incidents"],
            counts["high_severity_incidents"],
            counts["open_incidents"],
            inferred,
        )

        return {
            "risk_code": risk["code"],
            "risk_level": risk["level"],
            "risk_score": risk["score"],
            **counts,
            "incident_status": status,
            "incident_gap": gap,
            "gap_reasons": gap_reasons,
            "incident_priority": priority,
        }

    @staticmethod
    def _count_incidents(incidents):
        total = len(incidents)
        high = 0
        open_count = 0
        accidents = 0
        near_misses = 0

        for incident in incidents:
            severity = (
                incident.get("severity") or ""
            ).lower()

            status = (
                incident.get("status") or ""
            ).lower()

            incident_type = (
                incident.get("type") or ""
            ).lower()

            if severity == "high":
                high += 1

            if status == "open":
                open_count += 1

            if "accident" in incident_type:
                accidents += 1

            if (
                "near" in incident_type
                or "near miss" in incident_type
            ):
                near_misses += 1

        return {
            "total_incidents": total,
            "high_severity_incidents": high,
            "open_incidents": open_count,
            "accident_incidents": accidents,
            "near_miss_incidents": near_misses,
        }

    @staticmethod
    def _incident_status(total, high, open_count):
        if total == 0:
            return "No incidents"

        if high > 0:
            return "High incident severity"

        if open_count > 0:
            return "Open incidents require attention"

        return "Incidents under control"

    @staticmethod
    def _detect_gap(total, high, open_count):
        reasons = []

        if total == 0:
            reasons.append(
                "No incident evidence is associated with the risk."
            )

        if high > 0:
            reasons.append(
                "At least one high-severity incident "
                "is associated with the risk."
            )

        if open_count > 0:
            reasons.append(
                "At least one associated incident remains open."
            )

        return high > 0 or open_count > 0, reasons

    @staticmethod
    def _priority(total, high, open_count, inferred):
        if (
            inferred.get("priority_attention", False)
            or high > 0
        ):
            return "Urgent"

        if open_count > 0:
            return "High"

        if total > 0:
            return "Moderate"

        return "Normal"
