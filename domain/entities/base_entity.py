from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar


EntityId = TypeVar("EntityId")


@dataclass
class BaseEntity(ABC, Generic[EntityId]):
    """
    Base entity for RiskGuard domain objects.

    Entities are identified by a stable identity rather than
    only by their attributes.
    """

    id: EntityId
