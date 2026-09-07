from agents.base_agent import BaseAgent
from agents.policies.recommendation_policy import RecommendationPolicy
import sys
from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# RECOMMENDATION AGENT
# ============================================================

class RecommendationAgent(BaseAgent):
    """
    Agent responsible for generating an integrated
    recommendation using the results of:

    - RiskAnalysisAgent
    - ControlAnalysisAgent
    - IncidentAnalysisAgent

    The agent does not modify SQLite or RDF.
    """

    def __init__(self):
        super().__init__("RecommendationAgent")
        self.agent_name = "RecommendationAgent"
        self.policy = RecommendationPolicy()

    def analyze(self, context):
        """
        Adapter required by BaseAgent.

        The recommendation agent keeps its existing generate()
        interface for backward compatibility.
        """
        if not isinstance(context, dict):
            raise TypeError("RecommendationAgent context must be a dictionary.")

        return self.generate(
            context["risk_analysis"],
            context["control_analysis"],
            context["incident_analysis"],
        )

    def generate(
        self,
        risk_analysis,
        control_analysis,
        incident_analysis
    ):

        if not risk_analysis or not risk_analysis.get("success"):
            return {
                "success": False,
                "agent": self.agent_name,
                "message": "Risk analysis is unavailable."
            }

        if not control_analysis or not control_analysis.get("success"):
            return {
                "success": False,
                "agent": self.agent_name,
                "message": "Control analysis is unavailable."
            }

        if not incident_analysis or not incident_analysis.get("success"):
            return {
                "success": False,
                "agent": self.agent_name,
                "message": "Incident analysis is unavailable."
            }

        risk = risk_analysis["risk"]
        control = control_analysis["analysis"]
        incident = incident_analysis["analysis"]

        result = self.policy.generate(
            risk,
            control,
            incident,
        )

        return {
            "success": True,
            "agent": self.agent_name,
            "risk_code": risk["code"],
            "recommendation": result,
        }
    


# ============================================================
# DISPLAY
# ============================================================

def display_recommendation(result):

    print()
    print("=" * 70)
    print("RISKGUARD - RECOMMENDATION AGENT")
    print("=" * 70)

    if not result["success"]:

        print(result["message"])
        return

    recommendation = result["recommendation"]

    print()
    print("RISK")
    print("-" * 70)

    print(
        f"Risk code : "
        f"{recommendation['risk_code']}"
    )

    print(
        f"Risk name : "
        f"{recommendation['risk_name']}"
    )

    print(
        f"Risk level: "
        f"{recommendation['risk_level']}"
    )

    print(
        f"Risk score: "
        f"{recommendation['risk_score']}"
    )

    print()
    print("RECOMMENDATION PRIORITY")
    print("-" * 70)

    print(
        f"Priority  : "
        f"{recommendation['priority']}"
    )

    print()
    print("SUMMARY")
    print("-" * 70)

    print(
        recommendation["summary"]
    )

    print()
    print("RECOMMENDED ACTIONS")
    print("-" * 70)

    for index, action in enumerate(
        recommendation["recommendations"],
        start=1
    ):
        print(f"{index}. {action}")

    print()
    print("JUSTIFICATION")
    print("-" * 70)

    for reason in recommendation["justification"]:
        print(f"- {reason}")

    print()
    print("=" * 70)
    print("RECOMMENDATION COMPLETED")
    print("=" * 70)


# ============================================================
# MAIN
# ============================================================

def main():

    from agents.risk_analysis_agent import (
        RiskAnalysisAgent
    )

    from agents.control_analysis_agent import (
        ControlAnalysisAgent
    )

    from agents.incident_analysis_agent import (
        IncidentAnalysisAgent
    )

    risk_agent = RiskAnalysisAgent()

    risk_analysis = risk_agent.analyze(
        "RISK-001"
    )

    control_agent = ControlAnalysisAgent()

    control_analysis = control_agent.analyze(
        risk_analysis
    )

    incident_agent = IncidentAnalysisAgent()

    incident_analysis = incident_agent.analyze(
        risk_analysis
    )

    recommendation_agent = RecommendationAgent()

    recommendation = (
        recommendation_agent.generate(
            risk_analysis,
            control_analysis,
            incident_analysis
        )
    )

    display_recommendation(
        recommendation
    )


if __name__ == "__main__":
    main()
