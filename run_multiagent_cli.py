import json
import sys
from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS

# Namespaces Semánticos
RG = Namespace("http://riskguard.org/ontology#")

def load_knowledge_graph():
    """Carga el Grafo de Conocimiento unificado (TBox + ABox)."""
    g = Graph()
    g.parse("semantic/ontology.ttl", format="turtle")
    g.parse("data/riskguard.ttl", format="turtle")
    return g

def risk_agent(g, risk_code):
    """1. AGENTE DE ANÁLISIS DE RIESGO: Consulta SPARQL sobre la Ontología."""
    query = """
    PREFIX rg: <http://riskguard.org/ontology#>
    SELECT ?risk ?name ?score ?prob ?impact ?category WHERE {
        ?risk a rg:Risk ;
              rg:code ?code ;
              rg:name ?name ;
              rg:riskScore ?score ;
              rg:probability ?prob ;
              rg:impact ?impact ;
              rg:category ?category .
        FILTER(?code = "%s")
    }
    """ % risk_code
    
    results = list(g.query(query))
    if not results:
        return None
    
    row = results[0]
    score = int(row.score)
    
    # Inferencia semántica en memoria
    is_critical = score >= 17
    is_priority = score >= 20
    
    return {
        "risk_code": risk_code,
        "name": str(row.name),
        "score": score,
        "probability": int(row.prob),
        "impact": int(row.impact),
        "category": str(row.category),
        "inferred_classes": {
            "CriticalRisk": is_critical,
            "PriorityRisk": is_priority,
            "requiresPriorityAttention": is_priority
        }
    }

def control_agent(g, risk_code):
    """2. AGENTE DE CONTROL: Evalúa efectividad y brechas (Control Gap)."""
    query = """
    PREFIX rg: <http://riskguard.org/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?control ?label ?type ?effectiveness WHERE {
        ?risk rg:code "%s" ;
              rg:hasControl ?control .
        ?control rdfs:label ?label ;
                 rg:type ?type ;
                 rg:effectiveness ?effectiveness .
    }
    """ % risk_code
    
    results = list(g.query(query))
    controls = []
    
    for row in results:
        controls.append({
            "name": str(row.label),
            "type": str(row.type),
            "effectiveness": float(row.effectiveness)
        })
        
    # Evaluación de Brechas por Reglas Semánticas
    has_gap = len(controls) == 0 or all(c["type"] == "Administrative" for c in controls)
    
    return {
        "total_controls": len(controls),
        "controls": controls,
        "control_gap_detected": has_gap,
        "reason": "Solo existen controles administrativos de jerarquía baja." if has_gap else "Controles adecuados."
    }

def incident_agent(g, risk_code):
    """3. AGENTE DE INCIDENTES: Analiza eventos y severidades asociadas."""
    query = """
    PREFIX rg: <http://riskguard.org/ontology#>
    SELECT ?incident ?title ?severity ?status WHERE {
        ?risk rg:code "%s" ;
              rg:hasIncident ?incident .
        ?incident rg:title ?title ;
                  rg:severity ?severity ;
                  rg:status ?status .
    }
    """ % risk_code
    
    results = list(g.query(query))
    incidents = []
    
    for row in results:
        incidents.append({
            "title": str(row.title),
            "severity": str(row.severity),
            "status": str(row.status)
        })
        
    has_open_high = any(i["severity"] in ["High", "Critical"] and i["status"] == "Open" for i in incidents)
    
    return {
        "total_incidents": len(incidents),
        "incidents": incidents,
        "incident_gap_detected": has_open_high
    }

def coordinator_agent(risk_code="RISK-001"):
    """4. COORDINATOR AGENT: Orquesta los 3 agentes y emite la recomendación final."""
    print("\n" + "█" * 70)
    print(f"  EJECUCIÓN MULTI-AGENTE SEMÁNTICO - TARGET: {risk_code}")
    print("█" * 70 + "\n")
    
    g = load_knowledge_graph()
    
    # Invocación de Agentes
    risk_info = risk_agent(g, risk_code)
    if not risk_info:
        print(f"❌ Código de riesgo [{risk_code}] no encontrado en la Ontología.")
        return
        
    ctrl_info = control_agent(g, risk_code)
    inc_info = incident_agent(g, risk_code)
    
    # Síntesis de Decisión del CoordinatorAgent
    urgency = "URGENT" if (risk_info["inferred_classes"]["PriorityRisk"] or ctrl_info["control_gap_detected"]) else "NORMAL"
    
    recommendations = []
    if risk_info["inferred_classes"]["CriticalRisk"]:
        recommendations.append("Revisión inmediata por el comité de riesgos (ISO 31000).")
    if ctrl_info["control_gap_detected"]:
        recommendations.append("Elevar la jerarquía de controles: Implementar controles de Ingeniería o Cifrado ISO 27001 (A.8.5 / A.8.24).")
    if inc_info["incident_gap_detected"]:
        recommendations.append("Cerrar y auditar la causa raíz de los incidentes abiertos de alta severidad.")

    output = {
        "coordinator_status": "SUCCESS",
        "orchestrated_agents": ["RiskAnalysisAgent", "ControlAnalysisAgent", "IncidentAnalysisAgent"],
        "target_risk": risk_info,
        "control_assessment": ctrl_info,
        "incident_assessment": inc_info,
        "coordinated_decision": {
            "priority": urgency,
            "control_gap": ctrl_info["control_gap_detected"],
            "action_plan": recommendations
        }
    }
    
    print(json.dumps(output, indent=4, ensure_ascii=False))
    print("\n" + "=" * 70)
    print(" EJECUCIÓN MULTI-AGENTE FINALIZADA CON ÉXITO")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    code = sys.argv[1] if len(sys.argv) > 1 else "RISK-001"
    coordinator_agent(code)
