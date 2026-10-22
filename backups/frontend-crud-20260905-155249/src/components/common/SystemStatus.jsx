export default function SystemStatus({ name, status }) {
  return (
    <div className="system-item">
      <span className="system-name">
        {name}
      </span>

      <span className="system-status">
        <span className="status-circle"></span>
        {status}
      </span>
    </div>
  );
}
