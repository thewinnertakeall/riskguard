import sqlite3
import json
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "data" / "riskguard.db"
CONTROLS_JSON = BASE_DIR / "app" / "iso27001" / "data" / "controls.json"


def table_exists(conn, table_name):
    result = conn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name=?
        """,
        (table_name,)
    ).fetchone()

    return result is not None


def column_exists(conn, table_name, column_name):
    columns = conn.execute(
        f"PRAGMA table_info({table_name})"
    ).fetchall()

    return any(column[1] == column_name for column in columns)


def create_iso_controls(conn):
    print("\n[1] Creando iso_controls...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS iso_controls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            code VARCHAR(30) NOT NULL UNIQUE,

            name VARCHAR(255) NOT NULL,

            description TEXT,

            category VARCHAR(100),

            implementation_status VARCHAR(50)
                DEFAULT 'Not Implemented',

            effectiveness REAL
                DEFAULT 0.0,

            applicable BOOLEAN
                DEFAULT 1,

            evidence_required BOOLEAN
                DEFAULT 1,

            created_at DATETIME
                DEFAULT CURRENT_TIMESTAMP,

            updated_at DATETIME
                DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

    print("   OK")


def seed_iso_controls(conn):
    print("\n[2] Cargando controles ISO desde controls.json...")

    if not CONTROLS_JSON.exists():
        raise FileNotFoundError(
            f"No existe: {CONTROLS_JSON}"
        )

    with open(CONTROLS_JSON, "r", encoding="utf-8") as file:
        controls = json.load(file)

    inserted = 0
    updated = 0

    for control in controls:

        code = control["code"]
        name = control["name"]
        description = control.get("description")
        category = control.get("category")
        applicable = control.get("applicable", True)

        existing = conn.execute(
            """
            SELECT id
            FROM iso_controls
            WHERE code=?
            """,
            (code,)
        ).fetchone()

        if existing:

            conn.execute(
                """
                UPDATE iso_controls

                SET
                    name=?,
                    description=?,
                    category=?,
                    applicable=?,
                    updated_at=CURRENT_TIMESTAMP

                WHERE code=?
                """,
                (
                    name,
                    description,
                    category,
                    int(applicable),
                    code
                )
            )

            updated += 1

        else:

            conn.execute(
                """
                INSERT INTO iso_controls (
                    code,
                    name,
                    description,
                    category,
                    implementation_status,
                    effectiveness,
                    applicable,
                    evidence_required
                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    code,
                    name,
                    description,
                    category,
                    "Not Implemented",
                    0.0,
                    int(applicable),
                    1
                )
            )

            inserted += 1

    conn.commit()

    print(f"   Insertados: {inserted}")
    print(f"   Actualizados: {updated}")


def create_risk_iso_controls(conn):
    print("\n[3] Creando relación risks <-> iso_controls...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS risk_iso_controls (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            risk_id INTEGER NOT NULL,

            iso_control_id INTEGER NOT NULL,

            treatment_status VARCHAR(50)
                DEFAULT 'Planned',

            notes TEXT,

            created_at DATETIME
                DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(risk_id, iso_control_id),

            FOREIGN KEY(risk_id)
                REFERENCES risks(id)
                ON DELETE CASCADE,

            FOREIGN KEY(iso_control_id)
                REFERENCES iso_controls(id)
                ON DELETE CASCADE
        )
    """)

    conn.commit()

    print("   OK")


def create_control_iso_controls(conn):
    print("\n[4] Creando relación controls <-> iso_controls...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS control_iso_controls (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            control_id INTEGER NOT NULL,

            iso_control_id INTEGER NOT NULL,

            relationship_type VARCHAR(100)
                DEFAULT 'supports',

            notes TEXT,

            created_at DATETIME
                DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(control_id, iso_control_id),

            FOREIGN KEY(control_id)
                REFERENCES controls(id)
                ON DELETE CASCADE,

            FOREIGN KEY(iso_control_id)
                REFERENCES iso_controls(id)
                ON DELETE CASCADE
        )
    """)

    conn.commit()

    print("   OK")


