import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://campdovetest.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY'),
    'creator_key': os.environ.get('CAMP_DOVE_MASTER_KEY'),
    'my_test': os.environ.get('MY_TEST'),
    'database_id': os.environ.get('COSMOS_DATABASE', 'CampDoveTest'),
    'item_container_id': os.environ.get('ITEM_COSMOS_CONTAINER', 'SnackShackItem'),
    'user_container_id': os.environ.get('USER_COSMOS_CONTAINER', 'User'),
    'tab_container_id': os.environ.get('TAB_COSMOS_CONTAINER', 'Tab'),
    'transaction_container_id': os.environ.get('TRANSACTION_COSMOS_CONTAINER', 'Transaction'),
    'base_url' : os.environ.get('BASE_URL', 'http://localhost:5000/'),
}