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

import tab_table
import transaction_table
import item_class
import camper_class
import transaction
import os
import User_Table
import item_table

app = flask.Flask(__name__)
app.secret_key = os.urandom(24)

###########
# ROUTE:   Default
# RENDERS: index.html
###########
@app.route('/', methods=['GET','POST'])
def home():
    try:
        if request.method == 'POST':
            session.pop('user',None)
            loginInfo = User_Table.login(request.form['username'],request.form['password'],  app)
            loggedIn  = False
            for user in loginInfo:
                loggedIn = True
                session['user']      = request.form['username']
                session['user_role'] = user.get('role')
                return redirect(url_for('tabs'))
            if loggedIn == False:
                raise Exception("Could no log in")
    except Exception as e:
        app.logger.critical("Could not Login User")
        return render_template('index.html', loginError = True)

    return render_template('index.html', loginError = False)

###########
# ROUTE:   /logout
# RENDERS: index.html
###########
@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('user',None)
    session.pop('user_role',None)
    return render_template('index.html', loginError = False)

###########
# ROUTE:   /index
# RENDERS: index.html
###########
@app.route('/index', methods=['GET','POST'])
def index():
    try:
        if request.method == 'POST':
            session.pop('user',None)
            loginInfo = User_Table.login(request.form['username'],request.form['password'],  app)
            loggedIn  = False
            for user in loginInfo:
                loggedIn = True
                session['user']      = request.form['username']
                session['user_role'] = user.get('role')
                return redirect(url_for('tabs'))
            if loggedIn == False:
                raise Exception("Could no log in")
    except Exception as e:
        app.logger.critical("Could not Login User")
        return render_template('index.html', loginError = True)

    return render_template('index.html', loginError = False)

###########
# ROUTE:   /add_tab
# REDIRECTS
###########
@app.route('/add_tab', methods=['POST'])
def add_tab():
    if(checkAdminAccess()<0):
        return redirect(url_for('index'))
    
    try:
        c1 = camper_class.camper(app, request)
        tab_table.add_tab(c1 ,app)
    except Exception as e:
        app.logger.critical("[add_tab()] Could not Add a Tab")

    return redirect('/tabs')

###########
# ROUTE:   /edit_tab
# REDIRECTS
###########
@app.route('/edit_tab', methods=['POST'])
def edit_tab():
    if(checkAdminAccess()<0):
        return redirect(url_for('index'))

    try:
        c1 = camper_class.camper(app, request)
        tab_table.edit_tab(c1 ,app)
    except Exception as e:
        app.logger.critical("[edit_tab()] Could not Edit a Tab")

    return redirect(url_for('show_tab'), code=307)

###########
# ROUTE:   /delete_tab
# REDIRECTS
###########
@app.route('/delete_tab', methods=['POST'])
def delete_tab():
    if(checkAdminAccess()<0):
        return redirect(url_for('index'))

    id   = request.form['id']

    try:
        tab_table.delete_tab(id,app)
    except Exception as e:
        app.logger.critical("[delete_tab()] Could not Delete a Tab")

    return redirect('/tabs')

###########
# ROUTE:   /close_tab
# REDIRECTS
###########
@app.route('/close_tab', methods=['POST'])
def close_tab():
    if(checkAdminAccess()<0):
        return redirect(url_for('index'))

    id         = request.form['id']
    close_type = request.form['close_tab_option']

    try:
        tab_table.close_tab(id, close_type, app)
    except Exception as e:
        app.logger.critical("[close_tab()] Could not Close a Tab")

    return redirect(url_for('show_tab'), code=307)

###########
# ROUTE:   /add_transaction
# REDIRECTS
###########
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    if(checkAdminAccess()<0):
        return redirect(url_for('index'))

    try:
        t1 = transaction.transaction(request)
        transaction_table.add_transaction(t1,app)
    except Exception as e:
        app.logger.critical("[add_transaction()] Could not Add a Transaction")

    return redirect(url_for('show_tab'), code=307)

