from enum import Enum


class RiskLevel(str, Enum):
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"
    CRITICAL = "Critical"

    @classmethod
    def from_score(cls, score: int) -> "RiskLevel":
        if score >= 17:
            return cls.CRITICAL

        if score >= 10:
            return cls.HIGH

        if score >= 5:
            return cls.MODERATE

        return cls.LOW
