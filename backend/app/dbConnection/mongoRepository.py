from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# MongoDB connection details
MONGO_URI = os.getenv("MONGO_URI", "")
DATABASE_NAME = os.getenv("DATABASE_NAME", "BiteMeDB")

def get_mongo_client():
    """
    Establish a connection to the MongoDB server.
    Returns:
        MongoClient: The MongoDB client instance.
    Raises:
        ConnectionFailure: If the connection to MongoDB fails.
    """
    try:
        client = MongoClient(MONGO_URI)
        client.admin.command('ping')  # Verify connection
        return client
    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

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
    try:
        db = get_database()
        collection = db[collection_name]
        result = collection.insert_one(item)
        return result
    except Exception as e:
        logger.error(f"Error inserting item into {collection_name}: {e}")
        raise

def find_all(collection_name, filter=None):
    """
    Retrieve all documents from the specified collection that match the filter.
    Args:
        collection_name (str): The name of the collection.
        filter (dict): The filter criteria (default is None for all documents).
    Returns:
        list: A list of matching documents.
    """
    try:
        db = get_database()
        collection = db[collection_name]
        documents = list(collection.find(filter or {}, {"_id": 0}))
        return documents
    except Exception as e:
        logger.error(f"Error retrieving documents from {collection_name}: {e}")
        raise

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
    try:
        db = get_database()
        collection = db[collection_name]
        result = collection.update_one(filter, {"$set": update})
        return result
    except Exception as e:
        logger.error(f"Error updating item in {collection_name}: {e}")
        raise

def delete_item(collection_name, filter):
    """
    Delete a single document from the specified collection.
    Args:
        collection_name (str): The name of the collection.
        filter (dict): The filter criteria to find the document.
    Returns:
        DeleteResult: The result of the delete operation.
    """
    try:
        db = get_database()
        collection = db[collection_name]
        result = collection.delete_one(filter)
        return result
    except Exception as e:
        logger.error(f"Error deleting item from {collection_name}: {e}")
        raise