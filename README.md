# 🛡️ RiskGuard & RecMind: Sistema de Inferencia Semántica y Gestión de Riesgos

Sistema integral para la gestión de riesgos ocupacionales y tecnológicos basado en ontologías **OWL-DL/RDF**, consultas **SPARQL** y arquitectura **Multi-Agente** (ISO 31000 e ISO 27001).

---

## 🏛️ Arquitectura del Sistema
SQLite (SQL) -> ETL Pipeline -> Grafo RDF/OWL -> Razonador OWL-DL -> SPARQL -> Sistema Multi-Agente -> FastAPI -> React UI

---

## 🚀 Características Principales
- **Dominio Semántico Doble:** RiskGuard (ISO 31000/27001) y RecMind (Recomendación/Preferencia).
- **Sistema Multi-Agente:** RiskAnalysisAgent, ControlAnalysisAgent, IncidentAnalysisAgent y CoordinatorAgent.
- **Certificación E2E:** 100% verificado en Backend, CLI y Frontend.

---

## 🛠️ Ejecución del Sistema
1. **Ejecutar Agentes por Consola:**
   `./venv/bin/python3 run_multiagent_cli.py RISK-001`
2. **Iniciar Backend API:**
   `uvicorn app.main:app --reload --port 8000`
