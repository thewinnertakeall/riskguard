import AgentCard from "./AgentCard";

export default function AgentResults({ analysis }) {
  const riskAnalysis = analysis?.risk_analysis || {};
  const controlAnalysis = analysis?.control_analysis || {};
  const incidentAnalysis = analysis?.incident_analysis || {};
  const recommendation = analysis?.recommendation || {};

  const risk = riskAnalysis.risk || {};

  return (
    <div className="agent-results">
      <div className="agent-title">
        <span className="agent-pulse"></span>
        Multi-Agent Analysis
      </div>

      <div className="agent-grid">
        <AgentCard
          name="Risk Analysis Agent"
          value={
            risk.risk_level ||
            riskAnalysis.risk_level ||
            riskAnalysis.level ||
            "Analyzed"
          }
        />

        <AgentCard
          name="Control Analysis Agent"
          value={
            controlAnalysis.control_status ||
            "Analyzed"
          }
        />

        <AgentCard
          name="Incident Analysis Agent"
          value={
            incidentAnalysis.incident_status ||
            "Analyzed"
          }
        />

        <AgentCard
          name="Recommendation Agent"
          value={
            recommendation.priority ||
            "Generated"
          }
        />
      </div>

      {recommendation.summary && (
        <div className="recommendation-box">
          <strong>Recommendation</strong>

          <p>
            {recommendation.summary}
          </p>

          {Array.isArray(recommendation.recommendations) && (
            <ul>
              {recommendation.recommendations.map(
                (item, index) => (
                  <li key={index}>{item}</li>
                )
              )}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
