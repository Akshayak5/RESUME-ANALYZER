from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

load_dotenv()

_client = None
_db = None


def init_db():
    global _client, _db
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    db_name = os.getenv("DB_NAME", "resume_analyzer_db")
    try:
        _client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        _client.admin.command("ping")
        _db = _client[db_name]
        print(f"[DB] Connected to MongoDB: {db_name}")
        _create_indexes()
    except ConnectionFailure as e:
        print(f"[DB] MongoDB connection failed: {e}")
        raise


def get_db():
    global _db
    if _db is None:
        init_db()
    return _db


def _create_indexes():
    db = _db
    db.users.create_index("email", unique=True)
    db.resumes.create_index("user_id")
    db.resumes.create_index("created_at")
    db.skill_verifications.create_index([("user_id", 1), ("skill", 1)])
    print("[DB] Indexes created")
