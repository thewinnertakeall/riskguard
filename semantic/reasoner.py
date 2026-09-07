import sys
from pathlib import Path

from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF, XSD


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

RG = Namespace(
    "http://riskguard.org/ontology#"
)


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
# REASONING RULE 1
#
# Critical risk:
#
# IF riskScore >= 17
# THEN risk is a CriticalRisk
# ============================================================

def infer_critical_risks(graph):

    inferred = Graph()

    inferred.bind(
        "rg",
        RG
    )

    query = """
    PREFIX rg: <http://riskguard.org/ontology#>

    SELECT ?risk
    WHERE {
        ?risk a rg:Risk .
        ?risk rg:riskScore ?score .

        FILTER(
            ?score >= 17
        )
    }
    """

    results = graph.query(query)

    count = 0

    for row in results:

        risk = row.risk

        inferred.add(
            (
                risk,
                RDF.type,
                RG.CriticalRisk
            )
        )

        count += 1

    return inferred, count


# ============================================================
# REASONING RULE 2
#
# Priority risk:
#
# IF risk is Critical
# AND risk has an incident
# AND incident severity = High
# THEN risk is a PriorityRisk
# ============================================================

def infer_priority_risks(graph):

    inferred = Graph()

    inferred.bind(
        "rg",
        RG
    )

    query = """
    PREFIX rg: <http://riskguard.org/ontology#>

    SELECT DISTINCT ?risk
    WHERE {

        ?risk a rg:Risk .

        ?risk rg:riskScore ?score .

        ?risk rg:hasIncident ?incident .

        ?incident rg:severity ?severity .

        FILTER(
            ?score >= 17
            &&
            ?severity = "High"
        )
    }
    """

    results = graph.query(query)

    count = 0

    for row in results:

        risk = row.risk

        inferred.add(
            (
                risk,
                RDF.type,
                RG.PriorityRisk
            )
        )

        count += 1

    return inferred, count


# ============================================================
# REASONING RULE 3
#
# Priority attention:
#
# IF risk is PriorityRisk
# THEN risk requiresPriorityAttention
# ============================================================

def infer_priority_attention(graph):

    inferred = Graph()

    inferred.bind(
        "rg",
        RG
    )

    query = """
    PREFIX rg: <http://riskguard.org/ontology#>

    SELECT DISTINCT ?risk
    WHERE {

        ?risk a rg:PriorityRisk .
    }
    """

    results = graph.query(query)

    count = 0

    for row in results:

        risk = row.risk

        inferred.add(
            (
                risk,
                RG.requiresPriorityAttention,
                Literal(
                    True,
                    datatype=XSD.boolean
                )
            )
        )

        count += 1

    return inferred, count


# ============================================================
# APPLY REASONING
# ============================================================

def run_reasoning(graph):

    inferred_graph = Graph()

    inferred_graph.bind(
        "rg",
        RG
    )

    # --------------------------------------------------------
    # Rule 1
    # --------------------------------------------------------

    critical_graph, critical_count = (
        infer_critical_risks(graph)
    )

    for triple in critical_graph:
        inferred_graph.add(triple)


    # --------------------------------------------------------
    # Rule 2
    # --------------------------------------------------------

    priority_graph, priority_count = (
        infer_priority_risks(
            graph + inferred_graph
        )
    )

    for triple in priority_graph:
        inferred_graph.add(triple)


    # --------------------------------------------------------
    # Rule 3
    # --------------------------------------------------------

    attention_graph, attention_count = (
        infer_priority_attention(
            graph + inferred_graph
        )
    )

    for triple in attention_graph:
        inferred_graph.add(triple)


    return (
        inferred_graph,
        critical_count,
        priority_count,
        attention_count
    )


# ============================================================
# DISPLAY INFERRED KNOWLEDGE
# ============================================================

def display_inferred_knowledge(graph):

    print()
    print("=" * 70)
    print("INFERRED KNOWLEDGE")
    print("=" * 70)

    query = """
    PREFIX rg: <http://riskguard.org/ontology#>

    SELECT ?risk ?type
    WHERE {

        ?risk a ?type .

        FILTER(
            ?type = rg:CriticalRisk
            ||
            ?type = rg:PriorityRisk
        )
    }
    """

    results = graph.query(query)

    for row in results:

        print(
            f"{row.risk} -> {row.type}"
        )


    print()
    print("-" * 70)
    print("PRIORITY ATTENTION")
    print("-" * 70)

    query_attention = """
    PREFIX rg: <http://riskguard.org/ontology#>

    SELECT ?risk ?attention
    WHERE {

        ?risk rg:requiresPriorityAttention ?attention .
    }
    """

    results = graph.query(
        query_attention
    )

    for row in results:

        print(
            f"{row.risk} -> "
            f"requiresPriorityAttention = "
            f"{row.attention}"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("RISKGUARD SEMANTIC REASONER")
    print("=" * 70)

    print(
        f"Ontology : {ONTOLOGY_FILE}"
    )

    print(
        f"RDF data : {RDF_FILE}"
    )

    # --------------------------------------------------------
    # Load graph
    # --------------------------------------------------------

    graph = load_graph()

    original_triples = len(graph)

    print(
        f"Original graph triples: "
        f"{original_triples}"
    )


    # --------------------------------------------------------
    # Reasoning
    # --------------------------------------------------------

    (
        inferred_graph,
        critical_count,
        priority_count,
        attention_count
    ) = run_reasoning(graph)


    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("REASONING RESULTS")
    print("=" * 70)

    print(
        f"Critical risks inferred : "
        f"{critical_count}"
    )

    print(
        f"Priority risks inferred : "
        f"{priority_count}"
    )

    print(
        f"Priority attention      : "
        f"{attention_count}"
    )

    print(
        f"Inferred triples        : "
        f"{len(inferred_graph)}"
    )

    print(
        f"Knowledge graph total   : "
        f"{original_triples + len(inferred_graph)}"
    )


    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    display_inferred_knowledge(
        inferred_graph
    )


    # --------------------------------------------------------
    # Safety confirmation
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("SOURCE DATA PROTECTED")
    print("=" * 70)

    print(
        "SQLite database was not modified."
    )

    print(
        "Original RDF file was not modified."
    )

    print(
        "Inferences were generated in memory."
    )

    print("=" * 70)


if __name__ == "__main__":
    main()
