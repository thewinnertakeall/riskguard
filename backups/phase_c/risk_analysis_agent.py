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
# SPARQL PREFIXES
# ============================================================

PREFIXES = """
PREFIX rg: <http://riskguard.org/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""


# ============================================================
# RISK ANALYSIS AGENT
# ============================================================

class RiskAnalysisAgent:
    """
    Agent responsible for semantic analysis of occupational risks.

    The agent does not modify the SQL database or RDF source.
    It loads the semantic knowledge graph and performs analysis
    using SPARQL and reasoning results.
    """

    def __init__(self):

        self.graph = Graph()

        self.graph.parse(
            str(ONTOLOGY_FILE),
            format="turtle"
        )

        self.graph.parse(
            str(RDF_FILE),
            format="turtle"
        )


    # ========================================================
    # FIND RISK
    # ========================================================

    def find_risk(self, risk_code):

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

            FILTER(
                ?code = ?requestedCode
            )
        }
        """

        query = query.replace(
            "?requestedCode",
            f'"{risk_code}"'
        )

        results = list(
            self.graph.query(query)
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


    # ========================================================
    # GET CAUSES
    # ========================================================

    def get_causes(self, risk_uri):

        query = PREFIXES + """
        SELECT ?cause ?name ?type
        WHERE {

            ?risk rg:code ?riskCode .

            ?risk rg:hasCause ?cause .

            ?cause rg:name ?name .

            OPTIONAL {
                ?cause rg:causeType ?type .
            }

            FILTER(
                STR(?risk) = ?riskUri
            )
        }
        """

        query = query.replace(
            "?riskUri",
            f'"{risk_uri}"'
        )

        results = self.graph.query(query)

        causes = []

        for row in results:

            causes.append({
                "uri": str(row.cause),
                "name": str(row.name),
                "type": (
                    str(row.type)
                    if row.type
                    else None
                )
            })

        return causes


    # ========================================================
    # GET CONTROLS
    # ========================================================

    def get_controls(self, risk_uri):

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

            FILTER(
                STR(?risk) = ?riskUri
            )
        }
        """

        query = query.replace(
            "?riskUri",
            f'"{risk_uri}"'
        )

        results = self.graph.query(query)

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
                "effectiveness": effectiveness
            })

        return controls


    # ========================================================
    # GET INCIDENTS
    # ========================================================

    def get_incidents(self, risk_uri):

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

            FILTER(
                STR(?risk) = ?riskUri
            )
        }
        """

        query = query.replace(
            "?riskUri",
            f'"{risk_uri}"'
        )

        results = self.graph.query(query)

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
                )
            })

        return incidents


    # ========================================================
    # GET INFERRED KNOWLEDGE
    # ========================================================

    def get_inferred_status(self, risk_uri):

        critical = (
            (risk_uri, "CriticalRisk")
            in []
        )

        query = PREFIXES + """
        SELECT ?type
        WHERE {

            ?risk a ?type .

            FILTER(
                STR(?risk) = ?riskUri
            )

            FILTER(
                ?type = rg:CriticalRisk
                ||
                ?type = rg:PriorityRisk
            )
        }
        """

        query = query.replace(
            "?riskUri",
            f'"{risk_uri}"'
        )

        # The source RDF does not contain inferred triples.
        # Reproduce the reasoning rules locally so the agent
        # can consume the same semantic conclusions.

        risk_query = PREFIXES + """
        SELECT ?score
        WHERE {
            ?risk a rg:Risk .
            ?risk rg:riskScore ?score .

            FILTER(
                STR(?risk) = ?riskUri
            )
        }
        """

        risk_query = risk_query.replace(
            "?riskUri",
            f'"{risk_uri}"'
        )

        score_results = list(
            self.graph.query(risk_query)
        )

        if not score_results:
            return {
                "critical": False,
                "priority": False,
                "priority_attention": False
            }

        score = int(
            score_results[0].score
        )

        critical = score >= 17

        incident_query = PREFIXES + """
        SELECT ?severity
        WHERE {

            ?risk rg:hasIncident ?incident .

            ?incident rg:severity ?severity .

            FILTER(
                STR(?risk) = ?riskUri
            )
        }
        """

        incident_query = incident_query.replace(
            "?riskUri",
            f'"{risk_uri}"'
        )

        incidents = list(
            self.graph.query(
                incident_query
            )
        )

        high_incident = any(
            str(row.severity).lower() == "high"
            for row in incidents
        )

        priority = (
            critical
            and high_incident
        )

        return {
            "critical": critical,
            "priority": priority,
            "priority_attention": priority
        }


    # ========================================================
    # ANALYZE RISK
    # ========================================================

    def analyze(self, risk_code):

        risk = self.find_risk(
            risk_code
        )

        if not risk:
            return {
                "success": False,
                "message": (
                    f"Risk {risk_code} "
                    "was not found."
                )
            }

        risk_uri = risk["uri"]

        causes = self.get_causes(
            risk_uri
        )

        controls = self.get_controls(
            risk_uri
        )

        incidents = self.get_incidents(
            risk_uri
        )

        inferred = self.get_inferred_status(
            risk_uri
        )

        return {
            "success": True,
            "agent": "RiskAnalysisAgent",
            "risk": risk,
            "causes": causes,
            "controls": controls,
            "incidents": incidents,
            "inferred": inferred
        }


