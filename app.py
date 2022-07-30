import flask
from flask import request, render_template
from flask import redirect
from flask import url_for
from flask import session
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import datetime

import config
import tab_table
import transaction_table
import camper_class
import os
import User_Table
import item_table

app = flask.Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        session.pop('user',None)
        loginInfo = User_Table.login(request.form['username'],request.form['password'])
        for user in loginInfo:
            session['user']      = request.form['username']
            session['user_role'] = user.get('role')
            return redirect(url_for('tabs'))

    return render_template('index.html')

@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('user',None)
    session.pop('user_role',None)
    return render_template('index.html')

@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        session.pop('user',None)
        session.pop('user_role',None)
        if request.form['password'] == 'password':
            session['user'] = request.form['username']
            return redirect(url_for('tabs'))

    return render_template('index.html')

@app.route('/add_tab', methods=['POST'])
def add_tab():
    if(checkAdminAccess()<0):
        return redirect(url_for('index'))

    #Required Fields
    camper_lname   = request.form['camper_last_name']
    worker_name    = request.form['worker_name']

    #Optional Fields
    camper_fname   = ""
    if 'camper_first_name' in request.form:
        camper_fname   = request.form['camper_first_name']

    church_name   = ""
    if "church" in request.form:
        church_name    = request.form['church']

    contact_name   = ""
    if "contact_name" in request.form:
        contact_name    = request.form['contact_name']  

    no_limit       = 'False'    
    if "no_limit" in request.form:
        no_limit = 'True'
    
    if 'weekly_limit' not in request.form:
        weekly_limit = '0.0'
    elif request.form['weekly_limit']=='':
        weekly_limit = '0.0'
    else:
        weekly_limit   = request.form['weekly_limit']

    if 'prepaid_amount' not in request.form:
        prepaid_amount = '0.0'
    elif request.form['prepaid_amount']=='':
        prepaid_amount = '0.0'
    else:
        prepaid_amount = request.form['prepaid_amount']
        

    app.logger.info('prepaid_amount = [' + prepaid_amount + ']')
    app.logger.info('weekly_limit = [' + weekly_limit + ']')

    tab_table.add_tab(camper_fname, camper_lname, church_name, contact_name, worker_name, weekly_limit, prepaid_amount, no_limit,app)

    return redirect('/tabs')

@app.route('/edit_tab', methods=['POST'])
def edit_tab():
    if(checkAdminAccess()<0):
        return redirect(url_for('index'))

    camper_fname   = request.form['camper_first_name']
    camper_lname   = request.form['camper_last_name']
    church_name    = request.form['church']
    contact_name   = request.form['contact_name']
    worker_name    = request.form['worker_name']
    id             = request.form['id']
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

    tab_table.edit_tab(camper_fname, camper_lname, church_name, contact_name, worker_name, weekly_limit, prepaid_amount, no_limit,app,id)

    return redirect(url_for('show_tab'), code=307)

@app.route('/delete_tab', methods=['POST'])
def delete_tab():
    if(checkAdminAccess()<0):
        return redirect(url_for('index'))

    id   = request.form['id']

    app.logger.info('app.delete_tab id = [' + id + ']')

    tab_table.delete_tab(id,app)

    return redirect('/tabs')

@app.route('/close_tab', methods=['POST'])
def close_tab():
    checkAdminAccess()

    id         = request.form['id']
    close_type = request.form['close_tab_option']
    app.logger.info('close tab option = [' + close_type + ']')    

    tab_table.close_tab(id, close_type, app)

    return redirect(url_for('show_tab'), code=307)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    if(checkAdminAccess()<0):
        return redirect(url_for('index'))

    id     = request.form['id']
    amount = request.form['transaction_amount']
    transaction_table.add_transaction(id,amount,app)

    return redirect(url_for('show_tab'), code=307)

@app.route('/delete_transaction', methods=['POST'])
def delete_transaction():
    if(checkAdminAccess()<0):
        return redirect(url_for('index'))

    transaction_id  = request.form['transaction_id']
    transaction_table.delete_transaction(transaction_id,app)

    return redirect(url_for('show_tab'), code=307)

@app.route('/tabs', methods=['GET','POST'])
def tabs():
    if(checkAdminAccess()<0):
        return redirect(url_for('index'))

    if 'user_role' not in session:
        return redirect(url_for('index'))

    if session['user_role'] != 'SnackShackAdmin':
        app.logger.info('Incorrect Role!')
        return redirect(url_for('index'))

    tabs = tab_table.get_tabs(app)
    campers              = []
    churches             = []
    contact_names        = []

    for doc in tabs:
        TabClosed     = False
        if (doc.get("closed_status") in ["Refund", "PaidInFull", "Donation"]):
            TabClosed = True
        c1 = camper_class.camper(doc.get('camper_first_name'),
                                doc.get('camper_last_name'),
                                doc.get('home_church'),
                                doc.get('contact_name'),
                                doc.get('workerName'),
                                doc.get('noLimit'),
                                doc.get('weeklyLimit'),
                                doc.get('dailyLimit'),
                                doc.get('prepaid'),
                                TabClosed,
                                doc.get('id')
                   )
        if (doc.get('home_church') not in churches):
            churches.append(doc.get('home_church'))
        if (doc.get('contact_name') not in contact_names):
            contact_names.append(doc.get('contact_name'))    
        campers.append(c1)

    campers.sort(key=lambda x: (x.lname, x.fname))

    return render_template('add_tab.html', 
                           campers       = campers,
                           churhces      = churches,
                           contact_names = contact_names
                          )

