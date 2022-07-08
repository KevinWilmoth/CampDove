import flask
from flask import request, jsonify
import azure.cosmos.documents as documents
#import azure.cosmos.cosmos_client as cosmos_client
#import azure.cosmos.exceptions as exceptions
#from azure.cosmos.partition_key import PartitionKey
#import datetime

import config

#HOST = config.settings['host']
#MASTER_KEY = config.settings['master_key']
MY_TEST = config.settings['my_test']
#DATABASE_ID = config.settings['database_id']
#CONTAINER_ID = config.settings['container_id']

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return '<h1>Testing Cosmos DB Interaction 2</h1><p>' + MY_TEST + '</p>'

#@app.route('/api/v1/AddItem', methods=['GET'])
#def create_items():
#    client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
#    db        = client.get_database_client(DATABASE_ID)
#    container = db.get_container_client(CONTAINER_ID)

#    fname         = request.args['fname']
#    lname         = request.args['lname']
#    phone         = request.args['phone']
#    email         = request.args['email']
#    item_id       = fname + lname
#    person = {'id'           : item_id,
#              'first_name'   : fname,
#              'last_name'    : lname,
#              'phone'        : phone,
#              'email'        : email
#            }

#    container.create_item(body=person)

#    return "Person Added"

#@app.route('/api/v1/ReadItems', methods=['GET'])
#def read_items():
#    client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
#    db        = client.get_database_client(DATABASE_ID)
#    container = db.get_container_client(CONTAINER_ID)

    # NOTE: Use MaxItemCount on Options to control how many items come back per trip to the server
    #       Important to handle throttles whenever you are doing operations such as this that might
    #       result in a 429 (throttled request)
#    item_list = list(container.read_all_items(max_item_count=10))
    
#    item_string = ''
#    for doc in item_list:
#        item_string = item_string + '<p>' + doc.get('id') + ' ' + doc.get('first_name') + ' ' + doc.get('last_name') + ' ' + doc.get('phone') + ' ' + doc.get('email') + '</p>'

#    return item_string

if __name__ == '__main__':
    app.run(debug = True)