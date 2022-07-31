import config
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
import json
from azure.cosmos.partition_key import PartitionKey

HOST             = config.settings['host']
MASTER_KEY       = config.settings['master_key']
DATABASE_ID      = config.settings['database_id']

def create_table(table_name):
        client    = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
        db        = client.get_database_client(DATABASE_ID)
        container = db.create_container_if_not_exists(
                    id=table_name, 
                    partition_key=PartitionKey(path='/id', kind='Hash'),
                    )

        return container

def add_items(container, items):
    for i in items:
        try:
            container.create_item(body=i)
            print("ADDED Item i [" + str(i) + "]!")
        except Exception as e:
            print("DID NOT ADD Item i [" + str(i) + "]")
    
    return

if __name__ == '__main__':
    itemContainerName         = config.settings['item_container_id' ]
    userContainerName         = config.settings['user_container_id' ]
    tabContainerName          = config.settings['tab_container_id']
    transactionContainerName  = config.settings['transaction_container_id']

    itemContainer        = create_table(itemContainerName)
    userContainer        = create_table(userContainerName)
    tabContainer         = create_table(tabContainerName)
    transactionContainer = create_table(transactionContainerName)

    f       = open('artifacts/DB_Records.json')
    dbItems = json.load(f)
    f.close()

    add_items(itemContainer, dbItems['SnackShackItems'])

    exit(0)