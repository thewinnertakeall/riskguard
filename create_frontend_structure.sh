#!/usr/bin/env bash

set -e

BASE="frontend/src"

echo "📁 Creando estructura modular de RiskGuard..."

mkdir -p \
  "$BASE/api" \
  "$BASE/components/layout" \
  "$BASE/components/common" \
  "$BASE/components/evidence" \
  "$BASE/views" \
  "$BASE/hooks"

# Archivos API
touch \
  "$BASE/api/index.js" \
  "$BASE/api/risks.js" \
  "$BASE/api/incidents.js" \
  "$BASE/api/iso27001.js" \
  "$BASE/api/evidence.js"

# Layout
touch \
  "$BASE/components/layout/Sidebar.jsx" \
  "$BASE/components/layout/Topbar.jsx" \
  "$BASE/components/layout/Footer.jsx"

# Componentes comunes
touch \
  "$BASE/components/common/StatCard.jsx" \
  "$BASE/components/common/StatusBadge.jsx" \
  "$BASE/components/common/LoadingState.jsx"

# Evidence
touch \
  "$BASE/components/evidence/EvidenceTable.jsx" \
  "$BASE/components/evidence/EvidenceForm.jsx" \
  "$BASE/components/evidence/EvidenceView.jsx"

# Views
touch \
  "$BASE/views/DashboardView.jsx" \
  "$BASE/views/RiskRegisterView.jsx" \
  "$BASE/views/IncidentsView.jsx" \
  "$BASE/views/ControlsView.jsx" \
  "$BASE/views/ISO27001View.jsx" \
  "$BASE/views/EvidenceView.jsx" \
  "$BASE/views/KnowledgeView.jsx" \
  "$BASE/views/MultiAgentView.jsx"

# Hooks
touch \
  "$BASE/hooks/useRisks.js" \
  "$BASE/hooks/useISO27001.js" \
  "$BASE/hooks/useEvidence.js"

echo ""
echo "✅ Estructura creada."
echo ""

find "$BASE" -maxdepth 4 -type f | sort

echo ""
echo "⚠️ No se modificaron App.jsx, api.js ni styles.css."
