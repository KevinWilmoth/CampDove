import config;
import random;
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey

HOST         = config.settings['host']
MASTER_KEY   = config.settings['master_key']
DATABASE_ID  = config.settings['database_id']
CONTAINER_ID = config.settings['church_container_id']

def add_contact(churchName, churchContactName, churchContactPhone,churchContactEmail):
    client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
    db        = client.get_database_client(DATABASE_ID)
    container = db.get_container_client(CONTAINER_ID)


    item_id       = hash(churchName+churchContactName+churchContactPhone+churchContactEmail+str(random.randint(0,500)))

    church = {'id'             : str(item_id),
              'church_name'    : churchName,
              'contact_name'   : churchContactName,
              'contact_phone'  : churchContactPhone,
              'contact_email'  : churchContactEmail
            }

    container.create_item(body=church)
    return 0

def get_contacts():
    client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
    db        = client.get_database_client(DATABASE_ID)
    container = db.get_container_client(CONTAINER_ID)

    item_list = list(container.read_all_items(max_item_count=100))
    return item_list
