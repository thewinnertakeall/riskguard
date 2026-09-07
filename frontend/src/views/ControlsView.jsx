import StatCard from "../components/common/StatCard";
import AgentResults from "../components/agents/AgentResults";

export default function ControlsView({
  risks,
  selectedRisk,
  analysis,
  handleAnalyze,
  analysisLoading
}) {
  const controls = [];

  risks.forEach((risk) => {
    const riskControls =
      risk.controls ||
      risk.risk_controls ||
      [];

    if (Array.isArray(riskControls)) {
      riskControls.forEach((control) => {
        controls.push({
          ...control,
          risk_code: risk.code
        });
      });
    }
  });

  const controlAnalysis = analysis?.control_analysis || {};

  return (
    <>
      <section className="stats-grid">

        <StatCard
          title="Risks"
          value={risks.length}
          icon="◈"
          description="With registered controls"
        />

        <StatCard
          title="Controls"
          value={controls.length || "—"}
          icon="◆"
          description="Available control records"
        />

        <StatCard
          title="Effectiveness"
          value={
            controlAnalysis.average_effectiveness != null
              ? `${controlAnalysis.average_effectiveness}%`
              : "—"
          }
          icon="✓"
          description="Latest analysis"
        />

        <StatCard
          title="Control Gap"
          value={
            controlAnalysis.control_gap
              ? "YES"
              : "—"
          }
          icon="!"
          variant={
            controlAnalysis.control_gap
              ? "critical"
              : ""
          }
          description="Multi-agent assessment"
        />

      </section>

      <div className="panel">

        <div className="panel-header">

          <div>
            <h2>Control Management</h2>
            <p>
              Controls used to reduce identified occupational risks.
            </p>
          </div>

        </div>

        {controls.length > 0 ? (

          <div className="risk-table-wrapper">

            <table className="risk-table">

              <thead>
                <tr>
                  <th>Risk</th>
                  <th>Control</th>
                  <th>Type</th>
                  <th>Hierarchy</th>
                  <th>Effectiveness</th>
                </tr>
              </thead>

              <tbody>

                {controls.map((control, index) => (

                  <tr key={control.id || index}>

                    <td>
                      <strong>{control.risk_code}</strong>
                    </td>

                    <td>
                      {control.name ||
                        control.description ||
                        "Control"}
                    </td>

                    <td>
                      {control.type || "—"}
                    </td>

                    <td>
                      {control.hierarchy ||
                        control.hierarchy_level ||
                        "—"}
                    </td>

                    <td>
                      {control.effectiveness != null
                        ? `${control.effectiveness}%`
                        : "—"}
                    </td>

                  </tr>

                ))}

              </tbody>

            </table>

          </div>

        ) : (

          <div className="control-analysis">

            <h3>Control intelligence</h3>

            <p>
              Select a risk and run the multi-agent analysis
              to inspect its controls and effectiveness.
            </p>

            {selectedRisk && (
              <button
                className="primary-button"
                onClick={() => handleAnalyze(selectedRisk)}
                disabled={analysisLoading}
              >
                {analysisLoading
                  ? "Analyzing..."
                  : `Analyze ${selectedRisk.code}`}
              </button>
            )}

            {controlAnalysis.control_status && (
              <AgentResults analysis={analysis} />
            )}

          </div>

        )}

      </div>
    </>
  );
}
