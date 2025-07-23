import os
import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

class MongoDBHandler:
    def __init__(self, collection_name: str):
        # Load environment variables
        load_dotenv()

        username = os.getenv("MONGO_USER")
        password = os.getenv("MONGO_PASS")
        cluster = os.getenv("MONGO_CLUSTER")
        db_name = os.getenv("MONGO_DB")

        if not all([username, password, cluster, db_name]):
            raise ValueError("Missing MongoDB environment configuration.")

        uri = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority"

        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.client.server_info()
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
            print(f"Connected to MongoDB Atlas: {db_name}/{collection_name}")
        except ConnectionFailure as e:
            raise RuntimeError("Failed to connect to MongoDB Atlas.") from e

    def insert_post(self, post: dict) -> str:
        post["created_at"] = datetime.datetime.utcnow()
        result = self.collection.insert_one(post)
        return str(result.inserted_id)

    def get_all_posts(self) -> list:
        return list(self.collection.find({}, {'_id': 0}))

    def find_post(self, query: dict) -> dict:
        return self.collection.find_one(query)

    def update_post(self, query: dict, update_data: dict) -> bool:
        result = self.collection.update_one(query, {'$set': update_data})
        return result.modified_count > 0

    def delete_post(self, query: dict) -> bool:
        result = self.collection.delete_one(query)
        return result.deleted_count > 0
