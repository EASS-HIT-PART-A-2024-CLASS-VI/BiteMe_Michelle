import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

def detailed_mongodb_connection_test():
    # Explicitly load .env file
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(env_path)

    # Get MongoDB URI with detailed logging
    mongo_uri = os.getenv("MONGO_URI")
    
    print("🔍 Detailed MongoDB Connection Diagnostic")
    print("=" * 50)
    
    # Validate URI
    if not mongo_uri:
        print("❌ ERROR: MONGO_URI is not set in environment variables")
        return

    # Mask sensitive parts of the URI
    masked_uri = mongo_uri.split('@')[0][:20] + "...@" + mongo_uri.split('@')[1][:30]
    print(f"📡 Connection URI (masked): {masked_uri}")

    try:
        # Create client with verbose options
        client = MongoClient(
            mongo_uri, 
            server_api=ServerApi('1'),
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=5000,          # 5 second connection timeout
            socketTimeoutMS=5000            # 5 second socket timeout
        )

        # Test connection with ping
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!")

        # Get database
        db_name = os.getenv("DATABASE_NAME", "BiteMeDB")
        db = client[db_name]
        
        print(f"\n📊 Database Details:")
        print(f"Database Name: {db_name}")
        
        # List collections
        collections = db.list_collection_names()
        print("\n🗃️ Collections:")
        if not collections:
            print("❗ No collections found in the database")
        else:
            for collection in collections:
                # Count documents in each collection
                count = db[collection].count_documents({})
                print(f"- {collection}: {count} documents")
                
                # If collection has documents, print a sample
                if count > 0:
                    print("  Sample document:")
                    sample = db[collection].find_one()
                    for key, value in sample.items():
                        print(f"    {key}: {value}")

    except Exception as e:
        print(f"❌ Connection Error: {type(e).__name__}")
        print(f"Error Details: {str(e)}")
        
        # More detailed error analysis
        print("\n🕵️ Potential Connection Issues:")
        error_msg = str(e).lower()
        if "authentication" in error_msg:
            print("- Possible authentication failure")
            print("  Check username and password")
        elif "timeout" in error_msg:
            print("- Connection timeout")
            print("  Check network connection")
            print("  Verify MongoDB Atlas settings")
        elif "ssl" in error_msg:
            print("- SSL/TLS connection issue")
            print("  Check network security settings")
        else:
            print("- Unknown connection issue")
        
        # Print full traceback for debugging
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    detailed_mongodb_connection_test()