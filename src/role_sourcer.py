import json
import requests
import os
from pymongo import MongoClient
from urllib.parse import quote_plus

def get_role_from_external_api():
    base_url = "https://api.theirstack.com/v1/jobs/search"
    token = os.environ.get('API_TOKEN')
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
    }
    payload = {
        "page": 0,
        "limit": 25,
        "job_country_code_or": [
            "US"
        ],
        "posted_at_max_age_days": 7,
        "job_title_or": [
            "Backend Software Engineer", "Software Engineer"
        ],
        # "job_title_pattern_not": [
        #     ^[A-Za-z]*(Senior|senior|Staff|staff)[A-z]*

        # ],
        # "job_title_pattern_not": [
        #     ^[A-Za-z]*(Senior|senior|Staff|staff)[A-z]*

        # ],
        # "job_description_pattern_or": [
        #     (Java|JAVA|java), (Java|JAVA|java)
        # ],
        "remote": True,
        "blur_company_data": True
    }

    try:
        response = requests.post(base_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        print("Request successful")
        response = response.json()
        filename = "src/job_roles_dump.json"

        with open(filename, 'w') as file:
            json.dump(response, file, indent=4)

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


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

        with open("src/job_roles_dump.json", 'r') as file:
            roles = json.load(file)
        
        # Validate JSON structure
        if not isinstance(roles, list):
            raise ValueError("JSON file must contain a list of role descriptions.")
        
        result = role_collection

        result = role_collection.insert_many(roles)
        # print(f"Inserted document ID: {result.inserted_id}")

    except Exception as e:
        raise Exception(
            "The following error occurred: ", e)
    
    finally:
        client.close()
    
if __name__ == "__main__":   
    # get_role_from_external_api()
   # Get the database
    connect_to_database()