import sys
from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from agents.agent_factory import AgentFactory


# ============================================================
# COORDINATOR AGENT
# ============================================================

class CoordinatorAgent:
    """
    Coordinates the RiskGuard multi-agent workflow.

    Workflow:

    RiskAnalysisAgent
            |
            +----> ControlAnalysisAgent
            |
            +----> IncidentAnalysisAgent
            |
            +----> RecommendationAgent

    The coordinator does not modify SQLite or RDF.
    """

    def __init__(self):

        self.agent_name = "CoordinatorAgent"

    def analyze(self, risk_code):

        # ====================================================
        # STEP 1 - RISK ANALYSIS
        # ====================================================

        risk_agent = AgentFactory.create("risk")

        risk_analysis = risk_agent.analyze(
            risk_code
        )

        if not risk_analysis.get("success"):

            return {
                "success": False,
                "agent": self.agent_name,
                "message": "RiskAnalysisAgent failed."
            }

        # ====================================================
        # STEP 2 - CONTROL ANALYSIS
        # ====================================================

        control_agent = AgentFactory.create("control")

        control_analysis = control_agent.analyze(
            risk_analysis
        )

        if not control_analysis.get("success"):

            return {
                "success": False,
                "agent": self.agent_name,
                "message": "ControlAnalysisAgent failed."
            }

        # ====================================================
        # STEP 3 - INCIDENT ANALYSIS
        # ====================================================

        incident_agent = AgentFactory.create("incident")

        incident_analysis = incident_agent.analyze(
            risk_analysis
        )

        if not incident_analysis.get("success"):

            return {
                "success": False,
                "agent": self.agent_name,
                "message": "IncidentAnalysisAgent failed."
            }

        # ====================================================
        # STEP 4 - RECOMMENDATION
        # ====================================================

        recommendation_agent = AgentFactory.create("recommendation")

        recommendation = (
            recommendation_agent.generate(
                risk_analysis,
                control_analysis,
                incident_analysis
            )
        )

        if not recommendation.get("success"):

            return {
                "success": False,
                "agent": self.agent_name,
                "message": "RecommendationAgent failed."
            }

        # ====================================================
        # FINAL RESULT
        # ====================================================

        return {

            "success": True,

            "agent": self.agent_name,

            "risk_code": risk_code,

            "risk_analysis": risk_analysis,

            "control_analysis": control_analysis,

            "incident_analysis": incident_analysis,

            "recommendation": recommendation
        }


# ============================================================
# DISPLAY
# ============================================================

def display_result(result):

    print()
    print("=" * 75)
    print("RISKGUARD - MULTI-AGENT COORDINATOR")
    print("=" * 75)

    if not result["success"]:

        print()
        print("ERROR")
        print("-" * 75)
        print(result["message"])

        return

    risk = result["risk_analysis"]["risk"]

    control = result["control_analysis"]["analysis"]

    incident = result["incident_analysis"]["analysis"]

    recommendation = (
        result["recommendation"]["recommendation"]
    )

    print()
    print("MULTI-AGENT WORKFLOW")
    print("-" * 75)

    print("1. RiskAnalysisAgent       -> COMPLETED")
    print("2. ControlAnalysisAgent    -> COMPLETED")
    print("3. IncidentAnalysisAgent   -> COMPLETED")
    print("4. RecommendationAgent     -> COMPLETED")

    print()
    print("RISK SUMMARY")
    print("-" * 75)

    print(f"Code       : {risk['code']}")
    print(f"Name       : {risk['name']}")
    print(f"Level      : {risk['level']}")
    print(f"Score      : {risk['score']}")

    print()
    print("CONTROL SUMMARY")
    print("-" * 75)

    print(
        f"Controls   : "
        f"{control['total_controls']}"
    )

    print(
        f"Effectiveness : "
        f"{control['average_effectiveness']}%"
    )

    print(
        f"Control gap   : "
        f"{control['control_gap']}"
    )

    print()
    print("INCIDENT SUMMARY")
    print("-" * 75)

    print(
        f"Incidents      : "
        f"{incident['total_incidents']}"
    )

    print(
        f"High severity  : "
        f"{incident['high_severity_incidents']}"
    )

    print(
        f"Open incidents : "
        f"{incident['open_incidents']}"
    )

    print()
    print("FINAL DECISION")
    print("-" * 75)

    print(
        f"Priority : "
        f"{recommendation['priority']}"
    )

    print()
    print(
        recommendation["summary"]
    )

    print()
    print("RECOMMENDATIONS")
    print("-" * 75)

    for index, action in enumerate(
        recommendation["recommendations"],
        start=1
    ):

        print(
            f"{index}. {action}"
        )

    print()
    print("=" * 75)
    print("MULTI-AGENT ANALYSIS COMPLETED")
    print("=" * 75)


# ============================================================
# MAIN
# ============================================================

def main():

    coordinator = CoordinatorAgent()

    result = coordinator.analyze(
        "RISK-001"
    )

    display_result(
        result
    )


if __name__ == "__main__":
    main()
