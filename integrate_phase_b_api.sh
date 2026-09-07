#!/usr/bin/env bash

set -e

echo "=============================================="
echo "RISKGUARD - PHASE B API INTEGRATION"
echo "Controller -> Use Case -> Service -> Repository"
echo "=============================================="

python - << 'PY'
from pathlib import Path

path = Path("app/main.py")
text = path.read_text()

imports = """
# ============================================================
# PHASE B - OOP ARCHITECTURE API
# ============================================================

from presentation.api.routes.risk_routes import router as risk_v2_router
"""

if "risk_v2_router" not in text:
    text = imports + "\n" + text

include_router = """
# Phase B modular risk API
app.include_router(risk_v2_router)
"""

if "app.include_router(risk_v2_router)" not in text:
    text += "\n" + include_router + "\n"

path.write_text(text)

print("FastAPI Phase B router integrated.")
PY

echo
echo "Checking compilation..."

python -m compileall \
    app \
    domain \
    application \
    infrastructure \
    presentation

echo
echo "=============================================="
echo "PHASE B API INTEGRATION COMPLETED"
echo "=============================================="
echo
echo "New endpoints:"
echo "  GET /api/v2/risks"
echo "  GET /api/v2/risks/{risk_code}"
echo
echo "Legacy endpoints remain available:"
echo "  GET /api/risks"
echo "  GET /api/risks/{risk_id}"
echo
