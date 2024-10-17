import json
from pyshacl import validate
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD

# JSON-LD data
json_ld_data = '''
{
  "@context": {
    "ex": "http://example.org/",
    "name": "ex:name",
    "age": "ex:age"
  },
  "@id": "ex:JohnDoe",
  "@type": "ex:Person",
  "name": "John Doe",
  "age": 16
}
'''

# SHACL shape with SPARQL constraint
# shacl_ttl = """
# @prefix sh: <http://www.w3.org/ns/shacl#> .
# @prefix ex: <http://example.org/> .
# @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# ex:PersonShape
#     a sh:NodeShape ;
#     sh:targetClass ex:Person ;
#     sh:sparql [
#         a sh:SPARQLConstraint ;
#         sh:message "The age must be greater than 18." ;
#         sh:select """
#             SELECT ?this
#             WHERE {
#               ?this ex:age ?age .
#               FILTER (?age <= 18)
#             }
#         """ ;
#     ] .
# """

# Load the SHACL shape into an RDFLib graph
shacl_shapes_file = "constraints/instrument.ttl"

import pdb
pdb.set_trace()

shacl_graph = Graph()
shacl_graph.parse(shacl_shapes_file, format='turtle')

# Load the JSON-LD data into an RDFLib graph
data_graph = Graph()
data_graph.parse(data=json_ld_data, format='json-ld')

# Perform the SHACL validation
conforms, results_graph, results_text = validate(
    data_graph,
    shacl_graph=shacl_graph,
    inference='rdfs',  # Optional: perform RDFS inference
    debug=False,
    do_owl_imports=False,
    shacl_graph_format="ttl",  # SHACL format
    data_graph_format="json-ld"  # Data format
)

# Output the validation results
print("Conforms:", conforms)
print(results_text)
