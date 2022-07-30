import config;
import random;
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
from flask import Flask
from datetime import datetime
import traceback

HOST         = config.settings['host']
MASTER_KEY   = config.settings['master_key']
DATABASE_ID  = config.settings['database_id']
CONTAINER_ID = config.settings['user_container_id']


def login(username, password, app):
    try:
        client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
        db        = client.get_database_client(DATABASE_ID)
        container = db.get_container_client(CONTAINER_ID)
    except Exception as e:
        app.logger.critical("[user_table.login()] Error opening container [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        app.logger.critical(traceback.format_exc)
        raise

    try:
        item_list = container.query_items(
                    query='SELECT * FROM User r WHERE r.userName=@userName and r.password=@password',
                    parameters=[dict(name="@userName",value=username),dict(name="@password",value=password)],
                    enable_cross_partition_query=True)
    except Exception as e:
        app.logger.critical("[user_table.login()] Error querying container [" + CONTAINER_ID + "] in database [" + DATABASE_ID +"]")
        app.logger.critical(traceback.format_exc)
        raise   

    return item_list