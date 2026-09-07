#!/usr/bin/env bash

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EVIDENCE="$ROOT/evidence"

RF="${1:-}"

if [ -z "$RF" ]; then
    echo "Uso:"
    echo
    echo "  ./riskguard_rf.sh RF-01"
    echo "  ./riskguard_rf.sh RF-02"
    echo "  ./riskguard_rf.sh RF-03"
    echo "  ..."
    echo "  ./riskguard_rf.sh RF-18"
    exit 1
fi

mkdir -p "$EVIDENCE/$RF"

TIMESTAMP="$(date '+%Y%m%d_%H%M%S')"
REPORT="$EVIDENCE/$RF/audit_$TIMESTAMP.txt"

exec > >(tee "$REPORT") 2>&1

echo "============================================================"
echo "                 RISKGUARD - $RF"
echo "                 DIVIDE Y VENCERAS"
echo "============================================================"
echo
echo "Fecha: $(date)"
echo "Proyecto: $ROOT"
echo "Evidencia: $REPORT"
echo

cd "$ROOT"

case "$RF" in

RF-01)
    echo "RF-01 - GESTION DE RIESGOS"
    echo

    echo "=== ENDPOINTS ==="
    grep -nE '@app\.(get|post|put|patch|delete).*risks' app/main.py || true

    echo
    echo "=== CRUD ==="
    grep -nE '^def (create|get_risks|get_risk|update_risk|delete_risk)' \
        app/crud.py || true

    echo
    echo "=== FRONTEND ==="
    find frontend/src -type f \
        | grep -Ei 'risk|Risk' \
        | sort

    echo
    echo "=== SQLITE ==="
    sqlite3 data/riskguard.db \
        "SELECT COUNT(*) AS risks FROM risks;"

    ;;

RF-02)
    echo "RF-02 - VALORACION DE RIESGOS"
    echo

    grep -RniE \
        'probability|probabilidad|impact|impacto|score|nivel|level' \
        app frontend/src semantic \
        --exclude-dir=node_modules \
        --exclude-dir=__pycache__ \
        --exclude='*.backup*' \
        | head -n 150 || true

    ;;

RF-03)
    echo "RF-03 - CAUSAS"
    echo

    echo "=== BACKEND ==="
    grep -nE \
        '@app\.(get|post|put|patch|delete).*causes' \
        app/main.py || true

    echo
    echo "=== CRUD ==="
    grep -nE \
        '^def (create_cause|get_causes|get_cause|update_cause|delete_cause)' \
        app/crud.py || true

    echo
    echo "=== RELACIONES ==="
    grep -RniE \
        'cause.*risk|risk.*cause' \
        app semantic \
        --exclude-dir=__pycache__ \
        --exclude='*.backup*' \
        | head -n 100 || true

    ;;

RF-04)
    echo "RF-04 - CONTROLES"
    echo

    echo "=== ENDPOINTS ==="
    grep -nE \
        '@app\.(get|post|put|patch|delete).*controls' \
        app/main.py || true

    echo
    echo "=== CRUD ==="
    grep -nE \
        '^def (create_control|get_controls|get_control|update_control|delete_control)' \
        app/crud.py || true

    echo
    echo "=== SQLITE ==="
    sqlite3 data/riskguard.db \
        "SELECT COUNT(*) AS controls FROM controls;"

    echo
    echo "=== RELACION RISK-CONTROL ==="
    grep -RniE \
        'risk.*control|control.*risk|risk_controls|risk_control' \
        app semantic \
        --exclude-dir=__pycache__ \
        --exclude='*.backup*' \
        | head -n 120 || true

    ;;

RF-05)
    echo "RF-05 - INCIDENTES"
    echo

    echo "=== ENDPOINTS ==="
    grep -nE \
        '@app\.(get|post|put|patch|delete).*incidents' \
        app/main.py || true

    echo
    echo "=== CRUD ==="
    grep -nE \
        '^def (create_incident|get_incidents|get_incident|update_incident|delete_incident)' \
        app/crud.py || true

    echo
    echo "=== SQLITE ==="
    sqlite3 -header -column data/riskguard.db \
        "SELECT id,code,title,incident_date,incident_type,severity,location_id,status FROM incidents ORDER BY id;"

    echo
    echo "=== RELACION RISK-INCIDENT ==="
    sqlite3 -header -column data/riskguard.db \
        "SELECT * FROM risk_incidents;" 2>/dev/null || true

    echo
    echo "=== FRONTEND ==="
    find frontend/src \
        -type f \
        -iname '*incident*' \
        | sort

    ;;

RF-06)
    echo "RF-06 - ETL DATOS PUBLICOS"
    echo

    find . \
        -type f \
        \( -iname '*etl*' \
        -o -iname '*dataset*' \
        -o -iname '*public*' \
        -o -iname '*.csv' \) \
        -not -path './frontend/node_modules/*' \
        -not -path './venv/*' \
        | sort

    ;;

