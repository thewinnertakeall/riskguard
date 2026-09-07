export default function KnowledgeCard({
  semantic,
  syncLoading,
  handleSemanticSync
}) {
  return (
    <div className="panel semantic-panel">
      <div className="panel-header">
        <div>
          <h2>Knowledge Graph</h2>
          <p>RDF / OWL semantic layer</p>
        </div>

        <span
          className={
            semantic?.success
              ? "connection-status online"
              : "connection-status offline"
          }
        >
          <span className="status-circle"></span>

          {semantic?.success
            ? "Available"
            : "Unavailable"}
        </span>
      </div>

      <div className="semantic-content">
        <div className="semantic-stat">
          <span className="semantic-label">
            RDF file
          </span>

          <strong>
            {semantic?.rdf_file || "—"}
          </strong>
        </div>

        <div className="semantic-stat">
          <span className="semantic-label">
            Triples
          </span>

          <strong>
            {semantic?.triples ?? 0}
          </strong>
        </div>

        <div className="semantic-actions">
          <button
            className="primary-button"
            onClick={handleSemanticSync}
            disabled={syncLoading}
          >
            {syncLoading
              ? "Synchronizing..."
              : "Synchronize SQL → RDF"}
          </button>
        </div>
      </div>
    </div>
  );
}
