# SQL -> RDF synchronization service

import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from semantic.sql_to_rdf import convert_database_to_rdf


def synchronize_knowledge_graph():
    """
    Synchronize the SQL database with the RDF knowledge graph.
    """

    return convert_database_to_rdf()


if __name__ == "__main__":

    print("==============================================")
    print("RISKGUARD KNOWLEDGE GRAPH SYNCHRONIZATION")
    print("==============================================")

    result = synchronize_knowledge_graph()

    print(result)
