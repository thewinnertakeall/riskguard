import sys
from pathlib import Path

from rdflib import Graph


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# FILES
# ============================================================

RDF_FILE = PROJECT_ROOT / "data" / "riskguard.ttl"
ONTOLOGY_FILE = PROJECT_ROOT / "semantic" / "ontology.ttl"


# ============================================================
# NAMESPACE
# ============================================================

PREFIXES = """
PREFIX rg: <http://riskguard.org/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""


# ============================================================
# LOAD SEMANTIC GRAPH
# ============================================================

def load_graph():

    graph = Graph()

    graph.parse(
        str(ONTOLOGY_FILE),
        format="turtle"
    )

    graph.parse(
        str(RDF_FILE),
        format="turtle"
    )

    return graph


# ============================================================
# QUERY 1 - ALL RISKS
# ============================================================

def query_all_risks(graph):

    query = PREFIXES + """
    SELECT ?risk ?code ?name ?score ?level
    WHERE {
        ?risk a rg:Risk .
        ?risk rg:code ?code .
        ?risk rg:name ?name .
        ?risk rg:riskScore ?score .
        ?risk rg:riskLevel ?level .
    }
    ORDER BY DESC(?score)
    """

    return graph.query(query)


# ============================================================
# QUERY 2 - CRITICAL RISKS
# ============================================================

def query_critical_risks(graph):

    query = PREFIXES + """
    SELECT ?risk ?code ?name ?score
    WHERE {
        ?risk a rg:Risk .
        ?risk rg:code ?code .
        ?risk rg:name ?name .
        ?risk rg:riskScore ?score .

        FILTER(?score >= 17)
    }
    ORDER BY DESC(?score)
    """

    return graph.query(query)


# ============================================================
# QUERY 3 - RISK RELATIONSHIPS
# ============================================================

def query_risk_relationships(graph):

    query = PREFIXES + """
    SELECT ?riskCode ?riskName
           ?causeName
           ?controlName
           ?incidentTitle
    WHERE {

        ?risk a rg:Risk .
        ?risk rg:code ?riskCode .
        ?risk rg:name ?riskName .

        OPTIONAL {
            ?risk rg:hasCause ?cause .
            ?cause rg:name ?causeName .
        }

        OPTIONAL {
            ?risk rg:hasControl ?control .
            ?control rg:name ?controlName .
        }

        OPTIONAL {
            ?risk rg:hasIncident ?incident .
            ?incident rg:title ?incidentTitle .
        }
    }
    """

    return graph.query(query)


# ============================================================
# DISPLAY
# ============================================================

def print_results(title, results):

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)

    count = 0

    for row in results:

        count += 1

        values = [
            str(value)
            for value in row
        ]

        print(" | ".join(values))

    print()
    print(f"Results: {count}")


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("RISKGUARD SPARQL ENGINE")
    print("=" * 70)

    print(f"Ontology : {ONTOLOGY_FILE}")
    print(f"RDF data : {RDF_FILE}")

    graph = load_graph()

    print(f"Graph triples: {len(graph)}")

    print_results(
        "ALL RISKS",
        query_all_risks(graph)
    )

    print_results(
        "CRITICAL RISKS",
        query_critical_risks(graph)
    )

    print_results(
        "RISK RELATIONSHIPS",
        query_risk_relationships(graph)
    )

    print()
    print("=" * 70)
    print("SPARQL EXECUTION COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
