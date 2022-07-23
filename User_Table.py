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
CONTAINER_ID = config.settings['user_container_id']


def login(username, password):
    client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
    db        = client.get_database_client(DATABASE_ID)
    container = db.get_container_client(CONTAINER_ID)

    item_list = container.query_items(
                query='SELECT * FROM User r WHERE r.userName=@userName and r.password=@password',
                parameters=[dict(name="@userName",value=username),dict(name="@password",value=password)],
                enable_cross_partition_query=True)

    return item_list