from dataclasses import dataclass
from datetime import date
from typing import Optional

from domain.entities.base_entity import BaseEntity


@dataclass
class Incident(BaseEntity):
    """
    Domain entity representing an occupational incident.
    """

    code: str = ""
    title: str = ""
    description: str = ""

    incident_date: Optional[date] = None
    incident_type: str = ""
    severity: str = ""
    status: str = "Open"

    def is_high_severity(self) -> bool:
        return self.severity.lower() == "high"

    def is_open(self) -> bool:
        return self.status.lower() == "open"
