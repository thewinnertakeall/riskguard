from pathlib import Path

from rdflib import Graph

from domain.interfaces.semantic_repository import (
    SemanticRepository
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RDF_FILE = PROJECT_ROOT / "data" / "riskguard.ttl"
ONTOLOGY_FILE = PROJECT_ROOT / "semantic" / "ontology.ttl"

PREFIXES = """
PREFIX rg: <http://riskguard.org/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""


class RDFSemanticRepository(SemanticRepository):
    """
    RDF adapter for the RiskGuard semantic knowledge graph.

    Responsible for:
    - loading RDF/OWL
    - executing semantic queries
    - exposing semantic data through the repository port

    It does not contain agent orchestration logic.
    """

    def __init__(
        self,
        rdf_file=None,
        ontology_file=None,
    ):
        self.rdf_file = Path(
            rdf_file or RDF_FILE
        )

        self.ontology_file = Path(
            ontology_file or ONTOLOGY_FILE
        )

    def _load_graph(self):
        graph = Graph()

        if self.ontology_file.exists():
            graph.parse(
                str(self.ontology_file),
                format="turtle"
            )

        if self.rdf_file.exists():
            graph.parse(
                str(self.rdf_file),
                format="turtle"
            )

        return graph

    def find_risk(self, code: str):
        graph = self._load_graph()

        query = PREFIXES + """
        SELECT
            ?risk
            ?code
            ?name
            ?description
            ?category
            ?probability
            ?impact
            ?score
            ?level
            ?status

        WHERE {
            ?risk a rg:Risk .

            ?risk rg:code ?code .
            ?risk rg:name ?name .
            ?risk rg:description ?description .
            ?risk rg:category ?category .
            ?risk rg:probability ?probability .
            ?risk rg:impact ?impact .
            ?risk rg:riskScore ?score .
            ?risk rg:riskLevel ?level .
            ?risk rg:status ?status .

            FILTER(?code = ?target)
        }
        """

        results = list(
            graph.query(
                query,
                initBindings={"target": code}
            )
        )

        if not results:
            return None

        row = results[0]

        return {
            "uri": str(row.risk),
            "code": str(row.code),
            "name": str(row.name),
            "description": str(row.description),
            "category": str(row.category),
            "probability": int(row.probability),
            "impact": int(row.impact),
            "score": int(row.score),
            "level": str(row.level),
            "status": str(row.status),
        }

    def find_critical_risks(self):
        graph = self._load_graph()

        query = PREFIXES + """
        SELECT ?risk ?code ?name ?score
        WHERE {
            ?risk a rg:Risk ;
                  rg:code ?code ;
                  rg:name ?name ;
                  rg:riskScore ?score .

            FILTER(?score >= 17)
        }
        """

        return list(graph.query(query))

    def get_causes(self, risk_uri: str):
        graph = self._load_graph()

        query = PREFIXES + """
        SELECT ?cause ?name ?type
        WHERE {
            ?risk rg:hasCause ?cause .
            ?cause rg:name ?name .

            OPTIONAL {
                ?cause rg:causeType ?type .
            }

            FILTER(STR(?risk) = ?target)
        }
        """

        results = graph.query(
            query,
            initBindings={"target": risk_uri}
        )

        return [
            {
                "uri": str(row.cause),
                "name": str(row.name),
                "type": (
                    str(row.type)
                    if row.type
                    else None
                ),
            }
            for row in results
        ]

    def get_controls(self, risk_uri: str):
        graph = self._load_graph()

        query = PREFIXES + """
        SELECT
            ?control
            ?name
            ?type
            ?hierarchy
            ?effectiveness

        WHERE {
            ?risk rg:hasControl ?control .
            ?control rg:name ?name .

            OPTIONAL {
                ?control rg:controlType ?type .
            }

            OPTIONAL {
                ?control rg:hierarchyLevel ?hierarchy .
            }

            OPTIONAL {
                ?control rg:effectiveness ?effectiveness .
            }

            FILTER(STR(?risk) = ?target)
        }
        """

        results = graph.query(
            query,
            initBindings={"target": risk_uri}
        )

        controls = []

        for row in results:
            effectiveness = None

            if row.effectiveness:
                effectiveness = float(
                    row.effectiveness
                )

            controls.append({
                "uri": str(row.control),
                "name": str(row.name),
                "type": (
                    str(row.type)
                    if row.type
                    else None
                ),
                "hierarchy": (
                    str(row.hierarchy)
                    if row.hierarchy
                    else None
                ),
                "effectiveness": effectiveness,
            })

        return controls

    def get_incidents(self, risk_uri: str):
        graph = self._load_graph()

        query = PREFIXES + """
        SELECT
            ?incident
            ?title
            ?type
            ?severity
            ?status
            ?date

        WHERE {
            ?risk rg:hasIncident ?incident .
            ?incident rg:title ?title .

            OPTIONAL {
                ?incident rg:incidentType ?type .
            }

            OPTIONAL {
                ?incident rg:severity ?severity .
            }

            OPTIONAL {
                ?incident rg:status ?status .
            }

            OPTIONAL {
                ?incident rg:incidentDate ?date .
            }

            FILTER(STR(?risk) = ?target)
        }
        """

        results = graph.query(
            query,
            initBindings={"target": risk_uri}
        )

        incidents = []

        for row in results:
            incidents.append({
                "uri": str(row.incident),
                "title": str(row.title),
                "type": (
                    str(row.type)
                    if row.type
                    else None
                ),
                "severity": (
                    str(row.severity)
                    if row.severity
                    else None
                ),
                "status": (
                    str(row.status)
                    if row.status
                    else None
                ),
                "date": (
                    str(row.date)
                    if row.date
                    else None
                ),
            })

        return incidents

    def get_inferred_status(self, risk_uri: str):
        """
        Execute the existing RiskGuard semantic reasoning rules.

        Reasoning remains in semantic.reasoner.
        This repository only adapts the result for the agent.
        """

        from semantic.reasoner import run_reasoning

        graph = self._load_graph()

        inferred_graph, _, _, _ = run_reasoning(
            graph
        )

        critical = False
        priority = False
        priority_attention = False

        for subject, predicate, obj in inferred_graph:

            if str(subject) != risk_uri:
                continue

            predicate_name = str(predicate)

            if predicate_name.endswith(
                "#type"
            ):
                object_name = str(obj)

                if object_name.endswith(
                    "#CriticalRisk"
                ):
                    critical = True

                if object_name.endswith(
                    "#PriorityRisk"
                ):
                    priority = True

            if predicate_name.endswith(
                "#requiresPriorityAttention"
            ):
                priority_attention = (
                    str(obj).lower() == "true"
                )

        return {
            "critical": critical,
            "priority": priority,
            "priority_attention": priority_attention,
        }

    def get_graph_status(self):
        if not self.rdf_file.exists():
            return {
                "status": "missing",
                "triples": 0,
                "file": str(self.rdf_file),
            }

        graph = self._load_graph()

        return {
            "status": "available",
            "triples": len(graph),
            "file": str(self.rdf_file),
        }
