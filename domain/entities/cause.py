from dataclasses import dataclass

from domain.entities.base_entity import BaseEntity


@dataclass
class Cause(BaseEntity):
    """
    Domain entity representing a risk cause.
    """

    code: str = ""
    name: str = ""
    description: str = ""

    cause_type: str = ""
    status: str = "Active"
