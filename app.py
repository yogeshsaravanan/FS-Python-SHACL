from flask import Flask,jsonify,request
from utils import xml_to_shacl, convert_json_to_rdf, validate_rdf_with_shacl, save_to_neo4j,shacl_to_json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load SHACL constraints (from TTL file)
@app.route("/load_constraints", methods=["GET"])
def load_constraints():
    constraints_json= shacl_to_json('constraints/constraints.ttl')
    return jsonify(constraints_json)
    # with open('constraints/constraints.ttl', 'r') as file:
    #     shacl_ttl = file.read()
    # return jsonify({"constraints": shacl_ttl})

# Submit form data and validate
@app.route("/submit_form", methods=["POST"])
def submit_form():
    import pdb
    pdb.set_trace()
    data = request.json
    rdf_data = convert_json_to_rdf(data)
    
    conforms, results_text = validate_rdf_with_shacl(rdf_data)
    
    if conforms:
        save_to_neo4j(data)
        return jsonify({"message": "Data validated and stored successfully!"}), 200
    else:
        return jsonify({"message": "Validation failed", "errors": results_text}), 400

if __name__ == "__main__":
    app.run(debug=True)
