import RiskBadge from "../common/RiskBadge";

export default function RiskTable({
  risks,
  loading,
  selectedRisk,
  handleAnalyze
}) {
  if (loading) {
    return (
      <div className="loading-state">
        Loading risks...
      </div>
    );
  }

  if (risks.length === 0) {
    return (
      <div className="empty-state">
        No risks registered.
      </div>
    );
  }

  return (
    <div className="risk-table-wrapper">
      <table className="risk-table">
        <thead>
          <tr>
            <th>Code</th>
            <th>Risk</th>
            <th>Category</th>
            <th>Score</th>
            <th>Level</th>
            <th>Status</th>
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
                <div className="risk-name">
                  {risk.name}
                </div>

                {risk.description && (
                  <div className="risk-description">
                    {risk.description}
                  </div>
                )}
              </td>

              <td>
                {risk.category || "—"}
              </td>

              <td>
                <strong>{risk.risk_score}</strong>
              </td>

              <td>
                <RiskBadge level={risk.risk_level} />
              </td>

              <td>
                <span className="status-dot">
                  {risk.status || "Unknown"}
                </span>
              </td>

              <td>
                <button
                  className="analyze-button"
                  onClick={() => handleAnalyze(risk)}
                >
                  Analyze
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
