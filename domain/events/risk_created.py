from dataclasses import dataclass
from datetime import datetime

from domain.events.base_event import DomainEvent


@dataclass
class RiskCreatedEvent(DomainEvent):
    risk_code: str = ""
