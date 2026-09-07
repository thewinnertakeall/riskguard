#!/bin/bash

BASE="http://127.0.0.1:8000"
RISK="RISK-001"
ISO="A.5.15"

echo "=========================================="
echo "   TEST API REAL — RISK ↔ ISO 27001"
echo "=========================================="
echo

echo "1. GET inicial"
echo "------------------------------------------"

curl -s -i \
  "$BASE/api/v2/risks/$RISK/iso-controls"

echo
echo

echo "2. POST — crear relación"
echo "------------------------------------------"

curl -s -i \
  -X POST \
  "$BASE/api/v2/risks/$RISK/iso-controls" \
  -H "Content-Type: application/json" \
  -d '{
    "iso_control_code": "A.5.15",
    "treatment_status": "Planned",
    "notes": "Control asociado al riesgo eléctrico de mantenimiento"
  }'

echo
echo

echo "3. GET — verificar relación creada"
echo "------------------------------------------"

curl -s -i \
  "$BASE/api/v2/risks/$RISK/iso-controls"

echo
echo

echo "4. POST duplicado — debe devolver 409"
echo "------------------------------------------"

curl -s -i \
  -X POST \
  "$BASE/api/v2/risks/$RISK/iso-controls" \
  -H "Content-Type: application/json" \
  -d '{
    "iso_control_code": "A.5.15",
    "treatment_status": "Planned",
    "notes": "Prueba duplicada"
  }'

echo
echo

echo "5. DELETE — eliminar relación"
echo "------------------------------------------"

curl -s -i \
  -X DELETE \
  "$BASE/api/v2/risks/$RISK/iso-controls/$ISO"

echo
echo

echo "6. GET final — debe quedar vacío"
echo "------------------------------------------"

curl -s -i \
  "$BASE/api/v2/risks/$RISK/iso-controls"

echo
echo

echo "7. SQLite — verificar tabla"
echo "------------------------------------------"

sqlite3 data/riskguard.db <<'SQL'
.headers on
.mode column

SELECT
    id,
    risk_id,
    iso_control_id,
    treatment_status,
    notes,
    created_at
FROM risk_iso_controls;
SQL

echo
echo "=========================================="
echo "             TEST FINALIZADO"
echo "=========================================="
