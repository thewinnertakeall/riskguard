#!/usr/bin/env bash

set -e

PROJECT_ROOT="$HOME/projects/riskguard"
FRONTEND="$PROJECT_ROOT/frontend"
BACKUP="$PROJECT_ROOT/backups/s5_frontend"

echo "=============================================="
echo "RISKGUARD - S5 DASHBOARD SETUP"
echo "=============================================="

cd "$PROJECT_ROOT"

echo
echo "[1/9] Preparing frontend..."

mkdir -p "$BACKUP"

if [ -d "$FRONTEND" ]; then
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    echo "Existing frontend detected."
    echo "Creating backup: $BACKUP/frontend_$TIMESTAMP"

    cp -a "$FRONTEND" "$BACKUP/frontend_$TIMESTAMP"
fi

mkdir -p "$FRONTEND/src"

echo
echo "[2/9] Creating package.json..."

cat << 'PACKAGE_EOF' > "$FRONTEND/package.json"
{
  "name": "riskguard-dashboard",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.1",
    "vite": "^5.4.10"
  }
}
PACKAGE_EOF

echo
echo "[3/9] Creating Vite configuration..."

cat << 'VITE_EOF' > "$FRONTEND/vite.config.js"
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],

  server: {
    port: 5173,

    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true
      }
    }
  }
});
VITE_EOF

echo
echo "[4/9] Creating index.html..."

cat << 'HTML_EOF' > "$FRONTEND/index.html"
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />

    <meta
      name="viewport"
      content="width=device-width, initial-scale=1.0"
    />

    <meta
      name="description"
      content="RiskGuard Occupational Risk Management Dashboard"
    />

    <title>RiskGuard Dashboard</title>
  </head>

  <body>
    <div id="root"></div>

    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
HTML_EOF

echo
echo "[5/9] Creating React entry point..."

cat << 'MAIN_EOF' > "$FRONTEND/src/main.jsx"
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./styles.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
MAIN_EOF

echo
echo "[6/9] Creating API client..."

cat << 'API_EOF' > "$FRONTEND/src/api.js"
const API_BASE = "";

