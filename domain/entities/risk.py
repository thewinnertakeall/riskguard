from dataclasses import dataclass, field
from typing import List

from domain.entities.base_entity import BaseEntity
from domain.value_objects.risk_score import RiskScore
from domain.value_objects.risk_level import RiskLevel


@dataclass
class Risk(BaseEntity[str]):
    code: str
    name: str
    description: str
    category: str
    probability: int
    impact: int
    status: str = "Active"

    controls: List[str] = field(default_factory=list)
    incidents: List[str] = field(default_factory=list)
    iso_controls: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)

    @property
    def score(self) -> RiskScore:
        return RiskScore(
            probability=self.probability,
            impact=self.impact,
        )

    @property
    def level(self) -> RiskLevel:
        return RiskLevel.from_score(self.score.value)

    @property
    def is_priority(self) -> bool:
        return self.level == RiskLevel.CRITICAL

    def add_iso_control(self, control_code: str) -> None:
        if control_code not in self.iso_controls:
            self.iso_controls.append(control_code)

    def add_evidence(self, evidence_code: str) -> None:
        if evidence_code not in self.evidence:
            self.evidence.append(evidence_code)
