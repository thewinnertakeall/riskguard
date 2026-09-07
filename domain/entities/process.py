from dataclasses import dataclass

from domain.entities.base_entity import BaseEntity


@dataclass
class Process(BaseEntity):
    """
    Domain entity representing an organizational process.
    """

    code: str = ""
    name: str = ""
    description: str = ""
    status: str = "Active"
