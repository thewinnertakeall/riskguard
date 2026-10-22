from pathlib import Path
from rdflib import Graph

ontology_ttl = """@prefix rm: <http://recmind.org/ontology#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://recmind.org/ontology> a owl:Ontology ;
    rdfs:label "RecMind Recommendation System Ontology" ;
    rdfs:comment "Ontologia OWL-DL para el modelado semantico de usuarios, contenidos, calificaciones e inferencia de recomendaciones." ;
    owl:versionInfo "1.0.0" .

rm:User a owl:Class ; rdfs:label "Usuario" .
rm:ActiveUser a owl:Class ; rdfs:subClassOf rm:User ; rdfs:label "Usuario Activo" .
rm:Content a owl:Class ; rdfs:label "Contenido" .
rm:Movie a owl:Class ; rdfs:subClassOf rm:Content ; rdfs:label "Pelicula" .
rm:Book a owl:Class ; rdfs:subClassOf rm:Content ; rdfs:label "Libro" .
rm:Article a owl:Class ; rdfs:subClassOf rm:Content ; rdfs:label "Articulo" .
rm:Genre a owl:Class ; rdfs:label "Genero" .
rm:Rating a owl:Class ; rdfs:label "Calificacion" .
rm:Recommendation a owl:Class ; rdfs:label "Recomendacion" .
rm:HighPriorityRecommendation a owl:Class ; rdfs:subClassOf rm:Recommendation ; rdfs:label "Recomendacion de Alta Prioridad" .

rm:hasInterestInGenre a owl:ObjectProperty ; rdfs:domain rm:User ; rdfs:range rm:Genre .
rm:hasGenre a owl:ObjectProperty ; rdfs:domain rm:Content ; rdfs:range rm:Genre .
rm:hasRated a owl:ObjectProperty ; rdfs:domain rm:User ; rdfs:range rm:Rating .
rm:ratingForContent a owl:ObjectProperty ; rdfs:domain rm:Rating ; rdfs:range rm:Content .
rm:hasRecommendation a owl:ObjectProperty ; rdfs:domain rm:User ; rdfs:range rm:Recommendation .
rm:recommendsContent a owl:ObjectProperty ; rdfs:domain rm:Recommendation ; rdfs:range rm:Content .

rm:userId a owl:DatatypeProperty ; rdfs:domain rm:User ; rdfs:range xsd:string .
rm:userName a owl:DatatypeProperty ; rdfs:domain rm:User ; rdfs:range xsd:string .
rm:contentId a owl:DatatypeProperty ; rdfs:domain rm:Content ; rdfs:range xsd:string .
rm:title a owl:DatatypeProperty ; rdfs:domain rm:Content ; rdfs:range xsd:string .
rm:releaseYear a owl:DatatypeProperty ; rdfs:domain rm:Content ; rdfs:range xsd:integer .
rm:ratingValue a owl:DatatypeProperty ; rdfs:domain rm:Rating ; rdfs:range xsd:float .
rm:ratingTimestamp a owl:DatatypeProperty ; rdfs:domain rm:Rating ; rdfs:range xsd:dateTime .
rm:matchScore a owl:DatatypeProperty ; rdfs:domain rm:Recommendation ; rdfs:range xsd:float .
rm:recommendationReason a owl:DatatypeProperty ; rdfs:domain rm:Recommendation ; rdfs:range xsd:string .
"""

instances_ttl = """@prefix rm: <http://recmind.org/ontology#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

rm:Genre_SciFi a rm:Genre ;
    rdfs:label "Ciencia Ficcion" .

rm:Content_MOV101 a rm:Movie ;
    rm:contentId "MOV-101" ;
    rm:title "Matrix" ;
    rm:releaseYear 1999 ;
    rm:hasGenre rm:Genre_SciFi .

rm:User_USR001 a rm:User ;
    rm:userId "USR-001" ;
    rm:userName "Carlos Perez" ;
    rm:hasInterestInGenre rm:Genre_SciFi .

rm:Rating_RAT501 a rm:Rating ;
    rm:ratingValue "4.8"^^xsd:float ;
    rm:ratingTimestamp "2026-10-21T10:00:00"^^xsd:dateTime ;
    rm:ratingForContent rm:Content_MOV101 .

rm:User_USR001 rm:hasRated rm:Rating_RAT501 .

rm:Rec_REC901 a rm:Recommendation ;
    rm:matchScore "0.95"^^xsd:float ;
    rm:recommendationReason "Alta afinidad con genero Ciencia Ficcion" ;
    rm:recommendsContent rm:Content_MOV101 .

rm:User_USR001 rm:hasRecommendation rm:Rec_REC901 .
"""

Path("semantic/recmind_ontology.ttl").write_text(ontology_ttl, encoding="utf-8")
Path("data/recmind_instances.ttl").write_text(instances_ttl, encoding="utf-8")

g = Graph()
g.parse("semantic/recmind_ontology.ttl", format="turtle")
g.parse("data/recmind_instances.ttl", format="turtle")

print("=" * 60)
print(f"EXITO: Archivos RecMind sobreescritos y validados. Tripletos: {len(g)}")
print("=" * 60)
