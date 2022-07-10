import flask
from flask import request, render_template
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import datetime

import config
import Church_Table
import tab_table
import transaction_table

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
    churchName             = []
    churchContactName      = []
    churchContactPhone     = []
    churchContactEmail     = []

    for doc in churches:
        churchName.append(doc.get('church_name'))
        churchContactName.append(doc.get('contact_name'))
        churchContactPhone.append(doc.get('contact_phone'))
        churchContactEmail.append(doc.get('contact_email'))  

    return render_template('church_contacts.html', churchName = churchName, churchContactName = churchContactName, churchContactPhone = churchContactPhone, churchContactEmail = churchContactEmail)
   

@app.route('/add_tabs', methods=['POST'])
def add_tab():
    camper_fname   = request.form['camper_first_name']
    camper_lname   = request.form['camper_last_name']
    church_name    = request.form['church']
    contact_name   = request.form['contact_name']
    worker_name    = request.form['worker_name']
    no_limit       = request.form['no_limit']
    weekly_limit   = request.form['weekly_limit']
    prepaid_amount = request.form['prepaid_amount']

    app.logger.info('app.add_tab noLimit = [' + no_limit + ']')

    tab_table.add_tab(camper_fname, camper_lname, church_name, contact_name, worker_name, weekly_limit, prepaid_amount, no_limit,app)

    return tabs()
                          
@app.route('/delete_tab', methods=['POST'])
def delete_tab():
    id   = request.form['id']

    app.logger.info('app.delete_tab id = [' + id + ']')

    tab_table.delete_tab(id)

    return tabs()

@app.route('/tab_detail', methods=['POST'])
def tab_detail():
    id     = request.form['id']
    tab    = tab_table.get_tab(id)
    transactions = transaction_table.get_transactions_for_camper(id,app)

    transactionDays    = []
    transactionAmounts = []

    for doc in transactions:
        transactionDays.append(doc.get('day_of_week'));
        transactionAmounts.append(doc.get('amount'));

    return render_template('tab_detail.html',  
                           camperFirstName    = tab.get('camper_first_name'),
                           camperLastNamee    = tab.get('camper_last_name'), 
                           NoLimit            = tab.get('noLimit'),
                           homeChurch         = tab.get('home_church'),
                           dailyLimit         = tab.get('dailyLimit'),
                           contactName        = tab.get('contact_name'),
                           weeklyLimit        = tab.get('weeklyLimit'),
                           workerName         = tab.get('workerName'),
                           id                 = tab.get('id'),
                           prepaidAmount      = tab.get('prepaid'),
                           transactionDays    = transactionDays,
                           transactionAmounts = transactionAmounts
                          )

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    id     = request.form['id']
    amount = request.form['transaction_amount']
    tab    = tab_table.get_tab(id)
    transaction_table.add_transaction(id,amount)
    transactions = transaction_table.get_transactions_for_camper(id,app)

    transactionDays    = []
    transactionAmounts = []
    transactionNumbers = []
    transactionTotals  = []

    counter            = 1
    transactionTotal   = 0

    for doc in transactions:
        transactionAmount = float(doc.get('amount'))
        transactionTotal  = transactionTotal + transactionAmount
        transactionDays.append(doc.get('day_of_week'))
        transactionAmounts.append(str(transactionAmount))
        transactionNumbers.append(str(counter))
        transactionTotals.append(str(transactionTotal))
        counter = counter + 1

    return render_template('tab_detail.html',  
                           camperFirstName    = tab.get('camper_first_name'),
                           camperLastNamee    = tab.get('camper_last_name'), 
                           NoLimit            = tab.get('noLimit'),
                           homeChurch         = tab.get('home_church'),
                           dailyLimit         = tab.get('dailyLimit'),
                           contactName        = tab.get('contact_name'),
                           weeklyLimit        = tab.get('weeklyLimit'),
                           workerName         = tab.get('workerName'),
                           id                 = tab.get('id'),
                           prepaidAmount      = tab.get('prepaid'),
                           transactionDays    = transactionDays,
                           transactionAmounts = transactionAmounts,
                           transactionNumbers = transactionNumbers,
                           transactionTotals  = transactionTotals
                          )

@app.route('/tabs', methods=['GET'])
def tabs():
    tabs = tab_table.get_tabs()
    camperFirstName      = []
    camperLastName       = []
    church_list          = []
    contact_name_list    = []
    worker_name_list     = []
    no_limit_list        = []
    weekly_limit_list    = []
    daily_limit_list     = []
    prepaid_amount_list  = []
    id_list              = []


    for doc in tabs:
        camperFirstName.append(doc.get('camper_first_name'))
        camperLastName.append(doc.get('camper_last_name'))
        church_list.append(doc.get('home_church'))
        contact_name_list.append(doc.get('contact_name'))
        worker_name_list.append(doc.get('workerName'))
        no_limit_list.append(doc.get('noLimit'))
        weekly_limit_list.append(doc.get('weeklyLimit'))
        daily_limit_list.append(doc.get('dailyLimit'))
        prepaid_amount_list.append(doc.get('prepaid'))
        id_list.append(doc.get('id'))

    return render_template('add_tab.html',  
                           camperFirstName    = camperFirstName,
                           camperLastName     = camperLastName, 
                           church             = church_list, 
                           contactName        = contact_name_list, 
                           workerName         = worker_name_list,
                           NoLimit            = no_limit_list,
                           WeeklyLimit        = weekly_limit_list,
                           DailyLimit         = daily_limit_list,
                           PrepaidLimitAmount = prepaid_amount_list,
                           ids                = id_list
                          )

if __name__ == '__main__':
    app.run(debug = True)