def create_events(conn):
    print("\n[5] Creando nuevo modelo events...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            code VARCHAR(50) NOT NULL UNIQUE,

            title VARCHAR(255) NOT NULL,

            description TEXT,

            domain VARCHAR(100)
                NOT NULL
                DEFAULT 'Operational',

            event_type VARCHAR(100)
                NOT NULL
                DEFAULT 'Incident',

            severity VARCHAR(50),

            status VARCHAR(50)
                DEFAULT 'Open',

            occurred_at DATETIME,

            reported_at DATETIME
                DEFAULT CURRENT_TIMESTAMP,

            location_id INTEGER,

            process_id INTEGER,

            risk_id INTEGER,

            source_incident_id INTEGER,

            created_at DATETIME
                DEFAULT CURRENT_TIMESTAMP,

            updated_at DATETIME
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(location_id)
                REFERENCES locations(id),

            FOREIGN KEY(process_id)
                REFERENCES processes(id),

            FOREIGN KEY(risk_id)
                REFERENCES risks(id),

            FOREIGN KEY(source_incident_id)
                REFERENCES incidents(id)
        )
    """)

    conn.commit()

    print("   OK")


def migrate_incidents_to_events(conn):
    print("\n[6] Migrando incidents existentes a events...")

    if not table_exists(conn, "incidents"):
        print("   No existe incidents. Se omite.")
        return

    columns = {
        row[1]
        for row in conn.execute(
            "PRAGMA table_info(incidents)"
        ).fetchall()
    }

    # Intentamos descubrir las columnas existentes
    id_column = "id" if "id" in columns else None

    if id_column is None:
        print("   incidents no tiene columna id. Se omite.")
        return

    rows = conn.execute(
        "SELECT * FROM incidents"
    ).fetchall()

    if not rows:
        print("   No hay incidents para migrar.")
        return

    inserted = 0

    for row in rows:

        data = dict(zip(columns, row))

        incident_id = data.get("id")

        code = (
            data.get("code")
            or f"INC-{incident_id:03d}"
        )

        title = (
            data.get("title")
            or data.get("name")
            or data.get("description")
            or f"Incident {incident_id}"
        )

        description = data.get("description")

        severity = (
            data.get("severity")
            or data.get("criticality")
        )

        status = (
            data.get("status")
            or "Open"
        )

        occurred_at = (
            data.get("date")
            or data.get("occurred_at")
            or data.get("incident_date")
        )

        risk_id = data.get("risk_id")

        existing = conn.execute(
            """
            SELECT id
            FROM events
            WHERE source_incident_id=?
            """,
            (incident_id,)
        ).fetchone()

        if existing:
            continue

        conn.execute(
            """
            INSERT INTO events (
                code,
                title,
                description,
                domain,
                event_type,
                severity,
                status,
                occurred_at,
                risk_id,
                source_incident_id
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                code,
                title,
                description,
                "Operational",
                "Incident",
                severity,
                status,
                occurred_at,
                risk_id,
                incident_id
            )
        )

        inserted += 1

    conn.commit()

    print(f"   Eventos migrados: {inserted}")


def create_evidence(conn):
    print("\n[7] Creando evidence...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS evidence (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            code VARCHAR(50) NOT NULL UNIQUE,

            title VARCHAR(255) NOT NULL,

            description TEXT,

            evidence_type VARCHAR(100),

            file_path TEXT,

            source VARCHAR(255),

            hash_sha256 VARCHAR(64),

            status VARCHAR(50)
                DEFAULT 'Active',

            collected_at DATETIME,

            owner VARCHAR(255),

            iso_control_id INTEGER,

            risk_id INTEGER,

            event_id INTEGER,

            created_at DATETIME
                DEFAULT CURRENT_TIMESTAMP,

            updated_at DATETIME
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(iso_control_id)
                REFERENCES iso_controls(id),

            FOREIGN KEY(risk_id)
                REFERENCES risks(id),

            FOREIGN KEY(event_id)
                REFERENCES events(id)
        )
    """)

    conn.commit()

    print("   OK")


def create_audits(conn):
    print("\n[8] Creando audits...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS audits (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            code VARCHAR(50) NOT NULL UNIQUE,

            title VARCHAR(255) NOT NULL,

            audit_type VARCHAR(100),

            scope TEXT,

            status VARCHAR(50)
                DEFAULT 'Planned',

            auditor VARCHAR(255),

            planned_date DATETIME,

            started_at DATETIME,

            completed_at DATETIME,

            notes TEXT,

            created_at DATETIME
                DEFAULT CURRENT_TIMESTAMP,

            updated_at DATETIME
                DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

    print("   OK")


def create_audit_controls(conn):
    print("\n[9] Creando relación audits <-> iso_controls...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS audit_controls (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            audit_id INTEGER NOT NULL,

            iso_control_id INTEGER NOT NULL,

            result VARCHAR(50)
                DEFAULT 'Pending',

            notes TEXT,

            created_at DATETIME
                DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(audit_id, iso_control_id),

            FOREIGN KEY(audit_id)
                REFERENCES audits(id)
                ON DELETE CASCADE,

            FOREIGN KEY(iso_control_id)
                REFERENCES iso_controls(id)
                ON DELETE CASCADE
        )
    """)

    conn.commit()

    print("   OK")


