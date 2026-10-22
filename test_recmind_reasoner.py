from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF, XSD

g = Graph()
g.parse("semantic/recmind_ontology.ttl", format="turtle")
g.parse("data/recmind_instances.ttl", format="turtle")

RM = Namespace("http://recmind.org/ontology#")

query = """
PREFIX rm: <http://recmind.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?user ?userName ?movieTitle ?score ?reason
WHERE {
    ?user a rm:User ;
          rm:userName ?userName ;
          rm:hasRecommendation ?rec .
          
    ?rec rm:recommendsContent ?movie ;
         rm:matchScore ?score ;
         rm:recommendationReason ?reason .
         
    ?movie rm:title ?movieTitle .
}
"""

results = g.query(query)

print("=" * 60)
print("RECMIND RECOMMENDATION SYSTEM - CONSULTA SPARQL")
print("=" * 60)
for row in results:
    print(f"Usuario      : {row.userName}")
    print(f"Recomienda   : {row.movieTitle}")
    print(f"Match Score  : {row.score}")
    print(f"Razon        : {row.reason}")
print("=" * 60)
