import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://campdovetest.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', 'HajZBVXsgUWh1mLOQ8Ta5JNKOGo6OVl464NuYYwJizPZb3wbEryvdSPK7Nd03wbNp3SDlvujc6SflDjGeeJ3xw=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'CampDoveTest'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'Person'),
}