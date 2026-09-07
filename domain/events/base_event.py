from abc import ABC
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DomainEvent(ABC):
    occurred_at: datetime
