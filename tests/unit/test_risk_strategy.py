from application.services.risk_classification_strategy import (
    StandardRiskClassificationStrategy
)


def test_standard_strategy():

    strategy = StandardRiskClassificationStrategy()

    assert strategy.classify(4).value == "Low"
    assert strategy.classify(9).value == "Medium"
    assert strategy.classify(16).value == "High"
    assert strategy.classify(20).value == "Critical"
