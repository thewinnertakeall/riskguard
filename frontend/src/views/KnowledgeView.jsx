import StatCard from "../components/common/StatCard";
import KnowledgeCard from "../components/knowledge/KnowledgeCard";

export default function KnowledgeView({
  semantic,
  syncLoading,
  handleSemanticSync
}) {
  return (
    <>
      <section className="stats-grid">

        <StatCard
          title="RDF / OWL"
          value={
            semantic?.success
              ? "ONLINE"
              : "OFFLINE"
          }
          icon="◈"
          description="Semantic layer"
        />

        <StatCard
          title="Triples"
          value={semantic?.triples ?? 0}
          icon="◆"
          description="Knowledge graph"
        />

        <StatCard
          title="Source"
          value="SQLite"
          icon="▣"
          description="Operational database"
        />

        <StatCard
          title="SPARQL"
          value="READY"
          icon="◎"
          description="Semantic querying"
        />

      </section>

      <KnowledgeCard
        semantic={semantic}
        syncLoading={syncLoading}
        handleSemanticSync={handleSemanticSync}
      />

      <div className="panel">

        <div className="panel-header">

          <div>
            <h2>Semantic Architecture</h2>
            <p>
              Data flow between the relational and semantic layers.
            </p>
          </div>

        </div>

        <div className="semantic-content">

          <div className="semantic-stat">
            <span className="semantic-label">
              SQL
            </span>

            <strong>
              RiskGuard SQLite
            </strong>
          </div>

          <div className="semantic-stat">
            <span className="semantic-label">
              RDF
            </span>

            <strong>
              {semantic?.rdf_file || "riskguard.ttl"}
            </strong>
          </div>

          <div className="semantic-stat">
            <span className="semantic-label">
              OWL
            </span>

            <strong>
              RiskGuard Ontology
            </strong>
          </div>

          <div className="semantic-stat">
            <span className="semantic-label">
              SPARQL
            </span>

            <strong>
              Semantic Query Layer
            </strong>
          </div>

        </div>

      </div>
    </>
  );
}
