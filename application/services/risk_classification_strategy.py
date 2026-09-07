from abc import ABC, abstractmethod

from domain.value_objects.risk_level import RiskLevel


class RiskClassificationStrategy(ABC):

    @abstractmethod
    def classify(self, score: int) -> RiskLevel:
        pass


class StandardRiskClassificationStrategy(
    RiskClassificationStrategy
):
    """
    Standard RiskGuard classification strategy.
    """

    def classify(self, score: int) -> RiskLevel:

        return RiskLevel.from_score(score)
