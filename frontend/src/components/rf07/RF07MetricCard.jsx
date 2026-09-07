function formatValue(value) {
  return Number(value || 0).toLocaleString("es-CO");
}

export default function RF07MetricCard({ label, value }) {
  return (
    <article className="rf07-metric-card">
      <span className="rf07-metric-label">
        {label}
      </span>

      <strong className="rf07-metric-value">
        {formatValue(value)}
      </strong>
    </article>
  );
}
