import StatCard from "../components/common/StatCard";
import RiskBadge from "../components/common/RiskBadge";
import Metric from "../components/common/Metric";
import RiskTable from "../components/risk/RiskTable";
import AgentResults from "../components/agents/AgentResults";
import KnowledgeCard from "../components/knowledge/KnowledgeCard";
import SystemStatusPanel from "../components/common/SystemStatusPanel";

export default function DashboardView({
  risks,
  incidents,
  semantic,
  statistics,
  selectedRisk,
  analysis,
  loading,
  analysisLoading,
  syncLoading,
  handleAnalyze,
  handleSemanticSync
}) {
  return (
    <>
      <section className="stats-grid">

        <StatCard
          title="Total Risks"
          value={statistics.total}
          icon="◈"
          description="Registered risks"
        />

        <StatCard
          title="Critical"
          value={statistics.critical}
          icon="!"
          variant="critical"
          description="Immediate attention"
        />

        <StatCard
          title="High"
          value={statistics.high}
          icon="▲"
          variant="high"
          description="Requires control"
        />

        <StatCard
          title="Incidents"
          value={statistics.incidents}
          icon="●"
          variant="incident"
          description={`${statistics.openIncidents} open`}
        />

      </section>

      <section className="content-grid">

        <div className="panel risk-panel">

          <div className="panel-header">

            <div>
              <h2>Risk Register</h2>
              <p>Current occupational risk inventory</p>
            </div>

            <span className="count-badge">
              {risks.length} risks
            </span>

          </div>

          <RiskTable
            risks={risks}
            loading={loading}
            selectedRisk={selectedRisk}
            handleAnalyze={handleAnalyze}
          />

        </div>

        <div className="panel intelligence-panel">

          <div className="panel-header">

            <div>
              <h2>Selected Risk</h2>
              <p>Multi-agent intelligence</p>
            </div>

            {selectedRisk && (
              <RiskBadge level={selectedRisk.risk_level} />
            )}

          </div>

          {!selectedRisk ? (
            <div className="empty-state">
              Select a risk to begin analysis.
            </div>
          ) : (

            <div className="selected-risk">

              <div className="selected-risk-header">

                <div>
                  <span className="risk-code">
                    {selectedRisk.code}
                  </span>

                  <h3>{selectedRisk.name}</h3>
                </div>

                <div className="score-display">

                  <span>Risk Score</span>

                  <strong>
                    {selectedRisk.risk_score}
                  </strong>

                  <small>/ 25</small>

                </div>

              </div>

              <div className="risk-metrics">

                <Metric
                  label="Probability"
                  value={`${selectedRisk.probability}/5`}
                />

                <Metric
                  label="Impact"
                  value={`${selectedRisk.impact}/5`}
                />

                <Metric
                  label="Category"
                  value={selectedRisk.category || "—"}
                />

              </div>

              <button
                className="primary-button full-width"
                onClick={() => handleAnalyze(selectedRisk)}
                disabled={analysisLoading}
              >
                {analysisLoading
                  ? "Running agents..."
                  : "Run Multi-Agent Analysis"}
              </button>

              {analysis && (
                <AgentResults analysis={analysis} />
              )}

            </div>

          )}

        </div>

      </section>

      <section className="bottom-grid">

        <KnowledgeCard
          semantic={semantic}
          syncLoading={syncLoading}
          handleSemanticSync={handleSemanticSync}
        />

        <SystemStatusPanel semantic={semantic} />

      </section>
    </>
  );
}