RF-07)
    echo "RF-07 - ANALISIS DATOS PUBLICOS"
    echo

    grep -RniE \
        'analytics|analysis|estadistica|statistics|dataset|public' \
        app semantic agents frontend/src \
        --exclude-dir=node_modules \
        --exclude-dir=__pycache__ \
        --exclude='*.backup*' \
        | head -n 150 || true

    ;;

RF-08)
    echo "RF-08 - RDF"
    echo

    if [ -f data/riskguard.ttl ]; then
        echo "[OK] data/riskguard.ttl"
        wc -l data/riskguard.ttl
        echo
        head -n 100 data/riskguard.ttl
    else
        echo "[MISSING] data/riskguard.ttl"
    fi

    ;;

RF-09)
    echo "RF-09 - OWL / ONTOLOGIA"
    echo

    if [ -f semantic/ontology.ttl ]; then
        echo "[OK] semantic/ontology.ttl"
        wc -l semantic/ontology.ttl
        echo
        head -n 180 semantic/ontology.ttl
    else
        echo "[MISSING] semantic/ontology.ttl"
    fi

    ;;

RF-10)
    echo "RF-10 - SPARQL"
    echo

    if [ -f semantic/sparql.py ]; then
        echo "[OK] semantic/sparql.py"
        grep -nE \
            'SELECT|ASK|CONSTRUCT|DESCRIBE|query|sparql' \
            semantic/sparql.py \
            | head -n 150
    else
        echo "[MISSING] semantic/sparql.py"
    fi

    ;;

RF-11)
    echo "RF-11 - REASONING"
    echo

    if [ -f semantic/reasoner.py ]; then
        echo "[OK] semantic/reasoner.py"
        sed -n '1,250p' semantic/reasoner.py
    else
        echo "[MISSING] semantic/reasoner.py"
    fi

    ;;

RF-12)
    echo "RF-12 - RISK ANALYSIS AGENT"
    echo

    if [ -f agents/risk_analysis_agent.py ]; then
        echo "[OK] agents/risk_analysis_agent.py"
        sed -n '1,260p' agents/risk_analysis_agent.py
    else
        echo "[MISSING] agents/risk_analysis_agent.py"
    fi

    ;;

RF-13)
    echo "RF-13 - CONTROL ANALYSIS AGENT"
    echo

    if [ -f agents/control_analysis_agent.py ]; then
        echo "[OK] agents/control_analysis_agent.py"
        sed -n '1,260p' agents/control_analysis_agent.py
    else
        echo "[MISSING] agents/control_analysis_agent.py"
    fi

    ;;

RF-14)
    echo "RF-14 - INCIDENT ANALYSIS AGENT"
    echo

    if [ -f agents/incident_analysis_agent.py ]; then
        echo "[OK] agents/incident_analysis_agent.py"
        sed -n '1,260p' agents/incident_analysis_agent.py
    else
        echo "[MISSING] agents/incident_analysis_agent.py"
    fi

    ;;

RF-15)
    echo "RF-15 - RECOMMENDATION AGENT"
    echo

    if [ -f agents/recommendation_agent.py ]; then
        echo "[OK] agents/recommendation_agent.py"
        sed -n '1,300p' agents/recommendation_agent.py
    else
        echo "[MISSING] agents/recommendation_agent.py"
    fi

    ;;

RF-16)
    echo "RF-16 - COORDINATOR / COOPERACION"
    echo

    if [ -f agents/coordinator_agent.py ]; then
        echo "[OK] agents/coordinator_agent.py"
        sed -n '1,300p' agents/coordinator_agent.py
    else
        echo "[MISSING] agents/coordinator_agent.py"
    fi

    ;;

RF-17)
    echo "RF-17 - DASHBOARD"
    echo

    find frontend/src \
        -maxdepth 3 \
        -type f \
        | sort

    echo
    echo "=== APP ==="
    grep -nE \
        'Dashboard|Incidents|Controls|Knowledge|Risk' \
        frontend/src/App.jsx \
        | head -n 100 || true

    ;;

RF-18)
    echo "RF-18 - INTEGRACION"
    echo

    grep -RniE \
        'semantic|sparql|rdf|ontology|agent|recommend|sync|etl' \
        app agents semantic frontend/src \
        --exclude-dir=node_modules \
        --exclude-dir=__pycache__ \
        --exclude='*.backup*' \
        | head -n 200 || true

    ;;

*)
    echo "[ERROR] RF no reconocido: $RF"
    exit 1
    ;;

esac

echo
echo "============================================================"
echo " FIN $RF"
echo "============================================================"
echo
echo "EVIDENCIA:"
echo "$REPORT"
echo
echo "IMPORTANTE: este script NO modifica codigo."
echo
