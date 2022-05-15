from pydoc import cli
from pymongo import MongoClient

from app.core.config import settings

default_client = None

def get_client(
    host,
    port,
    username,
    password
):
    return MongoClient(f'mongodb://{username}:{password}@{host}:{port}')

def get_db(
    client:MongoClient,
    db:str
):
    return client.get_database(db)

def get_default_client():
    global default_client
    if default_client is None:
        default_client = get_client(
            settings.MONGODB_HOST,
            settings.MONGODB_PORT,
            settings.MONGO_INITDB_ROOT_USERNAME,
            settings.MONGO_INITDB_ROOT_PASSWORD
        )
    return default_client

def get_default_db():
    global default_client
    if default_client is None:
        get_default_client()
    return get_db(default_client,settings.MONGODB_DB)
