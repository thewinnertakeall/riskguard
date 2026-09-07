from pydantic import BaseModel


class RiskResponse(BaseModel):
    code: str
    name: str
    description: str | None
    category: str | None
    probability: int
    impact: int
    risk_score: int
    risk_level: str
    status: str | None

    model_config = {
        "from_attributes": True
    }
