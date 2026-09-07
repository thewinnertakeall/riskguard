from dataclasses import dataclass


@dataclass(frozen=True)
class RiskScore:
    probability: int
    impact: int

    def __post_init__(self):
        if not 1 <= self.probability <= 5:
            raise ValueError("Probability must be between 1 and 5.")

        if not 1 <= self.impact <= 5:
            raise ValueError("Impact must be between 1 and 5.")

    @property
    def value(self) -> int:
        return self.probability * self.impact

    @property
    def is_critical(self) -> bool:
        return self.value >= 17
