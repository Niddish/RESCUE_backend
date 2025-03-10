from flask import Flask, jsonify
from flask_cors import CORS  
import json
import os

app = Flask(__name__)
CORS(app)  

FILE_PATH = "gpu_topology.json"

@app.route("/json")
def get_json():
    """API endpoint to return GPU topology data as JSON"""
    with open(FILE_PATH, "r") as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
