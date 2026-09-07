import sys
from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORTS
# ============================================================

from rdflib import Graph, Literal
from rdflib.namespace import RDF, XSD

from app.database import SessionLocal

from app.models import (
    Process,
    Area,
    Location,
    Risk,
    Cause,
    Control,
    Incident,
)

from semantic.namespace import RISKGUARD


# ============================================================
# CONFIGURATION
# ============================================================

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "riskguard.ttl"
)


# ============================================================
# HELPERS
# ============================================================

def add_literal(
    graph,
    subject,
    predicate,
    value,
    datatype=None
):
    if value is None:
        return

    if datatype:
        graph.add(
            (
                subject,
                predicate,
                Literal(
                    value,
                    datatype=datatype
                )
            )
        )
    else:
        graph.add(
            (
                subject,
                predicate,
                Literal(value)
            )
        )


def entity_uri(
    entity_type,
    code
):
    return RISKGUARD[
        f"{entity_type}/{code}"
    ]


# ============================================================
# SQL → RDF
# ============================================================

def convert_database_to_rdf():

    graph = Graph()

    graph.bind(
        "rg",
        RISKGUARD
    )

    graph.bind(
        "rdf",
        RDF
    )

    graph.bind(
        "xsd",
        XSD
    )

    db = SessionLocal()

    try:

        # ====================================================
        # PROCESSES
        # ====================================================

        processes = db.query(
            Process
        ).all()

        for process in processes:

            subject = entity_uri(
                "process",
                process.code
            )

            graph.add(
                (
                    subject,
                    RDF.type,
                    RISKGUARD.Process
                )
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.code,
                process.code
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.name,
                process.name
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.description,
                process.description
            )


        # ====================================================
        # AREAS
        # ====================================================

        areas = db.query(
            Area
        ).all()

        for area in areas:

            subject = entity_uri(
                "area",
                area.code
            )

            graph.add(
                (
                    subject,
                    RDF.type,
                    RISKGUARD.Area
                )
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.code,
                area.code
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.name,
                area.name
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.description,
                area.description
            )


        # ====================================================
        # LOCATIONS
        # ====================================================

        locations = db.query(
            Location
        ).all()

        for location in locations:

            subject = entity_uri(
                "location",
                location.code
            )

            graph.add(
                (
                    subject,
                    RDF.type,
                    RISKGUARD.Location
                )
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.code,
                location.code
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.name,
                location.name
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.description,
                location.description
            )


        # ====================================================
        # CAUSES
        # ====================================================

        causes = db.query(
            Cause
        ).all()

        for cause in causes:

            subject = entity_uri(
                "cause",
                cause.code
            )

            graph.add(
                (
                    subject,
                    RDF.type,
                    RISKGUARD.Cause
                )
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.code,
                cause.code
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.name,
                cause.name
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.description,
                cause.description
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.causeType,
                cause.cause_type
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.status,
                cause.status
            )


        # ====================================================
        # CONTROLS
        # ====================================================

        controls = db.query(
            Control
        ).all()

        for control in controls:

            subject = entity_uri(
                "control",
                control.code
            )

            graph.add(
                (
                    subject,
                    RDF.type,
                    RISKGUARD.Control
                )
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.code,
                control.code
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.name,
                control.name
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.description,
                control.description
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.controlType,
                control.control_type
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.hierarchyLevel,
                control.hierarchy_level
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.effectiveness,
                control.effectiveness,
                XSD.double
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.status,
                control.status
            )


        # ====================================================
        # INCIDENTS
        # ====================================================

        incidents = db.query(
            Incident
        ).all()

        for incident in incidents:

            subject = entity_uri(
                "incident",
                incident.code
            )

            graph.add(
                (
                    subject,
                    RDF.type,
                    RISKGUARD.Incident
                )
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.code,
                incident.code
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.title,
                incident.title
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.description,
                incident.description
            )

            if incident.incident_date:

                add_literal(
                    graph,
                    subject,
                    RISKGUARD.incidentDate,
                    incident.incident_date.isoformat(),
                    XSD.date
                )

            add_literal(
                graph,
                subject,
                RISKGUARD.incidentType,
                incident.incident_type
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.severity,
                incident.severity
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.status,
                incident.status
            )

            if incident.location:

                location_uri = entity_uri(
                    "location",
                    incident.location.code
                )

                graph.add(
                    (
                        subject,
                        RISKGUARD.locatedIn,
                        location_uri
                    )
                )


        # ====================================================
        # RISKS
        # ====================================================

        risks = db.query(
            Risk
        ).all()

        for risk in risks:

            subject = entity_uri(
                "risk",
                risk.code
            )

            graph.add(
                (
                    subject,
                    RDF.type,
                    RISKGUARD.Risk
                )
            )

            # ------------------------------------------------
            # Basic attributes
            # ------------------------------------------------

            add_literal(
                graph,
                subject,
                RISKGUARD.code,
                risk.code
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.name,
                risk.name
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.description,
                risk.description
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.category,
                risk.category
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.probability,
                risk.probability,
                XSD.integer
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.impact,
                risk.impact,
                XSD.integer
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.riskScore,
                risk.risk_score,
                XSD.integer
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.riskLevel,
                risk.risk_level
            )

            add_literal(
                graph,
                subject,
                RISKGUARD.status,
                risk.status
            )


            # ------------------------------------------------
            # Risk → Process
            # ------------------------------------------------

            if risk.process_object:

                process_uri = entity_uri(
                    "process",
                    risk.process_object.code
                )

                graph.add(
                    (
                        subject,
                        RISKGUARD.belongsToProcess,
                        process_uri
                    )
                )


            # ------------------------------------------------
            # Risk → Area
            # ------------------------------------------------

            if risk.area_object:

                area_uri = entity_uri(
                    "area",
                    risk.area_object.code
                )

                graph.add(
                    (
                        subject,
                        RISKGUARD.belongsToArea,
                        area_uri
                    )
                )


            # ------------------------------------------------
            # Risk → Location
            # ------------------------------------------------

            if risk.location_object:

                location_uri = entity_uri(
                    "location",
                    risk.location_object.code
                )

                graph.add(
                    (
                        subject,
                        RISKGUARD.locatedIn,
                        location_uri
                    )
                )


            # ------------------------------------------------
            # Risk → Causes
            # ------------------------------------------------

            for cause in risk.causes:

                cause_uri = entity_uri(
                    "cause",
                    cause.code
                )

                graph.add(
                    (
                        subject,
                        RISKGUARD.hasCause,
                        cause_uri
                    )
                )


            # ------------------------------------------------
            # Risk → Controls
            # ------------------------------------------------

            for control in risk.controls:

                control_uri = entity_uri(
                    "control",
                    control.code
                )

                graph.add(
                    (
                        subject,
                        RISKGUARD.hasControl,
                        control_uri
                    )
                )


            # ------------------------------------------------
            # Risk → Incidents
            # ------------------------------------------------

            for incident in risk.incidents:

                incident_uri = entity_uri(
                    "incident",
                    incident.code
                )

                graph.add(
                    (
                        subject,
                        RISKGUARD.hasIncident,
                        incident_uri
                    )
                )


        # ====================================================
        # SERIALIZATION
        # ====================================================

        OUTPUT_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        graph.serialize(
            destination=str(
                OUTPUT_FILE
            ),
            format="turtle"
        )

        print("=" * 60)
        print("RISKGUARD SQL -> RDF ETL COMPLETED")
        print("=" * 60)
        print(
            f"Output file : {OUTPUT_FILE}"
        )
        print(
            f"Triples     : {len(graph)}"
        )
        print("=" * 60)

    finally:

        db.close()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    convert_database_to_rdf()
