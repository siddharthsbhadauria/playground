from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import json

app = Flask(__name__, static_folder="../json-viewer/build")
CORS(app)

directory = "/Users/deepeval/deepeval_test_results"  # Change this to your directory

@app.route('/api/files')
def list_files():
    files = [f for f in os.listdir(directory) if f.endswith('.json')]
    return jsonify(files)

@app.route('/api/file/<filename>')
def get_file(filename):
    with open(os.path.join(directory, filename), 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)