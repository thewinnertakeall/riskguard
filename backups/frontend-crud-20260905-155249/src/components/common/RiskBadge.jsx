export default function RiskBadge({ level }) {
  const normalized = String(level || "Unknown").toLowerCase();

  return (
    <span className={`risk-badge ${normalized}`}>
      {level || "Unknown"}
    </span>
  );
}
