import config;
import random;
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
from flask import Flask
from datetime import datetime

HOST         = config.settings['host']
MASTER_KEY   = config.settings['master_key']
DATABASE_ID  = config.settings['database_id']
CONTAINER_ID = config.settings['transaction_container_id']

def dayNameFromWeekday(weekday):
    if weekday == 0:
        return "Monday"
    if weekday == 1:
        return "Tuesday"
    if weekday == 2:
        return "Wednesday"
    if weekday == 3:
        return "Thursday"
    if weekday == 4:
        return "Friday"
    if weekday == 5:
        return "Saturday"
    if weekday == 6:
        return "Sunday"

def add_transaction(camperId, transactionAmount):
    client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
    db        = client.get_database_client(DATABASE_ID)
    container = db.get_container_client(CONTAINER_ID)


    item_id   = hash(camperId + transactionAmount + str(datetime.now()))
    dayofWeek = dayNameFromWeekday(datetime.today().weekday())

    transaction = { 'id'          : str(item_id),
                    'day_of_week' : dayofWeek,
                    'amount'      : float(transactionAmount),
                    'camper_id'   : camperId
                  }

    container.create_item(body=transaction)
    return 0

def get_transactions_for_camper(camperId, app):
    client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
    db        = client.get_database_client(DATABASE_ID)
    container = db.get_container_client(CONTAINER_ID)

    item_list = container.query_items(
                query='SELECT * FROM Transaction r WHERE r.camper_id=@camper_id',
                parameters=[{ "name":"@camper_id", "value": camperId }],
                enable_cross_partition_query=True)

    app.logger.info('get_transactions_for_camper camper = [' + camperId + ']')
    return item_list

def get_transactions():
    client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
    db        = client.get_database_client(DATABASE_ID)
    container = db.get_container_client(CONTAINER_ID)

    item_list = list(container.read_all_items(max_item_count=100))
    return item_list

def delete_transaction(id):
    client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
    db        = client.get_database_client(DATABASE_ID)
    container = db.get_container_client(CONTAINER_ID)

    container.delete_item(item=id, partition_key=id)
    return 0

