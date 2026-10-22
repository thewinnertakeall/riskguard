import StatCard from "../components/common/StatCard";
import RiskBadge from "../components/common/RiskBadge";

export default function IncidentsView({ incidents, statistics }) {
  return (
    <>
      <section className="stats-grid">

        <StatCard
          title="Total Incidents"
          value={statistics.incidents}
          icon="●"
          variant="incident"
          description="Registered incidents"
        />

        <StatCard
          title="Open"
          value={statistics.openIncidents}
          icon="!"
          variant="critical"
          description="Require attention"
        />

        <StatCard
          title="Closed"
          value={
            incidents.filter(
              (incident) =>
                String(incident.status || "").toLowerCase() ===
                "closed"
            ).length
          }
          icon="✓"
          description="Resolved incidents"
        />

      </section>

      <div className="panel">

        <div className="panel-header">

          <div>
            <h2>Incident Register</h2>
            <p>
              Incidents associated with occupational risks.
            </p>
          </div>

          <span className="count-badge">
            {incidents.length} incidents
          </span>

        </div>

        {incidents.length === 0 ? (
          <div className="empty-state">
            No incidents registered.
          </div>
        ) : (

          <div className="risk-table-wrapper">

            <table className="risk-table">

              <thead>
                <tr>
                  <th>Code</th>
                  <th>Incident</th>
                  <th>Type</th>
                  <th>Severity</th>
                  <th>Status</th>
                  <th>Date</th>
                </tr>
              </thead>

              <tbody>

                {incidents.map((incident, index) => (

                  <tr key={incident.id || incident.code || index}>

                    <td>
                      <strong>
                        {incident.code || incident.incident_code || "—"}
                      </strong>
                    </td>

                    <td>
                      <div className="risk-name">
                        {incident.name ||
                          incident.description ||
                          "Incident"}
                      </div>
                    </td>

                    <td>
                      {incident.type || incident.incident_type || "—"}
                    </td>

                    <td>
                      <RiskBadge
                        level={
                          incident.severity ||
                          incident.severity_level ||
                          "Unknown"
                        }
                      />
                    </td>

                    <td>
                      {incident.status || "—"}
                    </td>

                    <td>
                      {incident.date ||
                        incident.incident_date ||
                        "—"}
                    </td>

                  </tr>

                ))}

              </tbody>

            </table>

          </div>

        )}

      </div>
    </>
  );
}
