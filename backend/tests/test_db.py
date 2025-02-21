from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
print(f"MongoDB URI (partial): {MONGO_URI[:25]}...")

try:
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    
    # Test connection with ping
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB!")
    
    # Try to access the database
    db = client.BiteMeDB  # Using the database name from your code
    
    # Count restaurants
    restaurant_count = db.restaurants.count_documents({})
    print(f"Found {restaurant_count} restaurants in database")
    
    if restaurant_count > 0:
        print("Sample restaurant:")
        print(db.restaurants.find_one())
    else:
        print("No restaurants found. Database might be empty.")
        
except Exception as e:
    print(f"❌ Connection failed: {e}")