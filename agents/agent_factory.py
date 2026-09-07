from agents.risk_analysis_agent import RiskAnalysisAgent
from agents.control_analysis_agent import ControlAnalysisAgent
from agents.incident_analysis_agent import IncidentAnalysisAgent
from agents.recommendation_agent import RecommendationAgent


class AgentFactory:
    """
    Factory responsible for constructing RiskGuard agents.

    The factory centralizes agent creation so that clients
    do not need to instantiate concrete agent classes directly.
    """

    _agents = {
        "risk": RiskAnalysisAgent,
        "control": ControlAnalysisAgent,
        "incident": IncidentAnalysisAgent,
        "recommendation": RecommendationAgent,
    }

    @classmethod
    def create(cls, agent_type: str):
        """
        Create an agent according to its registered type.
        """

        if agent_type not in cls._agents:
            raise ValueError(
                f"Unknown agent type: {agent_type}"
            )

        agent_class = cls._agents[agent_type]

        return agent_class()

    @classmethod
    def supported_agents(cls):
        """
        Return the list of supported agent types.
        """

        return list(cls._agents.keys())
