from database import appointments_collection
from database import patients_collection
from database import doctors_collection


def book_appointment():
    print("\n========== BOOK APPOINTMENT ==========")

    appointment_id = input("Enter Appointment ID: ")
    patient_id = input("Enter Patient ID: ")
    doctor_id = input("Enter Doctor ID: ")
    date = input("Enter Appointment Date (DD-MM-YYYY): ")
    time = input("Enter Appointment Time: ")

    patient = patients_collection.find_one(
        {"patient_id": patient_id}
    )

    if not patient:
        print("Patient not found.")
        return

    doctor = doctors_collection.find_one(
        {"doctor_id": doctor_id}
    )

    if not doctor:
        print("Doctor not found.")
        return

    existing = appointments_collection.find_one(
        {"appointment_id": appointment_id}
    )

    if existing:
        print("Appointment ID already exists.")
        return

    appointment = {
        "appointment_id": appointment_id,
        "patient_id": patient_id,
        "patient_name": patient["name"],
        "doctor_id": doctor_id,
        "doctor_name": doctor["name"],
        "date": date,
        "time": time,
        "status": "Scheduled"
    }

    appointments_collection.insert_one(appointment)

    print("Appointment booked successfully.")


def view_appointments():
    print("\n========== ALL APPOINTMENTS ==========")

    appointments = appointments_collection.find()

    found = False

    for appointment in appointments:
        found = True

        print("--------------------------------")
        print("Appointment ID :", appointment["appointment_id"])
        print("Patient        :", appointment["patient_name"])
        print("Doctor         :", appointment["doctor_name"])
        print("Date           :", appointment["date"])
        print("Time           :", appointment["time"])
        print("Status         :", appointment["status"])

    if not found:
        print("No appointments found.")


def cancel_appointment():
    print("\n========== CANCEL APPOINTMENT ==========")

    appointment_id = input("Enter Appointment ID: ")

    result = appointments_collection.update_one(
        {"appointment_id": appointment_id},
        {"$set": {"status": "Cancelled"}}
    )

    if result.modified_count > 0:
        print("Appointment cancelled successfully.")
    else:
        print("Appointment not found.")