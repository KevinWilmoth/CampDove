import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://campdovetest.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY'),
    'my_test': os.environ.get('MY_TEST'),
    'database_id': os.environ.get('COSMOS_DATABASE', 'CampDoveTest'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'Person'),
    'base_url' : os.environ.get('BASE_URL', 'http://localhost:5000/'),
}