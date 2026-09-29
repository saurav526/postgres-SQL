from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# MongoDB connection
MONGO_URI = "mongodb://localhost:27017/"

# Database name
DATABASE_NAME = "employee_management_system"

# Collection name
COLLECTION_NAME = "employees"


try:
    # Connect to MongoDB
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

    # Test connection
    client.admin.command("ping")

    print("SUCCESS: Connected to MongoDB!")

    # Create/select database
    db = client[DATABASE_NAME]

    # Create/select collection
    employees = db[COLLECTION_NAME]

    # Sample employee data
    employee_data = [
        {
            "employee_id": 101,
            "name": "Rahul Sharma",
            "age": 24,
            "department": "Data Science",
            "salary": 55000
        },
        {
            "employee_id": 102,
            "name": "Priya Singh",
            "age": 25,
            "department": "AI/ML",
            "salary": 60000
        },
        {
            "employee_id": 103,
            "name": "Amit Kumar",
            "age": 26,
            "department": "Software Development",
            "salary": 58000
        }
    ]

    # Insert data
    result = employees.insert_many(employee_data)

    print("SUCCESS: Database created!")
    print(f"Database name: {DATABASE_NAME}")
    print(f"Collection name: {COLLECTION_NAME}")
    print(f"Inserted documents: {len(result.inserted_ids)}")

    # Display inserted documents
    print("\nEmployee Records:")
    print("-" * 50)

    for employee in employees.find():
        print(employee)

    # Display database collections
    print("\nCollections in database:")
    print(db.list_collection_names())

    # Close connection
    client.close()

    print("\nMongoDB connection closed.")


except ConnectionFailure:
    print("ERROR: Could not connect to MongoDB.")
    print("Make sure MongoDB Server is running.")

except ServerSelectionTimeoutError:
    print("ERROR: MongoDB server is not running.")
    print("Start MongoDB and run the program again.")

except Exception as e:
    print("ERROR:", e)
    