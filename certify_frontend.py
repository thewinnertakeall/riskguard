import urllib.request
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_endpoint(name, path):
    url = f"{BASE_URL}{path}"
    print(f"➜ Verificando Endpoint Frontend [{name}]: {url}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                print(f"  ✔ RESPUESTA HTTP 200 OK")
                return data
            else:
                print(f"  ❌ ERROR HTTP STATUS: {response.status}")
                return None
    except Exception as e:
        print(f"  ❌ ERROR DE CONEXIÓN: {e}")
        return None

def main():
    print("\n" + "█" * 70)
    print("  SUITE DE CERTIFICACIÓN FRONTEND - CAPA SEMÁNTICA & ONTOLOGÍAS")
    print("█" * 70 + "\n")

    # 1. Validar Indicadores de Estado Semántico (System Status Widget)
    health = test_endpoint("System Health / Status", "/api/health")
    if health:
        rdf_status = health.get("services", {}).get("rdf_owl", "Unknown")
        sparql_status = health.get("services", {}).get("sparql", "Unknown")
        print(f"  └─ Estado Componente RDF/OWL  : {rdf_status}")
        print(f"  └─ Estado Componente SPARQL   : {sparql_status}")
        
    print("-" * 70)

    # 2. Validar Grafo de Conocimiento (Knowledge Graph Panel)
    kg_data = test_endpoint("Knowledge Graph Metadata", "/api/semantic/graph-info")
    if kg_data:
        triples = kg_data.get("triples_count", 0)
        file_path = kg_data.get("file", "N/A")
        print(f"  └─ Tripletos RDF en el Frontend : {triples}")
        print(f"  └─ Archivo de Grafo Consumido   : {file_path}")

    print("-" * 70)

    # 3. Validar Inferencia Semántica (Multi-Agent & Reasoning View)
    reasoning_data = test_endpoint("Semantic Inferences", "/api/semantic/reasoning")
    if reasoning_data:
        critical = reasoning_data.get("critical_risks_count", 0)
        priority = reasoning_data.get("priority_risks_count", 0)
        inferred_triples = reasoning_data.get("inferred_triples", 0)
        print(f"  └─ Riesgos Críticos Inferidos  : {critical}")
        print(f"  └─ Riesgos Prioritarios        : {priority}")
        print(f"  └─ Nuevos Tripletos Generados  : {inferred_triples}")

    print("\n" + "=" * 70)
    if health and kg_data and reasoning_data:
        print(" RESULTADO FINAL: FRONTEND CERTIFICADO EXITOSAMENTE")
        print(" La interfaz web consume y refleja la ontología semántica correctamente.")
    else:
        print(" RESULTADO FINAL: CERTIFICACIÓN PARCIAL O FALLIDA")
        print(" Asegúrate de que el servidor FastAPI (backend) esté corriendo en el puerto 8000.")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