def create_findings(conn):
    print("\n[10] Creando findings...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS findings (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            code VARCHAR(50) NOT NULL UNIQUE,

            audit_id INTEGER,

            iso_control_id INTEGER,

            risk_id INTEGER,

            title VARCHAR(255) NOT NULL,

            description TEXT,

            finding_type VARCHAR(100),

            severity VARCHAR(50),

            status VARCHAR(50)
                DEFAULT 'Open',

            recommendation TEXT,

            due_date DATETIME,

            closed_at DATETIME,

            created_at DATETIME
                DEFAULT CURRENT_TIMESTAMP,

            updated_at DATETIME
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(audit_id)
                REFERENCES audits(id),

            FOREIGN KEY(iso_control_id)
                REFERENCES iso_controls(id),

            FOREIGN KEY(risk_id)
                REFERENCES risks(id)
        )
    """)

    conn.commit()

    print("   OK")


def create_corrective_actions(conn):
    print("\n[11] Creando corrective_actions...")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS corrective_actions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            code VARCHAR(50) NOT NULL UNIQUE,

            finding_id INTEGER NOT NULL,

            title VARCHAR(255) NOT NULL,

            description TEXT,

            responsible VARCHAR(255),

            priority VARCHAR(50),

            status VARCHAR(50)
                DEFAULT 'Open',

            due_date DATETIME,

            completed_at DATETIME,

            verification TEXT,

            created_at DATETIME
                DEFAULT CURRENT_TIMESTAMP,

            updated_at DATETIME
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(finding_id)
                REFERENCES findings(id)
                ON DELETE CASCADE
        )
    """)

    conn.commit()

    print("   OK")


def create_indexes(conn):
    print("\n[12] Creando índices...")

    indexes = [
        """
        CREATE INDEX IF NOT EXISTS
        idx_iso_controls_category
        ON iso_controls(category)
        """,

        """
        CREATE INDEX IF NOT EXISTS
        idx_iso_controls_status
        ON iso_controls(implementation_status)
        """,

        """
        CREATE INDEX IF NOT EXISTS
        idx_events_domain
        ON events(domain)
        """,

        """
        CREATE INDEX IF NOT EXISTS
        idx_events_type
        ON events(event_type)
        """,

        """
        CREATE INDEX IF NOT EXISTS
        idx_events_risk
        ON events(risk_id)
        """,

        """
        CREATE INDEX IF NOT EXISTS
        idx_evidence_iso_control
        ON evidence(iso_control_id)
        """,

        """
        CREATE INDEX IF NOT EXISTS
        idx_findings_status
        ON findings(status)
        """
    ]

    for statement in indexes:
        conn.execute(statement)

    conn.commit()

    print("   OK")


def show_summary(conn):
    print("\n" + "=" * 60)
    print("RESUMEN DE MIGRACIÓN")
    print("=" * 60)

    tables = [
        "iso_controls",
        "risk_iso_controls",
        "control_iso_controls",
        "events",
        "evidence",
        "audits",
        "audit_controls",
        "findings",
        "corrective_actions"
    ]

    for table in tables:

        if table_exists(conn, table):

            count = conn.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]

            print(f"{table:25} {count}")

    print("=" * 60)

    print("\nCONTROLES ISO:")

    controls = conn.execute("""
        SELECT
            code,
            name,
            category,
            implementation_status
        FROM iso_controls
        ORDER BY code
    """).fetchall()

    for control in controls:
        print(
            f"  {control[0]:8} | "
            f"{control[1]:45} | "
            f"{control[2]} | "
            f"{control[3]}"
        )


def main():

    print("=" * 60)
    print("RISKGUARD - MIGRACIÓN SGSI")
    print("=" * 60)

    print(f"\nDB: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)

    # Activar integridad referencial
    conn.execute("PRAGMA foreign_keys = ON")

    try:

        create_iso_controls(conn)

        seed_iso_controls(conn)

        create_risk_iso_controls(conn)

        create_control_iso_controls(conn)

        create_events(conn)

        migrate_incidents_to_events(conn)

        create_evidence(conn)

        create_audits(conn)

        create_audit_controls(conn)

        create_findings(conn)

        create_corrective_actions(conn)

        create_indexes(conn)

        show_summary(conn)

        print("\nMIGRACIÓN COMPLETADA CORRECTAMENTE.")

    except Exception:

        conn.rollback()

        print("\nERROR DURANTE LA MIGRACIÓN.")
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()
