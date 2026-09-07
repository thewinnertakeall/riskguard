import StatCard from "../components/common/StatCard";
import RiskBadge from "../components/common/RiskBadge";
import AgentResults from "../components/agents/AgentResults";

export default function MultiAgentView({
  risks,
  selectedRisk,
  setSelectedRisk,
  analysis,
  handleAnalyze,
  analysisLoading
}) {
  return (
    <>
      <section className="stats-grid">

        <StatCard
          title="Risk Agent"
          value="READY"
          icon="◈"
          description="Risk analysis"
        />

        <StatCard
          title="Control Agent"
          value="READY"
          icon="◆"
          description="Control analysis"
        />

        <StatCard
          title="Incident Agent"
          value="READY"
          icon="●"
          description="Incident analysis"
        />

        <StatCard
          title="Coordinator"
          value="READY"
          icon="◎"
          description="Decision coordination"
        />

      </section>

      <div className="panel">

        <div className="panel-header">

          <div>
            <h2>Multi-Agent Intelligence</h2>
            <p>
              Select a risk and execute the CoordinatorAgent.
            </p>
          </div>

        </div>

        {risks.length === 0 ? (

          <div className="empty-state">
            No risks available for analysis.
          </div>

        ) : (

          <>
            <div className="risk-table-wrapper">

              <table className="risk-table">

                <thead>
                  <tr>
                    <th>Code</th>
                    <th>Risk</th>
                    <th>Score</th>
                    <th>Level</th>
                    <th></th>
                  </tr>
                </thead>

                <tbody>

                  {risks.map((risk) => (

                    <tr
                      key={risk.id || risk.code}
                      className={
                        selectedRisk?.code === risk.code
                          ? "selected-row"
                          : ""
                      }
                    >

                      <td>
                        <strong>{risk.code}</strong>
                      </td>

                      <td>
                        {risk.name}
                      </td>

                      <td>
                        {risk.risk_score}
                      </td>

                      <td>
                        <RiskBadge level={risk.risk_level} />
                      </td>

                      <td>

                        <button
                          className="analyze-button"
                          onClick={() => {
                            setSelectedRisk(risk);
                            handleAnalyze(risk);
                          }}
                          disabled={analysisLoading}
                        >
                          Analyze
                        </button>

                      </td>

                    </tr>

                  ))}

                </tbody>

              </table>

            </div>

            {selectedRisk && (

              <div className="selected-risk">

                <div className="selected-risk-header">

                  <div>

                    <span className="risk-code">
                      {selectedRisk.code}
                    </span>

                    <h3>
                      {selectedRisk.name}
                    </h3>

                  </div>

                  <div className="score-display">

                    <span>Risk Score</span>

                    <strong>
                      {selectedRisk.risk_score}
                    </strong>

                    <small>/ 25</small>

                  </div>

                </div>

                <button
                  className="primary-button full-width"
                  onClick={() => handleAnalyze(selectedRisk)}
                  disabled={analysisLoading}
                >
                  {analysisLoading
                    ? "Running agents..."
                    : "Run CoordinatorAgent"}
                </button>

                {analysis && (
                  <AgentResults analysis={analysis} />
                )}

              </div>

            )}

          </>
        )}

      </div>
    </>
  );
}
