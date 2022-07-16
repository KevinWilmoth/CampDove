import flask
from flask import request, render_template
from flask import redirect
from flask import url_for
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import datetime

import config
import tab_table
import transaction_table
import camper_class

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

@app.route('/add_tabs', methods=['POST'])
def add_tab():
    camper_fname   = request.form['camper_first_name']
    camper_lname   = request.form['camper_last_name']
    church_name    = request.form['church']
    contact_name   = request.form['contact_name']
    worker_name    = request.form['worker_name']
    no_limit       = 'False'
    
    if "no_limit" in request.form:
        no_limit = 'True'
    
    if 'weekly_limit' not in request.form:
        weekly_limit = '0.0'
    else:
        weekly_limit   = request.form['weekly_limit']

    prepaid_amount = request.form['prepaid_amount']
    if prepaid_amount=='':
        prepaid_amount = '0.0'

    app.logger.info('prepaid_amount = [' + prepaid_amount + ']')

    tab_table.add_tab(camper_fname, camper_lname, church_name, contact_name, worker_name, weekly_limit, prepaid_amount, no_limit,app)

    return redirect('/tabs')
                          
@app.route('/delete_tab', methods=['POST'])
def delete_tab():
    id   = request.form['id']

    app.logger.info('app.delete_tab id = [' + id + ']')

    tab_table.delete_tab(id)

    return redirect('/tabs')

@app.route('/tab_detail', methods=['POST'])
def tab_detail():
    id     = request.form['id']
    tab    = tab_table.get_tab(id)
    transactions = transaction_table.get_transactions_for_camper(id,app)

    transactionDays    = []
    transactionAmounts = []
    transactionNumbers = []
    transactionTotals  = []
    transactionIds     = []

    counter            = 1
    transactionTotal   = 0

    for doc in transactions:
        transactionAmount = float(doc.get('amount'))
        transactionTotal  = transactionTotal + transactionAmount
        transactionDays.append(doc.get('day_of_week'))
        transactionAmounts.append(str(transactionAmount))
        transactionIds.append(doc.get('id'))
        transactionNumbers.append(str(counter))
        transactionTotals.append(str(transactionTotal))
        counter = counter + 1

    return render_template('tab_detail.html',  
                           camperFirstName    = tab.get('camper_first_name'),
                           camperLastName     = tab.get('camper_last_name'), 
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
                           transactionTotals  = transactionTotals,
                           transactionIds     = transactionIds
                          )

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    id     = request.form['id']
    amount = request.form['transaction_amount']
    transaction_table.add_transaction(id,amount)

    return redirect(url_for('show_tab'), code=307)

@app.route('/delete_transaction', methods=['POST'])
def delete_transaction():
    transaction_id  = request.form['transaction_id']
    transaction_table.delete_transaction(transaction_id)

    return redirect(url_for('show_tab'), code=307)

@app.route('/tabs', methods=['GET'])
def tabs():
    tabs = tab_table.get_tabs()
    campers              = []

    for doc in tabs:
        c1 = camper_class.camper(doc.get('camper_first_name'),
                                doc.get('camper_last_name'),
                                doc.get('home_church'),
                                doc.get('contact_name'),
                                doc.get('workerName'),
                                doc.get('noLimit'),
                                doc.get('weeklyLimit'),
                                doc.get('dailyLimit'),
                                doc.get('prepaid'),
                                doc.get('id')
                   )
        campers.append(c1)

    campers.sort(key=lambda x: (x.lname, x.fname))

    return render_template('add_tab.html', 
                           campers = campers
                          )

@app.route('/show_tab', methods=['POST','GET'])
def show_tab():
    tabs = tab_table.get_tabs()
    campers              = []

    id           = request.form['id']
    transactions = transaction_table.get_transactions_for_camper(id,app)
    tab          = tab_table.get_tab(id)

    transactionDays     = []
    transactionAmounts  = []
    transactionNumbers  = []
    transactionTotals   = []
    transactionIds      = []
    weeklyLimitWarnings = []

    counter            = 1
    transactionTotal   = 0

        
    for doc in tabs:
        c1 = camper_class.camper(doc.get('camper_first_name'),
                                doc.get('camper_last_name'),
                                doc.get('home_church'),
                                doc.get('contact_name'),
                                doc.get('workerName'),
                                doc.get('noLimit'),
                                doc.get('weeklyLimit'),
                                doc.get('dailyLimit'),
                                doc.get('prepaid'),
                                doc.get('id')
                   )
        campers.append(c1)

    for transaction in transactions:
        weeklyLimitWarning = 'noWarning'
        transactionAmount = float(transaction.get('amount'))
        transactionTotal  = transactionTotal + transactionAmount
        transactionDays.append(transaction.get('day_of_week'))
        transactionAmounts.append(str(transactionAmount))
        transactionIds.append(transaction.get('id'))
        transactionNumbers.append(str(counter))
        transactionTotals.append(str(transactionTotal))
        weeklyLimitWarnings.append
        counter = counter + 1
        if (float(transactionTotal) > tab.get('weeklyLimit')) and (tab.get('noLimit') == False):
            weeklyLimitWarning = 'overLimit'
        elif ((float(transactionTotal) + 5.0) >= tab.get('weeklyLimit')) and (tab.get('noLimit') == False):
             weeklyLimitWarning = 'warning'

        weeklyLimitWarnings.append(weeklyLimitWarning)

            
    campers.sort(key=lambda x: (x.lname, x.fname))

    return render_template('show_tab.html', 
                           campers = campers,
                           camperFirstName     = tab.get('camper_first_name'),
                           camperLastName      = tab.get('camper_last_name'), 
                           NoLimit             = tab.get('noLimit'),
                           homeChurch          = tab.get('home_church'),
                           dailyLimit          = tab.get('dailyLimit'),
                           contactName         = tab.get('contact_name'),
                           weeklyLimit         = tab.get('weeklyLimit'),
                           workerName          = tab.get('workerName'),
                           id                  = tab.get('id'),
                           prepaidAmount       = tab.get('prepaid'),
                           transactionDays     = transactionDays,
                           transactionAmounts  = transactionAmounts,
                           transactionNumbers  = transactionNumbers,
                           transactionTotals   = transactionTotals,
                           transactionIds      = transactionIds,
                           weeklyLimitWarnings = weeklyLimitWarnings
                          )

if __name__ == '__main__':
    app.run(debug = True)