@app.route('/show_tab', methods=['POST','GET'])
def show_tab():
    if(checkAdminAccess()<0):
        return redirect(url_for('index'))

    tabs = tab_table.get_tabs(app)
    campers              = []

    id           = request.form['id']
    transactions = transaction_table.get_transactions_for_camper(id,app)
    tab          = tab_table.get_tab(id,app)
    items        = item_table.get_items()

    transactionDays       = []
    transactionAmounts    = []
    transactionNumbers    = []
    transactionTotals     = []
    transactionIds        = []
    churches              = []
    overLimits            = []
    limitWarnings         = []
    contact_names         = []
    item_descs            = []
    item_prices           = []
    item_prices_formatted = []

    tab_closed          = tab.get("closed_status") in ["Refund", "PaidInFull", "Donation"]
    app.logger.info('close tab closed = [' + str(tab_closed) + ']')

    counter            = 1
    transactionTotal   = 0


    for snackShackItem in items:
        item_descs.append(snackShackItem.get("description"))
        item_prices.append(snackShackItem.get("price"))
        item_prices_formatted.append("${:0,.2f}".format(snackShackItem.get('price')))

    for doc in tabs:
        TabClosed     = False
        if (doc.get("closed_status") in ["Refund", "PaidInFull", "Donation"]):
            TabClosed = True
        c1 = camper_class.camper(doc.get('camper_first_name'),
                                doc.get('camper_last_name'),
                                doc.get('home_church'),
                                doc.get('contact_name'),
                                doc.get('workerName'),
                                doc.get('noLimit'),
                                doc.get('weeklyLimit'),
                                doc.get('dailyLimit'),
                                doc.get('prepaid'),
                                TabClosed,
                                doc.get('id')
                   )
        if (doc.get('home_church') not in churches):
            churches.append(doc.get('home_church'))
        if (doc.get('contact_name') not in contact_names):
            contact_names.append(doc.get('contact_name'))   
        campers.append(c1)

    for transaction in transactions:
        limit_warning = False
        limit_over    = False
        transactionAmount = float(transaction.get('amount'))
        transactionTotal  = transactionTotal + transactionAmount
        transactionDays.append(transaction.get('day_of_week'))
        transactionAmounts.append("${:0,.2f}".format(transactionAmount))
        transactionIds.append(transaction.get('id'))
        transactionNumbers.append(str(counter))
        transactionTotals.append("${:0,.2f}".format(transactionTotal))
        counter = counter + 1
        if (float(transactionTotal) > tab.get('weeklyLimit')) and (tab.get('noLimit') == False):
            limit_over = True
        elif ((float(transactionTotal) + 5.0) >= tab.get('weeklyLimit')) and (tab.get('noLimit') == False):
             limit_warning = True
        overLimits.append(limit_over)
        limitWarnings.append(limit_warning)

            
    campers.sort(key=lambda x: (x.lname, x.fname))

    return render_template('show_tab.html', 
                           campers = campers,
                           camperFirstName       = tab.get('camper_first_name'),
                           camperLastName        = tab.get('camper_last_name'), 
                           NoLimit               = tab.get('noLimit'),
                           homeChurch            = tab.get('home_church'),
                           dailyLimit            = "${:0,.2f}".format(tab.get('dailyLimit')),
                           contactName           = tab.get('contact_name'),
                           weeklyLimit           = "${:0,.2f}".format(tab.get('weeklyLimit')),
                           weeklyLimitNum        = tab.get('weeklyLimit'),
                           prepaidAmountNum      = tab.get('prepaid'),
                           workerName            = tab.get('workerName'),
                           id                    = tab.get('id'),
                           prepaidAmount         = "${:0,.2f}".format(tab.get('prepaid')),
                           transactionDays       = transactionDays,
                           transactionAmounts    = transactionAmounts,
                           transactionNumbers    = transactionNumbers,
                           transactionTotals     = transactionTotals,
                           transactionIds        = transactionIds,
                           overLimits            = overLimits,
                           limitWarnings         = limitWarnings,
                           churches              = churches,
                           contact_names         = contact_names,
                           tab_not_closed        = not tab_closed,
                           tab_closed            = tab_closed,
                           item_descs            = item_descs,
                           item_prices           = item_prices,
                           item_prices_formatted = item_prices_formatted
                          )

def checkAdminAccess():
    if 'user_role' not in session:
        app.logger.info('Not Logged In!')
        return -1

    if session['user_role'] != 'SnackShackAdmin':
        app.logger.info('Incorrect Role!')
        return -1
    
    app.logger.info('Logged In!')
    
    return 1

if __name__ == '__main__':
    app.run(debug = True)