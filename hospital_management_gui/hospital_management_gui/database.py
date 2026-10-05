from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime
import hashlib

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "hospital_management"

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    db = client[DB_NAME]
except ConnectionFailure as exc:
    raise RuntimeError(
        "Could not connect to MongoDB. Start MongoDB and run the application again."
    ) from exc

users = db["users"]
patients = db["patients"]
doctors = db["doctors"]
appointments = db["appointments"]
bills = db["bills"]

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def initialize_database():
    users.create_index("username", unique=True)
    patients.create_index("patient_id", unique=True)
    doctors.create_index("doctor_id", unique=True)
    appointments.create_index("appointment_id", unique=True)
    bills.create_index("bill_id", unique=True)

    if users.count_documents({}) == 0:
        users.insert_one({
            "username": "admin",
            "password": hash_password("admin123"),
            "role": "Administrator",
            "created_at": datetime.now()
        })

def authenticate(username, password):
    return users.find_one({
        "username": username.strip(),
        "password": hash_password(password)
    })
