from dataclasses import dataclass, field
from typing import List


@dataclass
class RecommendationDTO:

    risk_code: str

    priority: str

    recommendations: List[str] = field(
        default_factory=list
    )

    justification: str = ""
