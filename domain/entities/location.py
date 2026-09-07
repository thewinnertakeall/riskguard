from dataclasses import dataclass

from domain.entities.base_entity import BaseEntity


@dataclass
class Location(BaseEntity):
    """
    Domain entity representing a physical location.
    """

    code: str = ""
    name: str = ""
    description: str = ""
    status: str = "Active"
