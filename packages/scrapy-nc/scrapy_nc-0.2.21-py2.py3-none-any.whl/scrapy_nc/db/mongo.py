import os
from pymongo import MongoClient
import time

MONGO_HOST = os.environ.get('CRAWLAB_MONGO_HOST')
MONGO_PORT = int(os.environ.get('CRAWLAB_MONGO_PORT', '27017'))
MONGO_DB = os.environ.get('CRAWLAB_MONGO_DB')
MONGO_USERNAME = os.environ.get('CRAWLAB_MONGO_USERNAME')
MONGO_PASSWORD = os.environ.get('CRAWLAB_MONGO_PASSWORD')
MONGO_AUTHSOURCE = os.environ.get('CRAWLAB_MONGO_AUTHSOURCE')

mongo_client = MongoClient(
    host=MONGO_HOST,
    port=MONGO_PORT,
    username=MONGO_USERNAME,
    password=MONGO_PASSWORD,
    authSource=MONGO_AUTHSOURCE,
) if MONGO_HOST else None

mongo_db = mongo_client.get_database(MONGO_DB) if mongo_client else None

refresh_time = {}


def refresh_session(session):
    id = session.session_id.get('id')
    last_refresh_time = refresh_time.get(id)
    if last_refresh_time is not None and time.time() - last_refresh_time < 180:
        print(f'last refresh time too short, ignore refresh request ')
        return
    mongo_db.command("refreshSessions", [{'id': id}])
    print(f'refresh session success: {id}')
    refresh_time[id] = time.time()
