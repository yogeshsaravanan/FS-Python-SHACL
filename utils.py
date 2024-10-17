import xml.etree.ElementTree as ET

from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF, XSD, SH
import pyshacl
from neo4j import GraphDatabase

# Namespace for RDF triples
EX = Namespace("http://example.org/")

def shacl_to_json(shacl_file_path):
    """
    Converts SHACL constraints from a Turtle (.ttl) file into JSON format.
    :param shacl_file_path: Path to the SHACL .ttl file
    :return: A dictionary representing form constraints in JSON format
    """
    g = Graph()
    g.parse(shacl_file_path, format="turtle")

    form_constraints = []

    for shape in g.subjects(RDF.type, SH.NodeShape):
        # Iterate over each property shape constraint
        for prop in g.objects(shape, SH.property):
            field = {}

            # Get the field name (ex:name or ex:age, etc.)
            field_name = g.value(prop, SH.path)
            field['name'] = field_name.split('/')[-1]  # Extract field name (remove namespace)

            # Get field type (xsd:string, xsd:integer, etc.)
            field_type = g.value(prop, SH.datatype)
            field['type'] = str(field_type.split('#')[-1])  # Extract data type (string, integer, etc.)

            # Add any other constraints (minLength, maxLength, minInclusive, maxInclusive, etc.)
            min_length = g.value(prop, SH.minLength)
            if min_length:
                field['minLength'] = int(min_length)

            max_length = g.value(prop, SH.maxLength)
            if max_length:
                field['maxLength'] = int(max_length)

            min_value = g.value(prop, SH.minInclusive)
            if min_value:
                field['minValue'] = int(min_value)

            max_value = g.value(prop, SH.maxInclusive)
            if max_value:
                field['maxValue'] = int(max_value)

            # Add pattern constraint (for emails, etc.)
            pattern = g.value(prop, SH.pattern)
            if pattern:
                field['pattern'] = str(pattern)

            # Add field description
            description = g.value(prop, SH.description)
            if description:
                field['description'] = str(description)

            # Add field label/name for UI rendering
            label = g.value(prop, SH.name)
            if label:
                field['label'] = str(label)

            # Add the field constraints to the form constraints list
            form_constraints.append(field)

    # Convert constraints into a JSON-serializable format (list of field dictionaries)
    return form_constraints

# 1. XML to SHACL Conversion
def xml_to_shacl(xml_file_path, output_ttl_path="constraints/constraints.ttl"):
    """
    Converts an XML file with form constraints to SHACL .ttl format.

    :param xml_file_path: Path to the XML file.
    :param output_ttl_path: Path to save the SHACL .ttl file.
    """
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    shacl_constraints = []
    for field in root.findall('field'):
        name = field.get('name')
        field_type = field.find('type').text
        
        shape = f"""
        ex:{name}Shape a sh:NodeShape ;
            sh:targetClass ex:{name} ;
            sh:property [
                sh:path ex:{name} ;
                sh:datatype xsd:{field_type} ;
        """
        if field_type == "string":
            min_len = field.find('minLength').text
            max_len = field.find('maxLength').text
            shape += f"""
                sh:minLength {min_len} ;
                sh:maxLength {max_len} ;
            """
        elif field_type == "integer":
            min_val = field.find('minValue').text
            max_val = field.find('maxValue').text
            shape += f"""
                sh:minInclusive {min_val} ;
                sh:maxInclusive {max_val} ;
            """
        
        shape += "] ."
        shacl_constraints.append(shape)

    # Write the SHACL file
    with open(output_ttl_path, "w") as ttl_file:
        ttl_file.write("\n".join(shacl_constraints))
    
    print(f"SHACL file saved to {output_ttl_path}")

# 2. JSON to RDF Conversion
def convert_json_to_rdf(data):
    """
    Converts JSON form data into RDF format.

    :param data: JSON data to convert to RDF.
    :return: RDFLib Graph containing RDF triples.
    """
    g = Graph()
    
    # Define base URI for the subject (for simplicity, it's fixed)
    base_uri = EX.Person  # This can be modified to handle unique subjects
    
    for key, value in data.items():
        predicate = EX[key]  # Define predicate as "http://example.org/{key}"
        
        if isinstance(value, str):
            obj = Literal(value, datatype=XSD.string)
        elif isinstance(value, int):
            obj = Literal(value, datatype=XSD.integer)
        elif isinstance(value, float):
            obj = Literal(value, datatype=XSD.float)
        else:
            obj = Literal(str(value))  # Default to string conversion if type is unknown

        # Add triple to graph (subject, predicate, object)
        g.add((base_uri, predicate, obj))
    
    return g

# 3. SHACL Validation
def validate_rdf_with_shacl(rdf_data, shacl_file_path="constraints/constraints.ttl"):
    """
    Validates RDF data against SHACL constraints.

    :param rdf_data: RDFLib Graph containing the data to validate.
    :param shacl_file_path: Path to the SHACL constraints (.ttl file).
    :return: Tuple (conforms, results_text), where `conforms` is a boolean and `results_text` contains validation details.
    """
    # Load SHACL constraints
    import pdb
    pdb.set_trace()
    shacl_graph = Graph().parse(shacl_file_path, format="turtle")
    
    # Validate RDF data against SHACL
    conforms, results_graph, results_text = pyshacl.validate(
        rdf_data, shacl_graph=shacl_graph,
        abort_on_first=False,  # Set to True if you want to stop at the first violation
        allow_infos=True,      # Set to True if you want to allow informational messages
        allow_warnings=True,   # Set to True if you want to allow warning messages
        advanced=False,        # Set to True for advanced SHACL features
        focus_nodes=None, 
    )

    return conforms, results_text

# 4. Saving Data to Neo4j
def save_to_neo4j(data):
    """
    Saves form data into the Neo4j graph database.

    :param data: JSON data to save to Neo4j.
    """
    # Neo4j connection (replace with your own credentials)
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Lam@415Fer"))
    session = driver.session()
    
    # Cypher query to insert data into Neo4j
    query = """
    CREATE (p:Person {name: $name, age: $age, email: $email})
    """
    
    session.run(query, data)  # Pass the data dictionary directly
    session.close()

    print("Data successfully saved to Neo4j.")
