from database import doctors_collection


def add_doctor():
    print("\n========== ADD DOCTOR ==========")

    doctor_id = input("Enter Doctor ID: ")
    name = input("Enter Doctor Name: ")
    specialization = input("Enter Specialization: ")
    phone = input("Enter Phone Number: ")
    experience = int(input("Enter Experience (years): "))

    existing = doctors_collection.find_one(
        {"doctor_id": doctor_id}
    )

    if existing:
        print("Doctor ID already exists.")
        return

    doctor = {
        "doctor_id": doctor_id,
        "name": name,
        "specialization": specialization,
        "phone": phone,
        "experience": experience
    }

    doctors_collection.insert_one(doctor)

    print("Doctor added successfully.")


def view_doctors():
    print("\n========== ALL DOCTORS ==========")

    doctors = doctors_collection.find()

    found = False

    for doctor in doctors:
        found = True

        print("--------------------------------")
        print("Doctor ID      :", doctor["doctor_id"])
        print("Name           :", doctor["name"])
        print("Specialization :", doctor["specialization"])
        print("Phone          :", doctor["phone"])
        print("Experience     :", doctor["experience"], "years")

    if not found:
        print("No doctors found.")