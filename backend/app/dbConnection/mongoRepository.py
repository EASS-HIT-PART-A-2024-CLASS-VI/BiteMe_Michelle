from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MongoDB connection details
MONGO_URI = os.getenv("MONGO_URI")  # Fetch URI from .env
DATABASE_NAME = "BiteMeDB"  # Change this to your actual database name

def get_mongo_client():
    """
    Establish a connection to the MongoDB server.
    Returns:
        MongoClient: The MongoDB client instance.
    Raises:
        ConnectionFailure: If the connection to MongoDB fails.
    """
    try:
        print(f"Connecting to MongoDB with URI: {MONGO_URI}")  # Debug log
        client = MongoClient(MONGO_URI)
        client.admin.command('ping')  # Ensure the connection is successful
        print("Connected to MongoDB")  # Debug log
        return client
    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise ConnectionFailure(f"Failed to connect to MongoDB: {e}")

def get_database():
    """
    Retrieve the MongoDB database instance.
    Returns:
        Database: The MongoDB database instance.
    """
    client = get_mongo_client()
    return client[DATABASE_NAME]

def insert_item(collection_name, item):
    """
    Insert a single document into the specified collection.
    Args:
        collection_name (str): The name of the collection.
        item (dict): The document to insert.
    Returns:
        InsertOneResult: The result of the insert operation.
    """
    db = get_database()
    collection = db[collection_name]
    result = collection.insert_one(item)
    print(f"Inserted item into {collection_name}: {item}")
    return result

def find_all(collection_name, filter=None):
    """
    Retrieve all documents from the specified collection that match the filter.
    Args:
        collection_name (str): The name of the collection.
        filter (dict): The filter criteria (default is None for all documents).
    Returns:
        list: A list of matching documents.
    """
    db = get_database()
    collection = db[collection_name]
    documents = list(collection.find(filter or {}, {"_id": 0}))  # Exclude the `_id` field
    print(f"Retrieved documents from {collection_name}: {documents}")
    return documents

def update_item(collection_name, filter, update):
    """
    Update a single document in the specified collection.
    Args:
        collection_name (str): The name of the collection.
        filter (dict): The filter criteria to find the document.
        update (dict): The update to apply.
    Returns:
        UpdateResult: The result of the update operation.
    """
    db = get_database()
    collection = db[collection_name]
    result = collection.update_one(filter, {"$set": update})
    print(f"Updated item in {collection_name} where {filter}: {update}")
    return result

def delete_item(collection_name, filter):
    """
    Delete a single document from the specified collection.
    Args:
        collection_name (str): The name of the collection.
        filter (dict): The filter criteria to find the document.
    Returns:
        DeleteResult: The result of the delete operation.
    """
    db = get_database()
    collection = db[collection_name]
    result = collection.delete_one(filter)
    print(f"Deleted item from {collection_name} where {filter}")
    return result
