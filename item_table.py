import config;
import random;
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
from flask import Flask
import traceback

HOST         = config.settings['host']
MASTER_KEY   = config.settings['master_key']
DATABASE_ID  = config.settings['database_id']
CONTAINER_ID = config.settings['item_container_id']

def get_items(app):
    try:
        client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
        db        = client.get_database_client(DATABASE_ID)
        container = db.get_container_client(CONTAINER_ID)
    except Exception as e:
        app.logger.critical("[item_table.add_items()] Error opening container [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        app.logger.critical(traceback.format_exc)
        raise

    try:
        item_list = list(container.read_all_items(max_item_count=100))
    except Exception as e:
        app.logger.critical("[item_table.add_items()] Error querying container [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        app.logger.critical(traceback.format_exc)
        raise

    return item_list

