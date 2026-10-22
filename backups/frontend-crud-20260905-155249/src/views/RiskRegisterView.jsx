import StatCard from "../components/common/StatCard";
import RiskTable from "../components/risk/RiskTable";

export default function RiskRegisterView({
  risks,
  loading,
  selectedRisk,
  handleAnalyze,
  statistics
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
          title="Low / Medium"
          value={statistics.low + statistics.medium}
          icon="●"
          description="Lower priority risks"
        />

      </section>

      <div className="panel">

        <div className="panel-header">

          <div>
            <h2>Complete Risk Register</h2>
            <p>
              Occupational risks currently registered in RiskGuard.
            </p>
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
    </>
  );
}
