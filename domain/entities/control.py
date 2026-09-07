from dataclasses import dataclass

from domain.entities.base_entity import BaseEntity


@dataclass
class Control(BaseEntity):
    """
    Domain entity representing a risk control.
    """

    code: str = ""
    name: str = ""
    description: str = ""

    control_type: str = ""
    hierarchy_level: str = ""

    effectiveness: float = 0.0
    status: str = "Active"

    def is_effective(self) -> bool:
        return self.effectiveness >= 80.0
