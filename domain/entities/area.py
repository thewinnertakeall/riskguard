from dataclasses import dataclass

from domain.entities.base_entity import BaseEntity


@dataclass
class Area(BaseEntity):
    """
    Domain entity representing an organizational area.
    """

    code: str = ""
    name: str = ""
    description: str = ""
    status: str = "Active"
