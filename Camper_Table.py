import config;
import random;
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey

HOST         = config.settings['host']
MASTER_KEY   = config.settings['master_key']
DATABASE_ID  = config.settings['database_id']
CONTAINER_ID = config.settings['camper_container_id']

def add_camper(camperFirstName, camperLastName, contact, churchId):
    client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
    db        = client.get_database_client(DATABASE_ID)
    container = db.get_container_client(CONTAINER_ID)


    item_id       = hash(camperFirstName+camperLastName+churchId+contact+str(random.randint(0,500)))

    camper = {'id'                : str(item_id),
              'camper_first_name' : camperFirstName,
              'camper_last_name'  : camperLastName,
              'contact_name'      : contact,
              'church_id'         : churchId,
             }

    container.create_item(body=camper)
    return 0

def get_campers():
    client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
    db        = client.get_database_client(DATABASE_ID)
    container = db.get_container_client(CONTAINER_ID)

    item_list = list(container.read_all_items(max_item_count=100))
    return item_list
