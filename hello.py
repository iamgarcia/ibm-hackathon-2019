from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
import atexit
import os
import json

app = Flask(__name__, static_url_path='')

db_name = 'mydb'
client = None
db = None

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
'''
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
'''

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

@app.route('/')
def root():
    return app.send_static_file('index.html')

'''
def sortBy(doc, params):
    if(doc['data']['severity'] == params.get('severity', default = 0, type = int)):
        return doc['data']['name']
'''

# Sends a GET request to server
@app.route('/api/reports', methods=['GET'])
def get_reports():
    params = request.args

    if len(params) > 0:
        pass
        
    elif client:
        return jsonify(list(map(lambda doc: doc['data'], db)))
    else:
        print('No database')
        return jsonify([])

# Sends a POST request to server
@app.route('/api/reports', methods=['POST'])
def post_report():

    # Define the request params
    # NAME : STRING | LOCATION : STRING | DESC : STRING | SEVERITY : INT | TYPE : INT | ID_OF_DISASTER : INT
    # TODO :  Seperate name into firstname and lastname (?)

    _name = request.json['name']
    _location = request.json['location']
    _desc = request.json['desc']
    _severity = request.json['severity']
    _type = request.json['type']
    _disasterID = request.json['id_of_disaster']

    data = {'data': 
            {'name': _name,
            'location': _location,
            'desc': _desc,
            'severity': _severity,
            'type': _type,
            'id_of_disaster': _disasterID}}

            
    if client:
        my_document = db.create_document(data)
        data['_id'] = my_document['_id']
        return jsonify(data)

    else:
        print('No database')
        return jsonify(data)

@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
