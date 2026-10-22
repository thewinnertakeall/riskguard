export default function StatCard({
  title,
  value,
  icon,
  description,
  variant = ""
}) {
  return (
    <div className={`stat-card ${variant}`}>
      <div className="stat-icon">
        {icon}
      </div>

      <div className="stat-content">
        <span>{title}</span>
        <strong>{value}</strong>
        <small>{description}</small>
      </div>
    </div>
  );
}
