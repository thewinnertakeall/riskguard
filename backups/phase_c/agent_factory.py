from agents.risk_analysis_agent import RiskAnalysisAgent
from agents.control_analysis_agent import ControlAnalysisAgent
from agents.incident_analysis_agent import IncidentAnalysisAgent
from agents.recommendation_agent import RecommendationAgent


class AgentFactory:
    """
    Factory responsible for constructing agents.
    """

    @staticmethod
    def create(agent_type: str):

        agents = {
            "risk": RiskAnalysisAgent,
            "control": ControlAnalysisAgent,
            "incident": IncidentAnalysisAgent,
            "recommendation": RecommendationAgent,
        }

        if agent_type not in agents:
            raise ValueError(
                f"Unknown agent type: {agent_type}"
            )

        return agents[agent_type]()
