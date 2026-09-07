from dataclasses import dataclass


@dataclass(frozen=True)
class ControlEffectiveness:
    value: float

    def __post_init__(self):
        if not 0 <= self.value <= 100:
            raise ValueError(
                "Control effectiveness must be between 0 and 100."
            )

    @property
    def is_effective(self) -> bool:
        return self.value >= 70
