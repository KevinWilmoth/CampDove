import config;
import random;
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
from flask import Flask
from datetime import datetime
import traceback

HOST             = config.settings['host']
MASTER_KEY       = config.settings['master_key']
DATABASE_ID      = config.settings['database_id']
CONTAINER_ID     = config.settings['transaction_container_id']
MAX_RETURN_ITEMS = config.settings["max_return_items"]

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

def add_transaction(newTransaction, app):
    try:
        client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
        db        = client.get_database_client(DATABASE_ID)
        container = db.get_container_client(CONTAINER_ID)
    except Exception as e:
        app.logger.critical("[transaction_table.add_transaction()] Error opening container [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        app.logger.critical(traceback.format_exc)
        raise

    doc = { 'id'          : newTransaction.id,
            'day_of_week' : newTransaction.dayofWeek,
            'amount'      : newTransaction.amount,
            'camper_id'   : newTransaction.camperId
          }

    try:
        container.create_item(body=doc)
    except e:
        app.logger.critical("[transaction_table.add_transaction()] Error adding transaction to container [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        raise

    return 0

def get_transactions_for_camper(camperId, app):
    try:
        client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
        db        = client.get_database_client(DATABASE_ID)
        container = db.get_container_client(CONTAINER_ID)
    except Exception as e:
        app.logger.critical("[transaction_table.get_transactions_for_camper()] Error opening container [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        app.logger.critical(traceback.format_exc)
        raise

    try:
        item_list = container.query_items(
                    query='SELECT * FROM Transaction r WHERE r.camper_id=@camper_id',
                    parameters=[{ "name":"@camper_id", "value": camperId }],
                    enable_cross_partition_query=True)
    except e:
        app.logger.critical("[transaction_table.get_transactions_for_camper()] Error finding transaction in container [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        app.logger.critical(traceback.format_exc)
        raise       

    return item_list

def delete_transaction(id, app):
    try:
        client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
        db        = client.get_database_client(DATABASE_ID)
        container = db.get_container_client(CONTAINER_ID)
    except Exception as e:
        app.logger.critical("[transaction_table.delete_transaction()] Error opening container [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        app.logger.critical(traceback.format_exc)
        raise

    try:
        container.delete_item(item=id, partition_key=id)
    except e:
        app.logger.critical("[transaction_table.delete_transaction()] Error deleting transaction in container [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        app.logger.critical(traceback.format_exc)
        raise   

    return 0

