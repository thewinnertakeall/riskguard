from typing import Optional

from sqlalchemy.orm import Session

from app.models import Risk as RiskModel

from domain.entities.risk import Risk
from domain.interfaces.risk_repository import RiskRepository


class SQLRiskRepository(RiskRepository):

    def __init__(self, session: Session):
        self.session = session

    def _to_entity(self, model: RiskModel) -> Risk:
        return Risk(
            code=model.code,
            name=model.name,
            probability=model.probability,
            impact=model.impact,
            description=model.description,
            category=model.category,
            status=model.status,
        )

    def find_by_id(self, risk_id: int) -> Optional[Risk]:
        model = (
            self.session
            .query(RiskModel)
            .filter(RiskModel.id == risk_id)
            .first()
        )

        if model is None:
            return None

        return self._to_entity(model)

    def find_by_code(self, code: str) -> Optional[Risk]:
        model = (
            self.session
            .query(RiskModel)
            .filter(RiskModel.code == code)
            .first()
        )

        if model is None:
            return None

        return self._to_entity(model)

    def find_all(self) -> list[Risk]:
        models = (
            self.session
            .query(RiskModel)
            .order_by(RiskModel.id)
            .all()
        )

        return [self._to_entity(model) for model in models]

    def save(self, risk: Risk) -> Risk:
        model = (
            self.session
            .query(RiskModel)
            .filter(RiskModel.code == risk.code)
            .first()
        )

        if model is None:
            model = RiskModel(
                code=risk.code,
                name=risk.name,
                description=risk.description,
                category=risk.category,
                probability=risk.probability,
                impact=risk.impact,
                risk_score=risk.calculate_score(),
                risk_level=risk.classify(),
                status=risk.status,
            )

            self.session.add(model)

        else:
            model.name = risk.name
            model.description = risk.description
            model.category = risk.category
            model.probability = risk.probability
            model.impact = risk.impact
            model.risk_score = risk.calculate_score()
            model.risk_level = risk.classify()
            model.status = risk.status

        self.session.commit()
        self.session.refresh(model)

        return self._to_entity(model)
