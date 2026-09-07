#!/usr/bin/env bash
set -euo pipefail

echo "=========================================="
echo "   RISKGUARD - REPARACION SEGURA"
echo "=========================================="

APP="src/App.jsx"

if [ ! -f "$APP" ]; then
    echo "ERROR: No existe $APP"
    exit 1
fi

echo
echo "[1/6] Creando backup..."
BACKUP="${APP}.backup-$(date +%Y%m%d-%H%M%S)"
cp "$APP" "$BACKUP"
echo "Backup creado:"
echo "  $BACKUP"

echo
echo "[2/6] Buscando DashboardView actual..."
grep -n -A15 -B3 '<DashboardView' "$APP" || true

echo
echo "[3/6] Aplicando reparacion..."

python3 <<'PY'
from pathlib import Path

p = Path("src/App.jsx")
s = p.read_text()

old = '''          <DashboardView
            risks={risks || []}
            incidents={incidents || []}
            semantic={semantic}
            statistics={statistics}
            selectedRisk={selectedRisk}
          />'''

new = '''          <DashboardView
            risks={risks || []}
            incidents={incidents || []}
            semantic={semantic}
            statistics={statistics}
            selectedRisk={selectedRisk}
            analysis={analysis}
            loading={loading}
            analysisLoading={analysisLoading}
            syncLoading={syncLoading}
            handleAnalyze={handleAnalyze}
            handleSemanticSync={handleSemanticSync}
          />'''

if old in s:
    p.write_text(s.replace(old, new, 1))
    print("OK: DashboardView reparado.")
elif "handleAnalyze={handleAnalyze}" in s and "handleSemanticSync={handleSemanticSync}" in s:
    print("OK: DashboardView ya estaba conectado.")
else:
    print("ADVERTENCIA: No se encontro exactamente el bloque esperado.")
    print("No se hizo una modificacion destructiva.")
    raise SystemExit(2)
PY

echo
echo "[4/6] Verificando imports y estructura..."

grep -n "DashboardView" "$APP" | head -5
grep -n "handleAnalyze" "$APP" | head -10
grep -n "handleSemanticSync" "$APP" | head -10

echo
echo "[5/6] Ejecutando build de produccion..."
npm run build

echo
echo "[6/6] RESULTADO"
echo "=========================================="

if [ -d dist ]; then
    echo "BUILD OK"
    echo
    echo "DashboardView:"
    grep -n -A15 '<DashboardView' "$APP" | head -20
    echo
    echo "Backup disponible:"
    echo "  $BACKUP"
    echo
    echo "=========================================="
    echo " REPARACION COMPLETADA SIN ERROR"
    echo "=========================================="
else
    echo "ERROR: No se genero dist/"
    echo
    echo "Restaurando backup..."
    cp "$BACKUP" "$APP"
    echo "App.jsx restaurado."
    exit 1
fi
