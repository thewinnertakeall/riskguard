import StatCard from "../common/StatCard";

export default function IncidentStats({ incidents = [], statistics }) {
  const closedIncidents = incidents.filter(
    (incident) =>
      String(incident.status || "").toLowerCase() === "closed"
  ).length;

  return (
    <section className="stats-grid">
      <StatCard
        label="Total Incidents"
        value={statistics?.incidents ?? incidents.length}
        icon="🚨"
      />

      <StatCard
        label="Open"
        value={statistics?.openIncidents ?? 0}
        icon="🟠"
      />

      <StatCard
        label="Closed"
        value={closedIncidents}
        icon="🟢"
      />
    </section>
  );
}
