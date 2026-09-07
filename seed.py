import requests
from datetime import date


# ============================================================
# CONFIGURATION
# ============================================================

BASE_URL = "http://127.0.0.1:8000"


# ============================================================
# HTTP HELPERS
# ============================================================

def post(path, payload):
    url = f"{BASE_URL}{path}"

    print(f"\nPOST {path}")

    response = requests.post(
        url,
        json=payload,
        timeout=10
    )

    print(f"Status: {response.status_code}")

    if not response.ok:
        print("Response body:")
        print(response.text)
        response.raise_for_status()

    try:
        return response.json()

    except ValueError:
        print("Response is not valid JSON:")
        print(response.text)
        raise


def get(path):
    url = f"{BASE_URL}{path}"

    response = requests.get(
        url,
        timeout=10
    )

    if not response.ok:
        print(f"\nGET {path}")
        print(f"Status: {response.status_code}")
        print(response.text)
        response.raise_for_status()

    return response.json()


def get_or_create(path, payload):
    """
    Return an existing entity with the same code,
    or create it if it does not exist.
    """

    collection = get(path)

    code = payload.get("code")

    for item in collection:
        if item.get("code") == code:
            print(
                f"\nEXISTS {path}"
                f" -> {code}"
                f" -> ID {item['id']}"
            )
            return item

    return post(path, payload)


# ============================================================
# MAIN SEED
# ============================================================

def main():

    print("=" * 60)
    print("RISKGUARD TEST DATA SEED")
    print("=" * 60)


    # ========================================================
    # PROCESS
    # ========================================================

    process = get_or_create(
        "/api/processes",
        {
            "code": "PROC-MAINT",
            "name": "Industrial Maintenance",
            "description": (
                "Industrial equipment "
                "maintenance process"
            )
        }
    )


    # ========================================================
    # AREA
    # ========================================================

    area = get_or_create(
        "/api/areas",
        {
            "code": "AREA-IND",
            "name": "Industrial Area",
            "description": (
                "Main industrial "
                "operational area"
            )
        }
    )


    # ========================================================
    # LOCATION
    # ========================================================

    location = get_or_create(
        "/api/locations",
        {
            "code": "LOC-PLANT-01",
            "name": "Main Plant",
            "description": (
                "Main production "
                "and maintenance plant"
            )
        }
    )


    # ========================================================
    # RISK
    # ========================================================

    risk = get_or_create(
        "/api/risks",
        {
            "code": "RISK-001",
            "name": "Electrical shock",
            "description": (
                "Risk of electrical shock "
                "during maintenance activities"
            ),

            "process_id": process["id"],
            "area_id": area["id"],
            "location_id": location["id"],

            "category": "Electrical",

            "probability": 4,
            "impact": 5,

            "risk_score": 20,
            "risk_level": "Critical",

            "status": "Active"
        }
    )


    # ========================================================
    # CAUSE
    # ========================================================

    cause = get_or_create(
        "/api/causes",
        {
            "code": "CAUSE-001",
            "name": "Contact with energized equipment",
            "description": (
                "Direct contact with "
                "energized electrical components"
            ),

            "cause_type": "Unsafe condition",

            "status": "Active"
        }
    )


    # ========================================================
    # CONTROL
    # ========================================================

    control = get_or_create(
        "/api/controls",
        {
            "code": "CTRL-001",
            "name": "Electrical lockout/tagout",
            "description": (
                "Lockout and tagout procedure "
                "before electrical maintenance"
            ),

            "control_type": "Administrative",

            "hierarchy_level": "Engineering",

            "effectiveness": 90,

            "status": "Active"
        }
    )


    # ========================================================
    # INCIDENT
    # ========================================================

    incident = get_or_create(
        "/api/incidents",
        {
            "code": "INC-001",
            "title": "Electrical maintenance incident",
            "description": (
                "Electrical incident during "
                "maintenance operation"
            ),

            "incident_date": date.today().isoformat(),

            "incident_type": "Accident",

            "severity": "High",

            "location_id": location["id"],

            "status": "Open"
        }
    )


    # ========================================================
    # RELATIONSHIPS
    # ========================================================

    print("\nCreating relationships...")


    # --------------------------------------------------------
    # Risk -> Cause
    # --------------------------------------------------------

    response = post(
        f"/api/risks/{risk['id']}/causes/{cause['id']}",
        {}
    )

    print(
        f"Risk {risk['id']} -> Cause {cause['id']}"
    )


    # --------------------------------------------------------
    # Risk -> Control
    # --------------------------------------------------------

    response = post(
        f"/api/risks/{risk['id']}/controls/{control['id']}",
        {}
    )

    print(
        f"Risk {risk['id']} -> Control {control['id']}"
    )


    # --------------------------------------------------------
    # Risk -> Incident
    # --------------------------------------------------------

    response = post(
        f"/api/risks/{risk['id']}/incidents/{incident['id']}",
        {}
    )

    print(
        f"Risk {risk['id']} -> Incident {incident['id']}"
    )


    # ========================================================
    # RESULT
    # ========================================================

    print("\n" + "=" * 60)
    print("RISKGUARD TEST DATA READY")
    print("=" * 60)

    print(f"Process ID : {process['id']}")
    print(f"Area ID    : {area['id']}")
    print(f"Location ID: {location['id']}")
    print(f"Risk ID    : {risk['id']}")
    print(f"Cause ID   : {cause['id']}")
    print(f"Control ID : {control['id']}")
    print(f"Incident ID: {incident['id']}")

    print("\nRisk score calculated by API:")
    print(f"Score      : {risk['risk_score']}")
    print(f"Risk level : {risk['risk_level']}")

    print("\nRelationships:")
    print("Risk -> Cause")
    print("Risk -> Control")
    print("Risk -> Incident")

    print("\n" + "=" * 60)
    print("SEED COMPLETED SUCCESSFULLY")
    print("=" * 60)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
