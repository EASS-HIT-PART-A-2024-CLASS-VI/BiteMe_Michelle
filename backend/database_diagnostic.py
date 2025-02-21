from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB URI
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "BiteMeDB")

def check_database_contents():
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        
        # Select database
        db = client[DATABASE_NAME]
        
        # Check collections
        print("Collections in the database:")
        collections = db.list_collection_names()
        for collection in collections:
            print(f"\n{collection.upper()} Collection:")
            
            # Count documents
            count = db[collection].count_documents({})
            print(f"Total documents: {count}")
            
            # If collection has documents, print first few
            if count > 0:
                print("Sample documents:")
                for doc in db[collection].find().limit(3):
                    print(doc)
    
    except Exception as e:
        print(f"Error checking database: {e}")

if __name__ == "__main__":
    check_database_contents()
