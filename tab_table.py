import config;
import random;
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
from flask import Flask

HOST         = config.settings['host']
MASTER_KEY   = config.settings['master_key']
DATABASE_ID  = config.settings['database_id']
CONTAINER_ID = config.settings['tab_container_id']

def add_tab(camperFirstName, camperLastName, homeChurch, contactName, workerName, weeklyLimit, prepaid, noLimit,app):
    client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
    db        = client.get_database_client(DATABASE_ID)
    container = db.get_container_client(CONTAINER_ID)
    
    noLimitBoolean = noLimit=='True'

    app.logger.info('tab_table.add_tab noLimit = [' + noLimit + ']')
    app.logger.info('tab_table.add_tab boolean noLimit = [' + str(noLimitBoolean) + ']')

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

    container.create_item(body=tab)
    return 0

def get_tabs():
    client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
    db        = client.get_database_client(DATABASE_ID)
    container = db.get_container_client(CONTAINER_ID)

    item_list = list(container.read_all_items(max_item_count=100))
    return item_list

def get_tab(id):
    client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
    db        = client.get_database_client(DATABASE_ID)
    container = db.get_container_client(CONTAINER_ID)

    return container.read_item(item=id, partition_key=id)

def delete_tab(id):
    client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
    db        = client.get_database_client(DATABASE_ID)
    container = db.get_container_client(CONTAINER_ID)

    container.delete_item(item=id, partition_key=id)
    return 0
