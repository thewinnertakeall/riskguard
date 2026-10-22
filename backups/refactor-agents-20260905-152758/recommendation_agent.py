from agents.base_agent import BaseAgent
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

        # ====================================================
        # PRIORITY
        # ====================================================

        priorities = [
            control["recommendation_level"],
            incident["incident_priority"]
        ]

        if (
            risk["level"] == "Critical"
            or "Urgent" in priorities
        ):
            priority = "Urgent"

        elif (
            risk["level"] == "High"
            or "High" in priorities
        ):
            priority = "High"

        elif "Moderate" in priorities:
            priority = "Moderate"

        else:
            priority = "Normal"

        # ====================================================
        # RECOMMENDATIONS
        # ====================================================

        recommendations = []

        if risk["level"] == "Critical":
            recommendations.append(
                "Perform immediate review of the critical risk."
            )

        if control["control_gap"]:

            recommendations.append(
                "Review and strengthen the controls "
                "associated with the risk."
            )

        if control["administrative_controls"] > 0:

            recommendations.append(
                "Evaluate the implementation of controls "
                "higher in the control hierarchy."
            )

        if (
            control["average_effectiveness"] < 70
        ):

            recommendations.append(
                "Improve the effectiveness of existing controls."
            )

        if incident["high_severity_incidents"] > 0:

            recommendations.append(
                "Investigate the high-severity incident "
                "associated with the risk."
            )

        if incident["open_incidents"] > 0:

            recommendations.append(
                "Establish corrective actions for open incidents."
            )

        if not recommendations:

            recommendations.append(
                "Continue monitoring the risk and its controls."
            )

        # ====================================================
        # JUSTIFICATION
        # ====================================================

        justification = []

        if risk["score"] >= 17:
            justification.append(
                "Risk score is within the critical range."
            )

        if control["control_gap"]:
            justification.append(
                "A control gap was detected."
            )

        if incident["high_severity_incidents"] > 0:
            justification.append(
                "A high-severity incident was detected."
            )

        if incident["open_incidents"] > 0:
            justification.append(
                "An associated incident remains open."
            )

        if not justification:
            justification.append(
                "No critical conditions were detected."
            )

        # ====================================================
        # FINAL RECOMMENDATION
        # ====================================================

        if priority == "Urgent":

            summary = (
                "Immediate intervention is recommended "
                "because the risk presents critical or "
                "urgent conditions."
            )

        elif priority == "High":

            summary = (
                "Priority intervention is recommended "
                "to reduce the identified risk conditions."
            )

        elif priority == "Moderate":

            summary = (
                "Preventive actions and continued monitoring "
                "are recommended."
            )

        else:

            summary = (
                "Continue monitoring the risk and maintaining "
                "existing controls."
            )

        # ====================================================
        # RESULT
        # ====================================================

        result = {

            "risk_code": risk["code"],

            "risk_name": risk["name"],

            "risk_level": risk["level"],

            "risk_score": risk["score"],

            "priority": priority,

            "summary": summary,

            "recommendations": recommendations,

            "justification": justification
        }

        return {

            "success": True,

            "agent": self.agent_name,

            "risk_code": risk["code"],

            "recommendation": result
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
