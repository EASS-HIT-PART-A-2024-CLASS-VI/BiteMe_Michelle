from pymongo import MongoClient

uri = "mongodb+srv://loliprincess31:loliprincess31@biteme.jvwj4.mongodb.net/?retryWrites=true&w=majority&appName=BiteMe"
client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Connected to MongoDB!")
except Exception as e:
    print(f"Failed to connect: {e}")

