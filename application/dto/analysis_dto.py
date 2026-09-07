from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class AgentAnalysisDTO:
    """
    DTO representing the result of an agent analysis.
    """

    risk_code: str
    priority: str
    critical: bool

    control_gap: bool = False
    incident_gap: bool = False

    recommendations: List[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)
