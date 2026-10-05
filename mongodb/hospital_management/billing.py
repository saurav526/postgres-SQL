from database import bills_collection
from database import patients_collection


def create_bill():
    print("\n========== CREATE BILL ==========")

    bill_id = input("Enter Bill ID: ")
    patient_id = input("Enter Patient ID: ")

    patient = patients_collection.find_one(
        {"patient_id": patient_id}
    )

    if not patient:
        print("Patient not found.")
        return

    consultation = float(
        input("Consultation Fee: ")
    )

    medicine = float(
        input("Medicine Charges: ")
    )

    room = float(
        input("Room Charges: ")
    )

    test = float(
        input("Test Charges: ")
    )

    total = consultation + medicine + room + test

    existing = bills_collection.find_one(
        {"bill_id": bill_id}
    )

    if existing:
        print("Bill ID already exists.")
        return

    bill = {
        "bill_id": bill_id,
        "patient_id": patient_id,
        "patient_name": patient["name"],
        "consultation_fee": consultation,
        "medicine_charges": medicine,
        "room_charges": room,
        "test_charges": test,
        "total_amount": total
    }

    bills_collection.insert_one(bill)

    print("\nBill created successfully.")
    print("Patient:", patient["name"])
    print("Total Amount: ₹", total)


def view_bills():
    print("\n========== ALL BILLS ==========")

    bills = bills_collection.find()

    found = False

    for bill in bills:
        found = True

        print("--------------------------------")
        print("Bill ID          :", bill["bill_id"])
        print("Patient          :", bill["patient_name"])
        print("Consultation     :", bill["consultation_fee"])
        print("Medicine         :", bill["medicine_charges"])
        print("Room             :", bill["room_charges"])
        print("Tests            :", bill["test_charges"])
        print("Total            :", bill["total_amount"])

    if not found:
        print("No bills found.")