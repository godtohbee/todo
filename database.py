import os
from pymongo import mongo_client
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure

load_dotenv()

MONGO_DB_CONNECTION_URI = os.environ.get('MONGO_DB_CONNECTION_URI')

try:
    client = mongo_client.MongoClient(MONGO_DB_CONNECTION_URI)
    client.admin.command('ismaster')
    print("MongoDB connection successful")
except ConnectionFailure:
    print("MongoDB connection failed")
    raise

user_collection = client["todoapp"]["users"]
todo_collection = client["todoapp"]["todo"]

