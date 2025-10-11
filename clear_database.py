#!/usr/bin/env python3
"""
Script sederhana untuk clear database MongoDB
"""

from pymongo import MongoClient

# MongoDB URI
MONGO_URI = "mongodb+srv://seoterea_db_user:mandar309@friz.6qnklzk.mongodb.net/?retryWrites=true&w=majority&appName=friz"

def clear_database():
    try:
        print("Connecting to MongoDB...")
        client = MongoClient(MONGO_URI)
        
        # Test connection
        client.admin.command('ping')
        print("Connected successfully!")
        
        # Get database
        db = client["UltroidDB"]
        
        print(f"Current collections: {db.list_collection_names()}")
        
        # Clear all collections
        for collection_name in db.list_collection_names():
            db[collection_name].drop()
            print(f"Dropped collection: {collection_name}")
        
        print("Database cleared successfully!")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    clear_database()
