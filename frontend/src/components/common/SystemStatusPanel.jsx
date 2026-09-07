import SystemStatus from "./SystemStatus";

export default function SystemStatusPanel({ semantic }) {
  return (
    <div className="panel architecture-panel">

      <div className="panel-header">

        <div>
          <h2>System Status</h2>
          <p>RiskGuard components</p>
        </div>

      </div>

      <div className="system-list">

        <SystemStatus
          name="FastAPI"
          status="Operational"
        />

        <SystemStatus
          name="SQLite"
          status="Operational"
        />

        <SystemStatus
          name="RDF / OWL"
          status={
            semantic?.success
              ? "Operational"
              : "Unavailable"
          }
        />

        <SystemStatus
          name="Multi-Agent System"
          status="Operational"
        />

        <SystemStatus
          name="SPARQL"
          status="Operational"
        />

      </div>

    </div>
  );
}