# ============================================================
# DISPLAY
# ============================================================

def display_analysis(result):

    print()
    print("=" * 70)
    print("RISKGUARD - RISK ANALYSIS AGENT")
    print("=" * 70)

    if not result["success"]:

        print(
            result["message"]
        )

        return


    risk = result["risk"]

    print()
    print("RISK")
    print("-" * 70)

    print(
        f"Code        : {risk['code']}"
    )

    print(
        f"Name        : {risk['name']}"
    )

    print(
        f"Category    : {risk['category']}"
    )

    print(
        f"Probability : {risk['probability']}"
    )

    print(
        f"Impact      : {risk['impact']}"
    )

    print(
        f"Score       : {risk['score']}"
    )

    print(
        f"Level       : {risk['level']}"
    )

    print(
        f"Status      : {risk['status']}"
    )


    print()
    print("CAUSES")
    print("-" * 70)

    for cause in result["causes"]:

        print(
            f"- {cause['name']} "
            f"({cause['type']})"
        )


    print()
    print("CONTROLS")
    print("-" * 70)

    for control in result["controls"]:

        print(
            f"- {control['name']}"
        )

        print(
            f"  Type: {control['type']}"
        )

        print(
            f"  Hierarchy: {control['hierarchy']}"
        )

        print(
            f"  Effectiveness: "
            f"{control['effectiveness']}"
        )


    print()
    print("INCIDENTS")
    print("-" * 70)

    for incident in result["incidents"]:

        print(
            f"- {incident['title']}"
        )

        print(
            f"  Type: {incident['type']}"
        )

        print(
            f"  Severity: {incident['severity']}"
        )

        print(
            f"  Status: {incident['status']}"
        )

        print(
            f"  Date: {incident['date']}"
        )


    print()
    print("SEMANTIC INFERENCE")
    print("-" * 70)

    inferred = result["inferred"]

    print(
        f"CriticalRisk             : "
        f"{inferred['critical']}"
    )

    print(
        f"PriorityRisk             : "
        f"{inferred['priority']}"
    )

    print(
        f"requiresPriorityAttention: "
        f"{inferred['priority_attention']}"
    )


    print()
    print("=" * 70)
    print("RISK ANALYSIS COMPLETED")
    print("=" * 70)


# ============================================================
# MAIN
# ============================================================

def main():

    agent = RiskAnalysisAgent()

    result = agent.analyze(
        "RISK-001"
    )

    display_analysis(
        result
    )


if __name__ == "__main__":
    main()
