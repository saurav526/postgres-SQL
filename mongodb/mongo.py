from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError


MONGO_URI = "mongodb://localhost:27017/"

DATABASE_NAME = "employee_management_system"


COLLECTION_NAME = "employees"


try:
    
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

   
    client.admin.command("ping")

    print("SUCCESS: Connected to MongoDB!")

   
    db = client[DATABASE_NAME]

    
    employees = db[COLLECTION_NAME]

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

    
    result = employees.insert_many(employee_data)

    print("SUCCESS: Database created!")
    print(f"Database name: {DATABASE_NAME}")
    print(f"Collection name: {COLLECTION_NAME}")
    print(f"Inserted documents: {len(result.inserted_ids)}")

    
    print("\nEmployee Records:")
    print("-" * 50)

    for employee in employees.find():
        print(employee)

    
    print("\nCollections in database:")
    print(db.list_collection_names())

    
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
    