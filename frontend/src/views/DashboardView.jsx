import StatCard from "../components/common/StatCard";
import RiskBadge from "../components/common/RiskBadge";
import Metric from "../components/common/Metric";
import RiskTable from "../components/risk/RiskTable";
import AgentResults from "../components/agents/AgentResults";
import KnowledgeCard from "../components/knowledge/KnowledgeCard";
import SystemStatusPanel from "../components/common/SystemStatusPanel";

function getRiskLevel(score) {
  if (score <= 4) return "low";
  if (score <= 9) return "medium";
  if (score <= 16) return "high";
  return "critical";
}

function getRiskLevelLabel(score) {
  if (score <= 4) return "Low";
  if (score <= 9) return "Medium";
  if (score <= 16) return "High";
  return "Critical";
}

function RiskMatrix({ risks }) {
  const probabilities = [1, 2, 3, 4, 5];
  const impacts = [5, 4, 3, 2, 1];

  function risksAt(probability, impact) {
    return risks.filter(
      (risk) =>
        Number(risk.probability) === probability &&
        Number(risk.impact) === impact
    );
  }

  return (
    <div className="executive-panel matrix-panel">
      <div className="executive-panel-header">
        <div>
          <div className="executive-section-title">
            <span className="section-icon">⌁</span>
            Matriz de Riesgo ISO 31000 (5×5)
          </div>
          <p>Distribución de los riesgos ocupacionales registrados</p>
        </div>

        <div className="matrix-legend">
          <span><i className="legend-dot low" /> Low</span>
          <span><i className="legend-dot medium" /> Medium</span>
          <span><i className="legend-dot high" /> High</span>
          <span><i className="legend-dot critical" /> Critical</span>
        </div>
      </div>

      <div className="risk-matrix">
        <div className="matrix-corner">
          <span>Impact</span>
          <span>Prob.</span>
        </div>

        {probabilities.map((probability) => (
          <div className="matrix-axis probability-axis" key={`prob-${probability}`}>
            Prob {probability}
          </div>
        ))}

        {impacts.map((impact) => (
          <div className="matrix-row" key={`impact-${impact}`}>
            <div className="matrix-axis impact-axis">
              Imp {impact}
            </div>

            {probabilities.map((probability) => {
              const score = probability * impact;
              const cellRisks = risksAt(probability, impact);
              const level = getRiskLevel(score);

              return (
                <div
                  className={`matrix-cell ${level}`}
                  key={`${probability}-${impact}`}
                  title={`${getRiskLevelLabel(score)} — ${score}/25`}
                >
                  <strong>{score}</strong>

                  {cellRisks.length > 0 && (
                    <div className="matrix-risk-list">
                      {cellRisks.map((risk) => (
                        <span key={risk.code} className="matrix-risk-code">
                          {risk.code}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        ))}
      </div>

      <div className="matrix-summary">
        <span>
          <strong>{risks.length}</strong> riesgos posicionados en la matriz
        </span>
        <span>
          Modelo: <strong>Probability × Impact</strong>
        </span>
      </div>
    </div>
  );
}

function ResidualRiskPanel({ risks }) {
  const sortedRisks = [...risks]
    .sort((a, b) => Number(b.risk_score || 0) - Number(a.risk_score || 0))
    .slice(0, 6);

  return (
    <div className="executive-panel residual-panel">
      <div className="executive-panel-header">
        <div>
          <div className="executive-section-title">
            <span className="section-icon">✓</span>
            Análisis de Riesgo
          </div>
          <p>Exposición actual de los riesgos registrados</p>
        </div>
      </div>

      <div className="residual-table-wrapper">
        <table className="residual-table">
          <thead>
            <tr>
              <th>Riesgo</th>
              <th>Inherente</th>
              <th>Prob.</th>
              <th>Impacto</th>
              <th>Nivel</th>
            </tr>
          </thead>

          <tbody>
            {sortedRisks.length === 0 ? (
              <tr>
                <td colSpan="5" className="residual-empty">
                  No risk data available.
                </td>
              </tr>
            ) : (
              sortedRisks.map((risk) => (
                <tr key={risk.code}>
                  <td>
                    <strong>{risk.code}</strong>
                    <span className="residual-risk-name">
                      {risk.name}
                    </span>
                  </td>

                  <td>
                    <span className={`score-pill ${getRiskLevel(risk.risk_score)}`}>
                      {risk.risk_score}
                    </span>
                  </td>

                  <td>{risk.probability}/5</td>
                  <td>{risk.impact}/5</td>

                  <td>
                    <span className={`level-pill ${getRiskLevel(risk.risk_score)}`}>
                      {risk.risk_level}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div className="residual-note">
        <span>●</span>
        Residual treatment is displayed when control-treatment data is available.
      </div>
    </div>
  );
}

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
  handleSemanticSync,
  isoCompliance
}) {
  const safeRisks = risks || [];
  const safeIncidents = incidents || [];

  const averageRiskScore =
    safeRisks.length > 0
      ? (
          safeRisks.reduce(
            (sum, risk) => sum + Number(risk.risk_score || 0),
            0
          ) / safeRisks.length
        ).toFixed(1)
      : "0.0";

  const implementedControls = Number(
    isoCompliance?.implemented || 0
  );

  const openIncidents = safeIncidents.filter(
    (incident) =>
      String(incident.status || "").toLowerCase() === "open"
  ).length;

  return (
    <div className="executive-dashboard">

      <section className="executive-intro">
        <div>
          <div className="executive-kicker">
            DIRECTIVE CONTROL / ISO 31000
          </div>

          <h2>Dashboard de Control Directivo</h2>

          <p>
            Visualización ejecutiva de exposición al riesgo,
            incidentes, controles y conocimiento semántico.
          </p>
        </div>

        <div className="executive-status">
          <span className="status-dot" />
          RiskGuard Operational
        </div>
      </section>

      <section className="executive-stats-grid">

        <div className="executive-stat">
          <div className="executive-stat-label">TOTAL RIESGOS</div>
          <div className="executive-stat-value">
            {statistics.total}
          </div>
          <div className="executive-stat-description">
            Registered risks
          </div>
        </div>

        <div className="executive-stat critical">
          <div className="executive-stat-label">RIESGOS CRÍTICOS</div>
          <div className="executive-stat-value">
            {statistics.critical}
          </div>
          <div className="executive-stat-description">
            Immediate attention
          </div>
        </div>

        <div className="executive-stat high">
          <div className="executive-stat-label">RIESGOS HIGH</div>
          <div className="executive-stat-value">
            {statistics.high}
          </div>
          <div className="executive-stat-description">
            Requires control
          </div>
        </div>

        <div className="executive-stat incident">
          <div className="executive-stat-label">INCIDENTES</div>
          <div className="executive-stat-value">
            {statistics.incidents}
          </div>
          <div className="executive-stat-description">
            {openIncidents} open
          </div>
        </div>

        <div className="executive-stat control">
          <div className="executive-stat-label">CONTROLES IMPLEMENTADOS</div>
          <div className="executive-stat-value">
            {implementedControls}
          </div>
          <div className="executive-stat-description">
            ISO/IEC 27001:2022
          </div>
        </div>

        <div className="executive-stat average">
          <div className="executive-stat-label">RIESGO PROMEDIO</div>
          <div className="executive-stat-value">
            {averageRiskScore}
          </div>
          <div className="executive-stat-description">
            Score / 25
          </div>
        </div>

      </section>

      <section className="executive-main-grid">
        <RiskMatrix risks={safeRisks} />
        <ResidualRiskPanel risks={safeRisks} />
      </section>

      <section className="content-grid">

        <div className="panel risk-panel">

          <div className="panel-header">

            <div>
              <h2>Risk Register</h2>
              <p>Current occupational risk inventory</p>
            </div>

            <span className="count-badge">
              {safeRisks.length} risks
            </span>

          </div>

          <RiskTable
            risks={safeRisks}
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

      <section className="architecture-dashboard-panel">

        <div className="architecture-dashboard-title">
          Intelligent Semantic Architecture
        </div>

        <div className="architecture-dashboard-flow">

          <span>SQL</span>
          <b>→</b>

          <span>RDF</span>
          <b>→</b>

          <span>OWL</span>
          <b>→</b>

          <span>SPARQL</span>
          <b>→</b>

          <span>Reasoning</span>
          <b>→</b>

          <span>Multi-Agent</span>

        </div>

        <div className="architecture-dashboard-subtitle">
          Occupational Risk Management · Semantic Knowledge · Decision Intelligence
        </div>

      </section>

    </div>
  );
}