###########
# ROUTE:   /delete_transaction
# REDIRECTS
###########
@app.route('/delete_transaction', methods=['POST'])
def delete_transaction():
    if(checkAdminAccess()<0):
        return redirect(url_for('index'))

    transaction_id  = request.form['transaction_id']

    try:
        transaction_table.delete_transaction(transaction_id,app)
    except Exception as e:
        app.logger.critical("[Delete_transaction()] Could not Delete a Transaction")

    return redirect(url_for('show_tab'), code=307)

###########
# ROUTE:   /tabs
# RENDERS: add_tab.html
###########
@app.route('/tabs', methods=['GET','POST'])
def tabs():
    if(checkAdminAccess()<0):
        return redirect(url_for('index'))

    tabGetError = False
    try:
        tabs = tab_table.get_tabs(app)
    except Exception as e:
        app.logger.critical("[tabs()] Could not Get List of Tabs")
        tabGetError = True

    campers              = []
    churches             = []
    contact_names        = []

    for doc in tabs:
        c1 = camper_class.camper(app,"", doc)
        campers.append(c1)                   

        if (doc.get('home_church') not in churches):
            churches.append(doc.get('home_church'))
        if (doc.get('contact_name') not in contact_names):
            contact_names.append(doc.get('contact_name'))    

    campers.sort(key=lambda x: (x.lname, x.fname))

    return render_template('add_tab.html', 
                           campers       = campers,
                           churhces      = churches,
                           contact_names = contact_names,
                           tabError      = tabGetError
                          )
###########
# ROUTE:   /show_tabs
# RENDERS: show_tab.html
###########
@app.route('/show_tab', methods=['POST','GET'])
def show_tab():
    if(checkAdminAccess()<0):
        return redirect(url_for('index'))

    id           = request.form['id']

    loadError = False
    try:
        tabs         = tab_table.get_tabs(app)
        transactions = transaction_table.get_transactions_for_camper(id,app)
        tab          = tab_table.get_tab(id,app)
        items        = item_table.get_items(app)
    except Exception as e:
        app.logger.critical("[show_tabs()] Error getting Database info")
        loadError = True


    campers               = []
    transactionList       = []
    transactionTotals     = []
    churches              = []
    overLimits            = []
    limitWarnings         = []
    contact_names         = []
    itemList              = []

    counter            = 1
    transactionTotal   = 0


    for snackShackItem in items:
        i1 = item_class.item(snackShackItem)
        itemList.append(i1)

    for doc in tabs:
        c1 = camper_class.camper(app,"", doc)
        campers.append(c1)

        if (doc.get('home_church') not in churches):
            churches.append(doc.get('home_church'))
        if (doc.get('contact_name') not in contact_names):
            contact_names.append(doc.get('contact_name'))   
        

    for doc in transactions:
        limit_warning = False
        limit_over    = False
        transactionAmount = float(doc.get('amount'))
        transactionTotal  = transactionTotal + transactionAmount
        t1 = transaction.transaction("",doc,str(counter))
        transactionList.append(t1)
        transactionTotals.append("${:0,.2f}".format(transactionTotal))
        counter = counter + 1
        if (float(transactionTotal) > tab.get('weeklyLimit')) and (tab.get('noLimit') == False):
            limit_over = True
        elif ((float(transactionTotal) + 5.0) >= tab.get('weeklyLimit')) and (tab.get('noLimit') == False):
             limit_warning = True
        overLimits.append(limit_over)
        limitWarnings.append(limit_warning)

            
    campers.sort(key=lambda x: (x.lname, x.fname))
    currentCamper = camper_class.camper(app,"", tab)
    return render_template('show_tab.html', 
                           campers = campers,
                           currentCamper         = currentCamper,
                           transactionList       = transactionList,
                           transactionTotals     = transactionTotals,
                           overLimits            = overLimits,
                           limitWarnings         = limitWarnings,
                           churches              = churches,
                           contact_names         = contact_names,
                           itemList              = itemList,
                           loadError             = loadError
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