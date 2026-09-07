export default function StatCard({
  title,
  label,
  value,
  icon,
  description,
  variant = ""
}) {
  const displayTitle = title ?? label ?? "";

  return (
    <div className={`stat-card ${variant}`}>
      <div className="stat-icon">
        {icon}
      </div>

      <div className="stat-content">
        <span>{displayTitle}</span>
        <strong>{value}</strong>
        {description && <small>{description}</small>}
      </div>
    </div>
  );
}
