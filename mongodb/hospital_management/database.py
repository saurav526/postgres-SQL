from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

MONGO_URI = "mongodb://localhost:27017/"

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")

    db = client["hospital_management"]

    patients_collection = db["patients"]
    doctors_collection = db["doctors"]
    appointments_collection = db["appointments"]
    bills_collection = db["bills"]

    print("MongoDB connected successfully.")

except ConnectionFailure:
    print("MongoDB connection failed.")
    exit()