async function request(url, options = {}) {
  const response = await fetch(`${API_BASE}${url}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    },
    ...options
  });

  if (!response.ok) {
    const text = await response.text();

    throw new Error(
      `API ${response.status}: ${text || response.statusText}`
    );
  }

  return response.json();
}

export async function getRisks() {
  return request("/api/risks");
}

export async function getRiskDashboard() {
  return request("/api/v2/risks");
}

export async function analyzeRisk(riskCode) {
  return request(
    `/api/agents/analyze/${encodeURIComponent(riskCode)}`
  );
}

export async function getRecommendation(riskCode) {
  return request(
    `/api/agents/recommend/${encodeURIComponent(riskCode)}`
  );
}

export async function getSemanticStatus() {
  return request("/api/semantic/status");
}

export async function synchronizeSemanticGraph() {
  return request("/api/semantic/sync", {
    method: "POST"
  });
}

export async function getIncidents() {
  return request("/api/incidents");
}
API_EOF

echo
echo "[7/9] Creating dashboard application..."

cat << 'APP_EOF' > "$FRONTEND/src/App.jsx"
import { useEffect, useMemo, useState } from "react";

import {
  analyzeRisk,
  getIncidents,
  getRisks,
  getSemanticStatus,
  synchronizeSemanticGraph
} from "./api";

function App() {
  const [risks, setRisks] = useState([]);
  const [incidents, setIncidents] = useState([]);
  const [semantic, setSemantic] = useState(null);

  const [selectedRisk, setSelectedRisk] = useState(null);
  const [analysis, setAnalysis] = useState(null);

  const [loading, setLoading] = useState(true);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [syncLoading, setSyncLoading] = useState(false);

  const [error, setError] = useState("");

  async function loadDashboard() {
    try {
      setLoading(true);
      setError("");

      const [
        riskData,
        incidentData,
        semanticData
      ] = await Promise.all([
        getRisks(),
        getIncidents(),
        getSemanticStatus()
      ]);

      setRisks(Array.isArray(riskData) ? riskData : []);
      setIncidents(Array.isArray(incidentData) ? incidentData : []);
      setSemantic(semanticData);

      if (!selectedRisk && riskData.length > 0) {
        setSelectedRisk(riskData[0]);
      }
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleAnalyze(risk) {
    try {
      setSelectedRisk(risk);
      setAnalysisLoading(true);
      setError("");

      const result = await analyzeRisk(risk.code);

      setAnalysis(result);
    } catch (err) {
      console.error(err);
      setError(err.message);
      setAnalysis(null);
    } finally {
      setAnalysisLoading(false);
    }
  }

  async function handleSemanticSync() {
    try {
      setSyncLoading(true);
      setError("");

      await synchronizeSemanticGraph();

      const status = await getSemanticStatus();

      setSemantic(status);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setSyncLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  const statistics = useMemo(() => {
    const total = risks.length;

    const critical = risks.filter(
      (risk) => risk.risk_level === "Critical"
    ).length;

    const high = risks.filter(
      (risk) => risk.risk_level === "High"
    ).length;

    const medium = risks.filter(
      (risk) => risk.risk_level === "Medium"
    ).length;

    const low = risks.filter(
      (risk) => risk.risk_level === "Low"
    ).length;

    const openIncidents = incidents.filter(
      (incident) =>
        String(incident.status || "").toLowerCase() === "open"
    ).length;

    return {
      total,
      critical,
      high,
      medium,
      low,
      incidents: incidents.length,
      openIncidents
    };
  }, [risks, incidents]);

  return (
    <div className="app-shell">

      <aside className="sidebar">

        <div className="brand">
          <div className="brand-mark">R</div>

          <div>
            <div className="brand-name">RiskGuard</div>
            <div className="brand-subtitle">Safety Intelligence</div>
          </div>
        </div>

        <nav className="navigation">

          <button className="nav-item active">
            <span>▦</span>
            Dashboard
          </button>

          <button className="nav-item">
            <span>⚠</span>
            Risk Register
          </button>

          <button className="nav-item">
            <span>◉</span>
            Incidents
          </button>

          <button className="nav-item">
            <span>◆</span>
            Controls
          </button>

          <button className="nav-item">
            <span>◈</span>
            Knowledge Graph
          </button>

          <button className="nav-item">
            <span>◎</span>
            Multi-Agent
          </button>

        </nav>

        <div className="architecture-box">

          <div className="architecture-title">
            Intelligent Architecture
          </div>

          <div className="architecture-flow">
            <span>SQL</span>
            <b>→</b>
            <span>RDF</span>
            <b>→</b>
            <span>OWL</span>
          </div>

          <div className="architecture-flow">
            <span>SPARQL</span>
            <b>→</b>
            <span>Agents</span>
          </div>

        </div>

      </aside>

      <main className="main-content">

        <header className="topbar">

          <div>
            <div className="eyebrow">
              OCCUPATIONAL RISK MANAGEMENT
            </div>

            <h1>Risk Intelligence Dashboard</h1>

            <p>
              Semantic and multi-agent analysis of occupational risks.
            </p>
          </div>

          <div className="topbar-actions">

            <button
              className="secondary-button"
              onClick={loadDashboard}
              disabled={loading}
            >
              ↻ Refresh
            </button>

          </div>

        </header>

        {error && (
          <div className="error-banner">
            <strong>Connection error:</strong> {error}
          </div>
        )}

        <section className="stats-grid">

          <StatCard
            title="Total Risks"
            value={statistics.total}
            icon="◈"
            description="Registered risks"
          />

          <StatCard
            title="Critical"
            value={statistics.critical}
            icon="!"
            variant="critical"
            description="Immediate attention"
          />

          <StatCard
            title="High"
            value={statistics.high}
            icon="▲"
            variant="high"
            description="Requires control"
          />

          <StatCard
            title="Incidents"
            value={statistics.incidents}
            icon="●"
            variant="incident"
            description={`${statistics.openIncidents} open`}
          />

        </section>

        <section className="content-grid">

          <div className="panel risk-panel">

            <div className="panel-header">

              <div>
                <h2>Risk Register</h2>
                <p>Current occupational risk inventory</p>
              </div>

              <span className="count-badge">
                {risks.length} risks
              </span>

            </div>

            {loading ? (
              <div className="loading-state">
                Loading risks...
              </div>
            ) : risks.length === 0 ? (
              <div className="empty-state">
                No risks registered.
              </div>
            ) : (
              <div className="risk-table-wrapper">

                <table className="risk-table">

                  <thead>
                    <tr>
                      <th>Code</th>
                      <th>Risk</th>
                      <th>Category</th>
                      <th>Score</th>
                      <th>Level</th>
                      <th>Status</th>
                      <th></th>
                    </tr>
                  </thead>

                  <tbody>

                    {risks.map((risk) => (

                      <tr
                        key={risk.id || risk.code}
                        className={
                          selectedRisk?.code === risk.code
                            ? "selected-row"
                            : ""
                        }
                      >

                        <td>
                          <strong>{risk.code}</strong>
                        </td>

                        <td>
                          <div className="risk-name">
                            {risk.name}
                          </div>

                          {risk.description && (
                            <div className="risk-description">
                              {risk.description}
                            </div>
                          )}
                        </td>

                        <td>
                          {risk.category || "—"}
                        </td>

                        <td>
                          <strong>{risk.risk_score}</strong>
                        </td>

                        <td>
                          <RiskBadge level={risk.risk_level} />
                        </td>

                        <td>
                          <span className="status-dot">
                            {risk.status || "Unknown"}
                          </span>
                        </td>

                        <td>
                          <button
                            className="analyze-button"
                            onClick={() => handleAnalyze(risk)}
                          >
                            Analyze
                          </button>
                        </td>

                      </tr>

                    ))}

                  </tbody>

                </table>

              </div>
            )}

          </div>

          <div className="panel intelligence-panel">

            <div className="panel-header">

              <div>
                <h2>Selected Risk</h2>
                <p>Multi-agent intelligence</p>
              </div>

              {selectedRisk && (
                <RiskBadge level={selectedRisk.risk_level} />
              )}

            </div>

            {!selectedRisk ? (
              <div className="empty-state">
                Select a risk to begin analysis.
              </div>
            ) : (

              <div className="selected-risk">

                <div className="selected-risk-header">

                  <div>

                    <span className="risk-code">
                      {selectedRisk.code}
                    </span>

                    <h3>{selectedRisk.name}</h3>

                  </div>

                  <div className="score-display">

                    <span>Risk Score</span>

                    <strong>
                      {selectedRisk.risk_score}
                    </strong>

                    <small>/ 25</small>

                  </div>

                </div>

                <div className="risk-metrics">

                  <Metric
                    label="Probability"
                    value={`${selectedRisk.probability}/5`}
                  />

                  <Metric
                    label="Impact"
                    value={`${selectedRisk.impact}/5`}
                  />

                  <Metric
                    label="Category"
                    value={selectedRisk.category || "—"}
                  />

                </div>

                <button
                  className="primary-button full-width"
                  onClick={() => handleAnalyze(selectedRisk)}
                  disabled={analysisLoading}
                >
                  {analysisLoading
                    ? "Running agents..."
                    : "Run Multi-Agent Analysis"}
                </button>

                {analysis && (
                  <AgentResults analysis={analysis} />
                )}

              </div>

            )}

          </div>

        </section>

        <section className="bottom-grid">

          <div className="panel semantic-panel">

            <div className="panel-header">

              <div>
                <h2>Knowledge Graph</h2>
                <p>RDF / OWL semantic layer</p>
              </div>

              <span
                className={
                  semantic?.success
                    ? "connection-status online"
                    : "connection-status offline"
                }
              >
                <span className="status-circle"></span>
                {semantic?.success ? "Available" : "Unavailable"}
              </span>

            </div>

            <div className="semantic-content">

              <div className="semantic-stat">

                <span className="semantic-label">
                  RDF file
                </span>

                <strong>
                  {semantic?.rdf_file || "—"}
                </strong>

              </div>

              <div className="semantic-stat">

                <span className="semantic-label">
                  Triples
                </span>

                <strong>
                  {semantic?.triples ?? 0}
                </strong>

              </div>

              <div className="semantic-actions">

                <button
                  className="primary-button"
                  onClick={handleSemanticSync}
                  disabled={syncLoading}
                >
                  {syncLoading
                    ? "Synchronizing..."
                    : "Synchronize SQL → RDF"}
                </button>

              </div>

            </div>

          </div>

          <div className="panel architecture-panel">

            <div className="panel-header">

              <div>
                <h2>System Status</h2>
                <p>RiskGuard components</p>
              </div>

            </div>

            <div className="system-list">

              <SystemStatus
                name="FastAPI"
                status="Operational"
              />

              <SystemStatus
                name="SQLite"
                status="Operational"
              />

              <SystemStatus
                name="RDF / OWL"
                status={
                  semantic?.success
                    ? "Operational"
                    : "Unavailable"
                }
              />

              <SystemStatus
                name="Multi-Agent System"
                status="Operational"
              />

              <SystemStatus
                name="SPARQL"
                status="Operational"
              />

            </div>

          </div>

        </section>

        <footer className="footer">

          <span>
            RiskGuard v1.1.0
          </span>

          <span>
            SQL · RDF · OWL · SPARQL · Reasoning · Multi-Agent
          </span>

        </footer>

      </main>

    </div>
  );
}

function StatCard({
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

function RiskBadge({ level }) {
  const normalized = String(level || "Unknown").toLowerCase();

  return (
    <span className={`risk-badge ${normalized}`}>
      {level || "Unknown"}
    </span>
  );
}

function Metric({ label, value }) {
  return (
    <div className="metric">

      <span>{label}</span>

      <strong>{value}</strong>

    </div>
  );
}

function AgentResults({ analysis }) {
  const riskAnalysis = analysis?.risk_analysis || {};
  const controlAnalysis = analysis?.control_analysis || {};
  const incidentAnalysis = analysis?.incident_analysis || {};
  const recommendation = analysis?.recommendation || {};

  const risk = riskAnalysis.risk || {};

  return (
    <div className="agent-results">

      <div className="agent-title">
        <span className="agent-pulse"></span>
        Multi-Agent Analysis
      </div>

      <div className="agent-grid">

        <AgentCard
          name="Risk Analysis Agent"
          value={
            risk.risk_level ||
            riskAnalysis.risk_level ||
            riskAnalysis.level ||
            "Analyzed"
          }
        />

        <AgentCard
          name="Control Analysis Agent"
          value={
            controlAnalysis.control_status ||
            "Analyzed"
          }
        />

        <AgentCard
          name="Incident Analysis Agent"
          value={
            incidentAnalysis.incident_status ||
            "Analyzed"
          }
        />

        <AgentCard
          name="Recommendation Agent"
          value={
            recommendation.priority ||
            recommendation.recommendation_level ||
            "Generated"
          }
        />

      </div>

      {Array.isArray(recommendation.recommendations) &&
        recommendation.recommendations.length > 0 && (

          <div className="recommendations">

            <div className="recommendation-title">
              Recommended Actions
            </div>

            <ol>

              {recommendation.recommendations.map(
                (item, index) => (
                  <li key={index}>{item}</li>
                )
              )}

            </ol>

          </div>

        )}

    </div>
  );
}

function AgentCard({ name, value }) {
  return (
    <div className="agent-card">

      <span>{name}</span>

      <strong>{value}</strong>

    </div>
  );
}

function SystemStatus({ name, status }) {
  const operational =
    status === "Operational";

  return (
    <div className="system-item">

      <div className="system-name">

        <span
          className={
            operational
              ? "status-circle"
              : "status-circle offline"
          }
        ></span>

        {name}

      </div>

      <span
        className={
          operational
            ? "system-status operational"
            : "system-status"
        }
      >
        {status}
      </span>

    </div>
  );
}

export default App;
APP_EOF

echo
echo "[8/9] Creating dashboard styles..."

cat << 'CSS_EOF' > "$FRONTEND/src/styles.css"
:root {
  font-family:
    Inter,
    ui-sans-serif,
    system-ui,
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    sans-serif;

  color: #172033;
  background: #f5f7fb;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-width: 320px;
  min-height: 100vh;
  background: #f5f7fb;
}

button {
  font: inherit;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.app-shell {
  min-height: 100vh;
  display: flex;
}

/* Sidebar */

.sidebar {
  width: 260px;
  min-height: 100vh;
  padding: 26px 18px;
  background: #111827;
  color: white;
  display: flex;
  flex-direction: column;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 10px 28px;
}

.brand-mark {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: grid;
  place-items: center;
  background: #2563eb;
  font-size: 22px;
  font-weight: 800;
}

.brand-name {
  font-size: 18px;
  font-weight: 800;
}

.brand-subtitle {
  margin-top: 2px;
  font-size: 11px;
  color: #9ca3af;
}

.navigation {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.nav-item {
  border: 0;
  border-radius: 9px;
  padding: 12px 13px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: #cbd5e1;
  background: transparent;
  text-align: left;
  cursor: pointer;
}

.nav-item:hover {
  background: #1f2937;
  color: white;
}

.nav-item.active {
  background: #1d4ed8;
  color: white;
}

.nav-item span {
  width: 18px;
  text-align: center;
}

.architecture-box {
  margin-top: auto;
  padding: 15px;
  border: 1px solid #374151;
  border-radius: 12px;
  background: #172033;
}

.architecture-title {
  margin-bottom: 10px;
  font-size: 11px;
  font-weight: 700;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.architecture-flow {
  display: flex;
  align-items: center;
  gap: 7px;
  margin-top: 6px;
  font-size: 10px;
  color: #d1d5db;
}

.architecture-flow b {
  color: #60a5fa;
}

/* Main */

.main-content {
  flex: 1;
  min-width: 0;
  padding: 30px 34px;
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 28px;
}

.eyebrow {
  margin-bottom: 7px;
  color: #2563eb;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.12em;
}

.topbar h1 {
  margin: 0;
  font-size: 30px;
  letter-spacing: -0.04em;
}

.topbar p {
  margin: 7px 0 0;
  color: #64748b;
  font-size: 14px;
}

.topbar-actions {
  display: flex;
  gap: 10px;
}

.primary-button,
.secondary-button,
.analyze-button {
  border: 0;
  border-radius: 8px;
  padding: 10px 14px;
  font-weight: 700;
  cursor: pointer;
}

.primary-button {
  background: #2563eb;
  color: white;
}

.primary-button:hover {
  background: #1d4ed8;
}

.secondary-button {
  border: 1px solid #dbe2ea;
  background: white;
  color: #334155;
}

.secondary-button:hover {
  background: #f8fafc;
}

.full-width {
  width: 100%;
}

.error-banner {
  margin-bottom: 18px;
  padding: 13px 15px;
  border: 1px solid #fecaca;
  border-radius: 9px;
  background: #fef2f2;
  color: #991b1b;
  font-size: 13px;
}

/* Statistics */

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.stat-card {
  min-height: 112px;
  padding: 19px;
  display: flex;
  align-items: center;
  gap: 15px;
  border: 1px solid #e5eaf1;
  border-radius: 13px;
  background: white;
  box-shadow: 0 4px 14px rgba(15, 23, 42, 0.035);
}

.stat-icon {
  width: 45px;
  height: 45px;
  flex-shrink: 0;
  display: grid;
  place-items: center;
  border-radius: 11px;
  background: #eff6ff;
  color: #2563eb;
  font-weight: 800;
}

.stat-card.critical .stat-icon {
  background: #fef2f2;
  color: #dc2626;
}

.stat-card.high .stat-icon {
  background: #fff7ed;
  color: #ea580c;
}

.stat-card.incident .stat-icon {
  background: #fefce8;
  color: #ca8a04;
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-content span {
  color: #64748b;
  font-size: 12px;
}

.stat-content strong {
  margin-top: 2px;
  font-size: 27px;
  letter-spacing: -0.03em;
}

.stat-content small {
  margin-top: 3px;
  color: #94a3b8;
  font-size: 10px;
}

/* Panels */

.content-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.55fr) minmax(330px, 0.85fr);
  gap: 20px;
}

.bottom-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.55fr) minmax(300px, 0.85fr);
  gap: 20px;
  margin-top: 20px;
}

.panel {
  border: 1px solid #e5eaf1;
  border-radius: 13px;
  background: white;
  box-shadow: 0 4px 14px rgba(15, 23, 42, 0.035);
  overflow: hidden;
}

.panel-header {
  padding: 18px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 15px;
  border-bottom: 1px solid #edf0f4;
}

.panel-header h2 {
  margin: 0;
  font-size: 15px;
}

.panel-header p {
  margin: 4px 0 0;
  color: #94a3b8;
  font-size: 11px;
}

.count-badge {
  padding: 5px 9px;
  border-radius: 999px;
  background: #f1f5f9;
  color: #64748b;
  font-size: 10px;
  font-weight: 700;
}

/* Risk table */

.risk-table-wrapper {
  overflow-x: auto;
}

.risk-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 760px;
}

.risk-table th {
  padding: 11px 13px;
  background: #f8fafc;
  color: #64748b;
  font-size: 10px;
  text-align: left;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.risk-table td {
  padding: 13px;
  border-top: 1px solid #edf0f4;
  font-size: 12px;
  vertical-align: middle;
}

.risk-table tbody tr:hover {
  background: #fafcff;
}

.risk-table tbody tr.selected-row {
  background: #eff6ff;
}

.risk-name {
  font-weight: 700;
  color: #1e293b;
}

.risk-description {
  max-width: 250px;
  margin-top: 3px;
  overflow: hidden;
  color: #94a3b8;
  font-size: 10px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.risk-badge {
  display: inline-flex;
  padding: 5px 8px;
  border-radius: 999px;
  font-size: 10px;
  font-weight: 800;
}

.risk-badge.critical {
  background: #fee2e2;
  color: #b91c1c;
}

.risk-badge.high {
  background: #ffedd5;
  color: #c2410c;
}

.risk-badge.medium {
  background: #fef3c7;
  color: #a16207;
}

.risk-badge.low {
  background: #dcfce7;
  color: #15803d;
}

.risk-badge.unknown {
  background: #e2e8f0;
  color: #475569;
}

.status-dot {
  color: #64748b;
  font-size: 10px;
}

.analyze-button {
  padding: 6px 9px;
  background: #eff6ff;
  color: #2563eb;
  font-size: 10px;
}

.analyze-button:hover {
  background: #dbeafe;
}

/* Selected risk */

.selected-risk {
  padding: 20px;
}

.selected-risk-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 15px;
}

.risk-code {
  color: #2563eb;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.08em;
}

.selected-risk-header h3 {
  max-width: 300px;
  margin: 6px 0 0;
  font-size: 18px;
  line-height: 1.25;
}

.score-display {
  min-width: 72px;
  text-align: right;
}

.score-display span {
  display: block;
  color: #94a3b8;
  font-size: 9px;
}

.score-display strong {
  font-size: 30px;
}

.score-display small {
  color: #94a3b8;
}

.risk-metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin: 20px 0;
}

.metric {
  padding: 10px;
  border-radius: 8px;
  background: #f8fafc;
}

.metric span {
  display: block;
  color: #94a3b8;
  font-size: 9px;
}

.metric strong {
  display: block;
  margin-top: 3px;
  font-size: 12px;
}

/* Agents */

.agent-results {
  margin-top: 20px;
  padding-top: 17px;
  border-top: 1px solid #edf0f4;
}

.agent-title {
  display: flex;
  align-items: center;
  gap: 7px;
  margin-bottom: 10px;
  color: #334155;
  font-size: 11px;
  font-weight: 800;
}

.agent-pulse {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #2563eb;
}

.agent-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.agent-card {
  padding: 10px;
  border: 1px solid #e8edf3;
  border-radius: 8px;
}

.agent-card span {
  display: block;
  color: #94a3b8;
  font-size: 8px;
}

.agent-card strong {
  display: block;
  margin-top: 4px;
  color: #334155;
  font-size: 10px;
}

.recommendations {
  margin-top: 12px;
  padding: 12px;
  border-radius: 9px;
  background: #f8fafc;
}

.recommendation-title {
  font-size: 10px;
  font-weight: 800;
}

.recommendations ol {
  margin: 7px 0 0;
  padding-left: 20px;
  color: #64748b;
  font-size: 10px;
  line-height: 1.6;
}

/* Semantic */

.semantic-content {
  padding: 20px;
}

.semantic-stat {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  padding: 11px 0;
  border-bottom: 1px solid #edf0f4;
}

.semantic-label {
  color: #64748b;
  font-size: 11px;
}

.semantic-stat strong {
  max-width: 70%;
  overflow: hidden;
  color: #334155;
  font-size: 11px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.semantic-actions {
  margin-top: 15px;
}

.connection-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #64748b;
  font-size: 10px;
  font-weight: 700;
}

.connection-status.online {
  color: #15803d;
}

.status-circle {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #22c55e;
}

.status-circle.offline {
  background: #ef4444;
}

/* System */

.system-list {
  padding: 8px 20px 15px;
}

.system-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 11px 0;
  border-bottom: 1px solid #edf0f4;
}

.system-item:last-child {
  border-bottom: 0;
}

.system-name {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #334155;
  font-size: 11px;
}

.system-status {
  color: #94a3b8;
  font-size: 9px;
}

.system-status.operational {
  color: #15803d;
  font-weight: 700;
}

/* States */

.loading-state,
.empty-state {
  min-height: 180px;
  display: grid;
  place-items: center;
  color: #94a3b8;
  font-size: 12px;
}

/* Footer */

.footer {
  margin-top: 25px;
  padding: 16px 4px 5px;
  display: flex;
  justify-content: space-between;
  gap: 20px;
  color: #94a3b8;
  font-size: 10px;
}

/* Responsive */

@media (max-width: 1180px) {

  .sidebar {
    width: 220px;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .content-grid,
  .bottom-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 800px) {

  .app-shell {
    display: block;
  }

  .sidebar {
    width: 100%;
    min-height: auto;
    padding: 15px;
  }

  .navigation {
    flex-direction: row;
    overflow-x: auto;
  }

  .nav-item {
    white-space: nowrap;
  }

  .architecture-box {
    display: none;
  }

  .main-content {
    padding: 20px 15px;
  }

  .topbar {
    flex-direction: column;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .footer {
    flex-direction: column;
  }
}
CSS_EOF

echo
echo "[9/9] Installing dependencies..."

cd "$FRONTEND"

npm install

echo
echo "=============================================="
echo "S5 DASHBOARD CREATED"
echo "=============================================="

echo
echo "Frontend:"
echo "  $FRONTEND"

echo
echo "Backend:"
echo "  http://localhost:8000"

echo
echo "Dashboard:"
echo "  http://localhost:5173"

echo
echo "API proxy:"
echo "  /api -> http://localhost:8000"

echo
echo "Existing frontend backup:"
echo "  $BACKUP"

echo
echo "Database untouched:"
echo "  $PROJECT_ROOT/data/riskguard.db"

echo
echo "RDF untouched by setup:"
echo "  $PROJECT_ROOT/data/riskguard.ttl"

echo
echo "=============================================="
