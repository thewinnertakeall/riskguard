export default function RF07Header({
  loading,
  onRefresh,
}) {
  return (
    <header className="rf07-header">
      <div>
        <span className="rf07-kicker">
          OCCUPATIONAL RISK MANAGEMENT
        </span>

        <h2>Public Risk Analysis</h2>

        <p>
          Análisis de datos públicos de riesgos laborales — RF-07
        </p>
      </div>

      <button
        className="rf07-refresh"
        onClick={onRefresh}
        disabled={loading}
      >
        {loading ? "Actualizando..." : "↻ Actualizar"}
      </button>
    </header>
  );
}
