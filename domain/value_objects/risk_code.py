from dataclasses import dataclass


@dataclass(frozen=True)
class RiskCode:
    """
    Immutable value object for risk identifiers.
    """

    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Risk code cannot be empty.")

        if not self.value.startswith("RISK-"):
            raise ValueError(
                "Risk code must follow the RISK-XXX format."
            )
