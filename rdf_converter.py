import json
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD
from pyshacl import validate

# Define a base namespace
BASE = Namespace("http://schema.org/")

# Recursive function to handle JSON dynamically
def json_to_rdf_recursive(g, subject, json_data, ns=BASE):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            predicate = ns[key]  # Use key as predicate
            if isinstance(value, (dict, list)):  # Nested structure
                if isinstance(value, dict):
                    nested_subject = URIRef(f"{subject}/{key}")
                    g.add((subject, predicate, nested_subject))
                    json_to_rdf_recursive(g, nested_subject, value, ns)
                elif isinstance(value, list):
                    for index, item in enumerate(value):
                        nested_subject = URIRef(f"{subject}/{key}_{index}")
                        g.add((subject, predicate, nested_subject))
                        json_to_rdf_recursive(g, nested_subject, item, ns)
            else:
                # Handle literal values (strings, numbers, booleans, etc.)
                if isinstance(value, str):
                    g.add((subject, predicate, Literal(value, datatype=XSD.string)))
                elif isinstance(value, int):
                    g.add((subject, predicate, Literal(value, datatype=XSD.integer)))
                elif isinstance(value, float):
                    g.add((subject, predicate, Literal(value, datatype=XSD.float)))
                elif isinstance(value, bool):
                    g.add((subject, predicate, Literal(value, datatype=XSD.boolean)))
    else:
        # Directly add literals if no further nesting
        g.add((subject, RDF.value, Literal(json_data, datatype=XSD.string)))

# Main function to convert JSON to RDF
def json_to_rdf(json_data):
    g = Graph()
    subject = URIRef(BASE["device"])  # Root subject
    json_to_rdf_recursive(g, subject, json_data)
    return g
