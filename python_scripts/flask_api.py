from flask import Flask, jsonify, request
from flask_cors import CORS
import leafly_maria_db as db

### Leafly Data - FLASK test server ###

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# return data

@app.route('/strain/<name>', methods = ['GET'])
def search_by_name(name):
    """Get a strain matching a specified name."""
    if(request.method == 'GET'):
        data = db.connect_get(name, 'name')
        return data

@app.route('/type/<type_>', methods = ['GET'])
def strain_type(type_):
    """Get all strains matching the specified type."""
    if(request.method == 'GET'):
        data = db.connect_get(type_, 'type')
        return data

@app.route('/names/', methods = ['GET'])
def get_names():
    """Return array of all strain names as JSON string."""
    if(request.method == 'GET'):
        data = db.connect_all_names()
        return data

if __name__ == '__main__':
    app.run(debug = True)