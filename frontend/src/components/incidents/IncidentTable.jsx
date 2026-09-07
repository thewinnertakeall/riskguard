export default function IncidentTable({
  incidents = [],
  onEdit,
  onDelete,
  deletingId = null
}) {
  const getSeverityClass = (severity) => {
    const value = String(severity || "").toLowerCase();

    if (value === "critical") return "severity-badge severity-critical";
    if (value === "high") return "severity-badge severity-high";
    if (value === "medium") return "severity-badge severity-medium";
    if (value === "low") return "severity-badge severity-low";

    return "severity-badge severity-unknown";
  };

  const getStatusClass = (status) => {
    const value = String(status || "").toLowerCase();

    if (value === "closed") {
      return "status-badge status-closed";
    }

    if (
      value === "in progress" ||
      value === "in_progress"
    ) {
      return "status-badge status-in-progress";
    }

    return "status-badge status-open";
  };

  return (
    <div className="panel">
      <div className="panel-header">
        Incident Register
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
                <th>Title</th>
                <th>Date</th>
                <th>Type</th>
                <th>Severity</th>
                <th>Status</th>
                <th>Location</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>
              {incidents.map((incident) => {
                const severity =
                  incident.severity || "Unknown";

                const status =
                  incident.status || "Open";

                return (
                  <tr key={incident.id}>
                    <td>{incident.code}</td>

                    <td>
                      <div className="risk-name">
                        {incident.title ||
                          incident.name ||
                          incident.description ||
                          "Incident"}
                      </div>
                    </td>

                    <td>
                      {incident.incident_date || "—"}
                    </td>

                    <td>
                      {incident.incident_type || "—"}
                    </td>

                    <td>
                      <span className={getSeverityClass(severity)}>
                        {severity}
                      </span>
                    </td>

                    <td>
                      <span className={getStatusClass(status)}>
                        {status}
                      </span>
                    </td>

                    <td>
                      {incident.location_id ?? "—"}
                    </td>

                    <td>
                      <div className="table-actions">
                        <button
                          type="button"
                          className="secondary-button small-button"
                          onClick={() => onEdit(incident)}
                          disabled={deletingId === incident.id}
                        >
                          Edit
                        </button>

                        <button
                          type="button"
                          className="danger-button small-button"
                          onClick={() => onDelete(incident)}
                          disabled={deletingId === incident.id}
                        >
                          {deletingId === incident.id
                            ? "Deleting..."
                            : "Delete"}
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
