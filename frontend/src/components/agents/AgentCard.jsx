export default function AgentCard({ name, value }) {
  return (
    <div className="agent-card">
      <span className="agent-card-name">
        {name}
      </span>

      <strong>
        {value}
      </strong>
    </div>
  );
}
