import config;
import random;
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
from flask import Flask
import traceback

HOST             = config.settings['host']
MASTER_KEY       = config.settings['master_key']
DATABASE_ID      = config.settings['database_id']
CONTAINER_ID     = config.settings['tab_container_id']
MAX_RETURN_ITEMS = config.settings["max_return_items"]

def add_tab(camperFirstName, camperLastName, homeChurch, contactName, workerName, weeklyLimit, prepaid, noLimit,app):
    try:
        client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
        db        = client.get_database_client(DATABASE_ID)
        container = db.get_container_client(CONTAINER_ID)
    except Exception as e:
        app.logger.critical("[tab_table.add_tab()] Error opening container [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        app.logger.critical(traceback.format_exc)
        raise
        
    
    noLimitBoolean = noLimit=='True'

    if noLimitBoolean==True:
        dailyLimit = 0.0
        weeklyLimit = 0.0
    elif float(prepaid) > float(weeklyLimit):
        dailyLimit = float(prepaid) / 4
    elif float(weeklyLimit) > 0:
        dailyLimit = float(weeklyLimit) / 4      
    else:
        dailyLimit = 0.0

    item_id       = hash(camperFirstName+camperLastName+homeChurch+contactName+workerName+str(weeklyLimit)+str(prepaid)+str(noLimit)+str(random.randint(0,500)))

    tab = {'id'                : str(item_id),
           'camper_first_name' : camperFirstName,
           'camper_last_name'  : camperLastName,
           'home_church'       : homeChurch,
           'contact_name'      : contactName,
           'workerName'        : workerName,
           'weeklyLimit'       : float(weeklyLimit),
           'dailyLimit'        : float(dailyLimit),
           'prepaid'           : float(prepaid),
           'noLimit'           : noLimitBoolean
        }

    try:
        container.create_item(body=tab)
    except Exception as e:
        app.logger.critical("[tab_table.add_tab()] Error adding camper to container [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        app.logger.critical(traceback.format_exc)
        raise     

    return 0

def edit_tab(camperFirstName, camperLastName, homeChurch, contactName, workerName, weeklyLimit, prepaid, noLimit,app, id):
    try:
        client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
        db        = client.get_database_client(DATABASE_ID)
        container = db.get_container_client(CONTAINER_ID)
    except Exception as e:
        app.logger.critical("[tab_table.edit_tab()] Error opening container [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        app.logger.critical(traceback.format_exc)
        raise
    
    noLimitBoolean = noLimit=='True'

    if noLimitBoolean==True:
        dailyLimit = 0.0
        weeklyLimit = 0.0
    elif float(prepaid) > float(weeklyLimit):
        dailyLimit = float(prepaid) / 4
    elif float(weeklyLimit) > 0:
        dailyLimit = float(weeklyLimit) / 4      
    else:
        dailyLimit = 0.0

    try:
        doc = container.read_item(item=id, partition_key=id)
    except Exception as e:
        app.logger.critical("[tab_table.edit_tab()] Error reading tab in container [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        app.logger.critical(traceback.format_exc)
        raise

    doc['camper_first_name'] = camperFirstName
    doc['camper_last_name']  = camperLastName
    doc['home_church']       = homeChurch
    doc['contact_name']      = contactName
    doc['workerName']        = workerName
    doc['weeklyLimit']       = float(weeklyLimit)
    doc['dailyLimit']        = float(dailyLimit)
    doc['prepaid']           = float(prepaid)
    doc['noLimit']           = noLimitBoolean

    try:
        container.replace_item(item=doc, body=doc)
    except Exception as e:
        app.logger.critical("[tab_table.edit_tab()] Error updating tab in container [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        app.logger.critical(traceback.format_exc)
        raise

    return 0

def get_tabs(app):
    try:
        client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
        db        = client.get_database_client(DATABASE_ID)
        container = db.get_container_client(CONTAINER_ID)
    except Exception as e:
        app.logger.critical("[tab_table.get_tabs()] Error opening container [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        app.logger.critical(traceback.format_exc)
        raise
    
    try:
        item_list = list(container.read_all_items(max_item_count=MAX_RETURN_ITEMS))
    except Exception as e:
        app.logger.critical("[tab_table.get_tabs()] Error retrieving tabs [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        app.logger.critical(traceback.format_exc)
        raise

    return item_list

def get_tab(id,app):
    try:
        client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
        db        = client.get_database_client(DATABASE_ID)
        container = db.get_container_client(CONTAINER_ID)
    except Exception as e:
        app.logger.critical("[tab_table.get_tab()] Error opening container [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        app.logger.critical(traceback.format_exc)
        raise

    try:
        item = container.read_item(item=id, partition_key=id)
    except Exception as e:
        app.logger.critical("[tab_table.get_tab()] Error reading item from  [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        app.logger.critical(traceback.format_exc)
        raise

    return item

def close_tab(id, close_type, app):
    try:
        client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
        db        = client.get_database_client(DATABASE_ID)
        container = db.get_container_client(CONTAINER_ID)
    except Exception as e:
        app.logger.critical("[tab_table.close_tab()] Error opening container [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        app.logger.critical(traceback.format_exc)
        raise

    try:
        doc                   = container.read_item(item=id, partition_key=id)
        doc['closed_status']  = close_type
    except Exception as e:
        app.logger.critical("[tab_table.close_tab()] Error retrieving tab from container [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        app.logger.critical(traceback.format_exc)
        raise     

    try:
        container.replace_item(item=doc, body=doc)
    except Exception as e:
        app.logger.critical("[tab_table.close_tab()] Error closing tab in container [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        app.logger.critical(traceback.format_exc)
        raise       

    return 0

def delete_tab(id, app):
    try:
        client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
        db        = client.get_database_client(DATABASE_ID)
        container = db.get_container_client(CONTAINER_ID)
    except Exception as e:
        app.logger.critical("[tab_table.delete_tab()] Error opening container [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        app.logger.critical(traceback.format_exc)
        raise

    try:
        container.delete_item(item=id, partition_key=id)
    except Exception as e:
        app.logger.critical("[tab_table.delete_tab()] Error deleting tab from container [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        app.logger.critical(traceback.format_exc)
        raise 

    return 0
