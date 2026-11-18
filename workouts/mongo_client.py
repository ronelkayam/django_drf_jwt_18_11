import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class MongoConnection:
    _client = None
    _db = None

    @classmethod
    def get_db(cls):
        if cls._client is None:
            mongo_uri = os.getenv('MONGO_URI',"mongodb://localhost:27017")
            db_name = os.getenv('MONGO_DB',"gym_drf_logs")
            cls._client = MongoClient(mongo_uri)
            cls._db = cls._client[db_name]
        return cls._db

def get_audit_collection():
    db = MongoConnection.get_db()
    return db["activity_logs"]
