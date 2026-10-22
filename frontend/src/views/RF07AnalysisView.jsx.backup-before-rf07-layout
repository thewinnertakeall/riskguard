import { useRF07Analysis } from "../hooks/useRF07Analysis";

function MetricCard({ label, value }) {
  return (
    <div className="stat-card">
      <div className="stat-content">
        <span>{label}</span>
        <strong>{value}</strong>
      </div>
    </div>
  );
}

export default function RF07AnalysisView() {
  const {
    analysis,
    loading,
    error,
    loadAnalysis,
  } = useRF07Analysis();

  if (loading && !analysis) {
    return (
      <section>
        <h2>Public Risk Analysis</h2>
        <p>Cargando análisis RF-07...</p>
      </section>
    );
  }

  if (error && !analysis) {
    return (
      <section>
        <h2>Public Risk Analysis</h2>
        <p>{error}</p>

        <button onClick={() => loadAnalysis()}>
          Reintentar
        </button>
      </section>
    );
  }

  if (!analysis) {
    return null;
  }

  const { summary, indicators, municipalities, activities, trends } =
    analysis;

  return (
    <section>
      <div className="view-header">
        <div>
          <h2>Public Risk Analysis</h2>
          <p>
            Análisis de datos públicos de riesgos laborales — RF-07
          </p>
        </div>

        <button onClick={() => loadAnalysis()} disabled={loading}>
          {loading ? "Actualizando..." : "Actualizar"}
        </button>
      </div>

      <div className="stats-grid">
        <MetricCard
          label="Registros"
          value={summary.records}
        />

        <MetricCard
          label="Trabajadores"
          value={summary.total_workers}
        />

        <MetricCard
          label="Accidentes"
          value={summary.reported_accidents}
        />

        <MetricCard
          label="Muertes"
          value={summary.reported_work_deaths}
        />
      </div>

      <div className="stats-grid">
        <MetricCard
          label="Trabajadores dependientes"
          value={indicators.dependent_workers}
        />

        <MetricCard
          label="Trabajadores independientes"
          value={indicators.independent_workers}
        />

        <MetricCard
          label="Pensiones por accidente"
          value={indicators.disability_pension_accident}
        />

        <MetricCard
          label="Incapacidad parcial por accidente"
          value={indicators.permanent_partial_disability_accident}
        />
      </div>

      <div className="panel">
        <h3>Municipios</h3>

        <p>
          Municipios analizados: {municipalities.length}
        </p>

        {municipalities.slice(0, 10).map((item) => (
          <div
            key={item.municipality}
            className="analysis-row"
          >
            <span>{item.municipality}</span>
            <strong>
              {item.reported_accidents} accidentes
            </strong>
          </div>
        ))}
      </div>

      <div className="panel">
        <h3>Actividades económicas</h3>

        <p>
          Actividades analizadas: {activities.length}
        </p>

        {activities.slice(0, 10).map((item) => (
          <div
            key={item.economic_activity_code}
            className="analysis-row"
          >
            <span>{item.economic_activity_code}</span>
            <strong>
              {item.reported_accidents} accidentes
            </strong>
          </div>
        ))}
      </div>

      <div className="panel">
        <h3>Períodos</h3>

        <p>
          Períodos disponibles: {trends.length}
        </p>

        {trends.map((item) => (
          <div
            key={`${item.report_year}-${item.report_month}`}
            className="analysis-row"
          >
            <span>
              {item.report_year}-{String(item.report_month).padStart(2, "0")}
            </span>
            <strong>
              {item.reported_accidents} accidentes
            </strong>
          </div>
        ))}
      </div>
    </section>
  );
}
