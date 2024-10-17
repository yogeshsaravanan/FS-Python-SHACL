from rdflib import Graph
from pyshacl import validate
from rdf_converter import json_to_rdf
from convert_json_ld import convert_json_to_jsonld

import pandas as pd

# Function to validate RDF against SHACL shapes





def validate_rdf_against_shacl(data_graph, shacl_shapes_file):
    # Load SHACL shapes from file
    import pdb
    pdb.set_trace()
    
    shacl_graph = Graph()
    shacl_graph.parse(shacl_shapes_file, format="turtle")
    
    # Validate the RDF data against the SHACL shapes
    conforms, results_graph, results_text = validate(data_graph, shacl_graph=shacl_graph,
        data_graph_format="json-ld",
        shacl_graph_format="ttl",
        inference="rdfs",
        debug=True,
        serialize_report_graph="ttl",)
    
    # Print validation results
    
    if conforms:
        print("The data conforms to the SHACL shapes.")
    else:
        print("The data does not conform to the SHACL shapes.")
        print("Validation report:\n", results_text)
        
    return conforms, results_graph, results_text
        
def get_report_details(results_graph):
    
    import pdb
    pdb.set_trace()
    
    sparql = """
    SELECT ?id ?focus ?path ?value ?constraint ?message
      WHERE {
        ?id rdf:type sh:ValidationResult .
        ?id sh:focusNode ?focus .
        ?id sh:resultPath ?path .
        ?id sh:value ?value .
        ?id sh:resultMessage ?message .
        ?id sh:sourceConstraintComponent ?constraint
      }
    """
    result_graph = Graph()
    result_graph.parse(results_graph, format="turtle",encoding="utf-8")
    
    nm = result_graph.namespace_manager

    for s, p, o in sorted(result_graph):
        print(s.n3(nm), p.n3(nm), o.n3(nm))

    # df = result_graph.query_as_df(sparql)
    # print(df)

# RDF data graph from JSON conversion
# Or the RDF graph you have

json_data = {
    "NAME": "Test_1",
    "Description": "Validating_shacl",
    "XMA_ANA": [
        {
            "0": 0,
            "Measurement_NO": "",
            "Channel_type": "",
            "Min": "",
            "Accuracy": "",
            "Status": "",
            "Config_Delay": ""
        }
    ],
    "XMA_THC": [
        {
            "0": 0,
            "Measurement_NO": "1",
            "Channel_type": "Thermocouple K",
            "Min": "20",
            "Accuracy": "22",
            "Status": "progress",
            "Config_Delay": "1"
        }
    ]
}

rdf_graph = """
{
  "@context": {
    "schema": "http://schema.org/",
    "ex": "http://example.org/ex#",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@id": "ex:XMA3",
  "@type": "schema:XMA3",
  "schema:NAME": {
    "@value": "Test_1",
    "@type": "xsd:string"
  },
  "schema:Description": {
    "@value": "Validating_shacl",
    "@type": "xsd:string"
  },
  "schema:PSI_Current": {
    "@value": 5,
    "@type": "xsd:integer"
  },
  "schema:PSI_Voltage": {
    "@value": 5,
    "@type": "xsd:integer"
  },
  "schema:XMA_ANA": {
    "@id": "ex:XMA_ANA_0",
    "@type": "schema:ParentElements",
    "schema:Measurement_NO": {
      "@value": "1",
      "@type": "xsd:string"
    },
    "schema:Channel_type": {
      "@value": "Thermocouple K",
      "@type": "xsd:string"
    },
    "schema:Min": {
      "@value": 1,
      "@type": "xsd:integer"
    },
    "schema:Accuracy": {
      "@value": 1,
      "@type": "xsd:integer"
    },
    "schema:Status": {
      "@value": "Progress",
      "@type": "xsd:string"
    },
    "schema:Config_Delay": {
      "@value": "1",
      "@type": "xsd:string"
    }
  },
  "schema:XMA_THC": {
    "@id": "ex:XMA_THC_0",
    "@type": "schema:ParentElements",
    "schema:Measurement_NO": {
      "@value": "1",
      "@type": "xsd:string"
    },
    "schema:Channel_type": {
      "@value": "Thermocouple K",
      "@type": "xsd:string"
    },
    "schema:Min": {
      "@value": 20,
      "@type": "xsd:integer"
    },
    "schema:Accuracy": {
      "@value": 22,
      "@type": "xsd:integer"
    },
    "schema:Status": {
      "@value": "progress",
      "@type": "xsd:string"
    },
    "schema:Config_Delay": {
      "@value": "1",
      "@type": "xsd:string"
    }
  }
}
"""


# rdf_graph= """
# {
#     "@context": {
#         "name": "http://schema.org/name",
#         "age": "http://schema.org/age",
#         "address": {
#             "@id": "http://schema.org/address",
#             "@type": "@id"
#         },
#         "street": "http://schema.org/streetAddress",
#         "city": "http://schema.org/addressLocality",
#         "phone": "http://schema.org/telephone",
#         "email": "http://schema.org/email",
#         "@type": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
#     },
#     "@type": "XMA3",
#     "name": "Test_1",
#     "Description": "Validating_shacl",
#     "PSI_Voltage": "5",
#     "PSI_Current": "5",
#     "XMA_ANA": [
#         {
#             "@type": "ParentElementShape",
#             "Measurement_NO": "1",
#             "Channel_type": "Thermocouple K",
#             "Min": "20",
#             "Accuracy": "5",
#             "Status": "active",
#             "Config_Delay": "1"
#         }
#     ],
#     "XMA_THC": [
#         {
#             "@type": "ParentElementShape",
#             "Measurement_NO": "1",
#             "Channel_type": "Thermocouple K",
#             "Min": "20",
#             "Accuracy": "5",
#             "Status": "active",
#             "Config_Delay": "1"
#         }
#     ]
# }
# """

import pdb
pdb.set_trace()

# rdf_graph = json_to_rdf(json_data)

# rdf_shapes_file = "constraints/rdf.ttl" 
# rdf_graph = Graph()
# rdf_graph.parse(rdf_shapes_file, format="turtle")




# Load your RDF data into a graph
# rdf_graph = Graph()
# rdf_graph.parse(data=rdf_data, format="turtle")

# Example SHACL shapes file
# rdf_graph =convert_json_to_jsonld(json_data)

shacl_shapes_file = "constraints/instrument.ttl"  # The SHACL shapes in Turtle format

# Validate the RDF graph against SHACL
conforms, results_graph, results_text =validate_rdf_against_shacl(rdf_graph, shacl_shapes_file)

get_report_details(results_graph)
