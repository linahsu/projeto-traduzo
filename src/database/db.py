from pymongo import MongoClient
from os import environ, getenv

client = MongoClient(environ.get("MONGO_URI", "mongodb://localhost:27017"))

db = client[getenv("DB_NAME", "test_db_traduzo")]