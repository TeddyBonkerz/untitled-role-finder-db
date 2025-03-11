import json
from pymongo import MongoClient
from urllib.parse import quote_plus

def connect_to_database():
    
    try:
        host = "localhost"
        port = 27017
        db_name = "mongo_park_db"
        db_collection = "mongo_park_collection"
        username = quote_plus("mongo_park")
        password = quote_plus("mongo_park")
        authsource = "admin"

        uri = f"mongodb://{username}:{password}@{host}:{port}/?authSource={authsource}"


        client = MongoClient(uri)
        client.admin.command("ping")
        print("Connected successfully")


        role_db = client[db_name]
        role_collection = role_db.get_collection(db_collection)

        with open("job_roles_dump.json", 'r') as file:
            roles = json.load(file)
        
        # Validate JSON structure
        if not isinstance(roles, list):
            raise ValueError("JSON file must contain a list of role descriptions.")
        
        result = role_collection

        result = role_collection.insert_many(roles)
        print(f"Inserted document ID: {result.inserted_id}")

    except Exception as e:
        raise Exception(
            "The following error occurred: ", e)
    
    finally:
        client.close()
    
if __name__ == "__main__":   
  
   # Get the database
   connect_to_database()