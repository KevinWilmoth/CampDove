import flask
from flask import request, render_template
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import datetime

import config
import Church_Table

HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
MY_TEST = config.settings['my_test']
DATABASE_ID = config.settings['database_id']
CONTAINER_ID = config.settings['person_container_id']
BASE_URL = config.settings['base_url']

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/contacts', methods=['GET'])
def contacts():
    client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
    db        = client.get_database_client(DATABASE_ID)
    container = db.get_container_client(CONTAINER_ID)

    item_list = list(container.read_all_items(max_item_count=10))
    firstName = [];
    lastName  = [];
    phone     = [];
    email     = [];

    for doc in item_list:
        firstName.append(doc.get('first_name'))
        lastName.append(doc.get('last_name'))
        phone.append(doc.get('phone'))
        email.append(doc.get('email'))

    return render_template('contacts.html', FirstName = firstName, LastName = lastName, Phone = phone, Email = email)

@app.route('/add_contact', methods=['GET'])
def add_contact():
    client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
    db        = client.get_database_client(DATABASE_ID)
    container = db.get_container_client(CONTAINER_ID)

    fname         = request.args['fname']
    lname         = request.args['lname']
    phone         = request.args['phone']
    email         = request.args['email']
    item_id       = fname + lname
    person = {'id'           : item_id,
              'first_name'   : fname,
              'last_name'    : lname,
              'phone'        : phone,
              'email'        : email
            }

    container.create_item(body=person)

    item_list = list(container.read_all_items(max_item_count=10))
    firstName = [];
    lastName  = [];
    phone     = [];
    email     = [];

    for doc in item_list:
        firstName.append(doc.get('first_name'))
        lastName.append(doc.get('last_name'))
        phone.append(doc.get('phone'))
        email.append(doc.get('email'))

    return render_template('contacts.html', FirstName = firstName, LastName = lastName, Phone = phone, Email = email)

@app.route('/churches', methods=['GET'])
def churches():
    churches = Church_Table.get_contacts()
    churchName             = [];
    churchContactName      = [];
    churchContactPhone     = [];
    churchContactEmail     = [];

    for doc in churches:
        churchName.append(doc.get('church_name'))
        churchContactName.append(doc.get('contact_name'))
        churchContactPhone.append(doc.get('contact_phone'))
        churchContactEmail.append(doc.get('contact_email')) 

    return render_template('church_contacts.html', churchName = churchName, churchContactName = churchContactName, churchContactPhone = churchContactPhone, churchContactEmail = churchContactEmail)


@app.route('/add_church_contact', methods=['GET'])
def add_church_contact():
    church_name    = request.args['church_name']
    church_contact = request.args['church_contact']
    church_phone   = request.args['church_phone']
    church_email   = request.args['church_email']

    Church_Table.add_contact(church_name, church_contact, church_phone, church_email);

    churches = Church_Table.get_contacts()
    churchName             = [];
    churchContactName      = [];
    churchContactPhone     = [];
    churchContactEmail     = [];

    for doc in churches:
        churchName.append(doc.get('church_name'))
        churchContactName.append(doc.get('contact_name'))
        churchContactPhone.append(doc.get('contact_phone'))
        churchContactEmail.append(doc.get('contact_email'))  

    return render_template('church_contacts.html', churchName = churchName, churchContactName = churchContactName, churchContactPhone = churchContactPhone, churchContactEmail = churchContactEmail)

if __name__ == '__main__':
    app.run(debug = True)