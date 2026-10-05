from database import patients_collection


def add_patient():
    print("\n========== ADD PATIENT ==========")

    patient_id = input("Enter Patient ID: ")
    name = input("Enter Patient Name: ")
    age = int(input("Enter Age: "))
    gender = input("Enter Gender: ")
    phone = input("Enter Phone Number: ")
    address = input("Enter Address: ")
    disease = input("Enter Disease: ")

    existing = patients_collection.find_one({"patient_id": patient_id})

    if existing:
        print("Patient ID already exists.")
        return

    patient = {
        "patient_id": patient_id,
        "name": name,
        "age": age,
        "gender": gender,
        "phone": phone,
        "address": address,
        "disease": disease
    }

    patients_collection.insert_one(patient)

    print("Patient added successfully.")


def view_patients():
    print("\n========== ALL PATIENTS ==========")

    patients = patients_collection.find()

    found = False

    for patient in patients:
        found = True

        print("--------------------------------")
        print("Patient ID :", patient["patient_id"])
        print("Name       :", patient["name"])
        print("Age        :", patient["age"])
        print("Gender     :", patient["gender"])
        print("Phone      :", patient["phone"])
        print("Address    :", patient["address"])
        print("Disease    :", patient["disease"])

    if not found:
        print("No patients found.")


def search_patient():
    print("\n========== SEARCH PATIENT ==========")

    patient_id = input("Enter Patient ID: ")

    patient = patients_collection.find_one(
        {"patient_id": patient_id}
    )

    if patient:
        print("\nPatient Found")
        print("--------------------------------")
        print("Patient ID :", patient["patient_id"])
        print("Name       :", patient["name"])
        print("Age        :", patient["age"])
        print("Gender     :", patient["gender"])
        print("Phone      :", patient["phone"])
        print("Address    :", patient["address"])
        print("Disease    :", patient["disease"])
    else:
        print("Patient not found.")


def update_patient():
    print("\n========== UPDATE PATIENT ==========")

    patient_id = input("Enter Patient ID: ")

    patient = patients_collection.find_one(
        {"patient_id": patient_id}
    )

    if not patient:
        print("Patient not found.")
        return

    name = input("Enter new name: ")
    age = int(input("Enter new age: "))
    gender = input("Enter new gender: ")
    phone = input("Enter new phone: ")
    address = input("Enter new address: ")
    disease = input("Enter new disease: ")

    patients_collection.update_one(
        {"patient_id": patient_id},
        {
            "$set": {
                "name": name,
                "age": age,
                "gender": gender,
                "phone": phone,
                "address": address,
                "disease": disease
            }
        }
    )

    print("Patient updated successfully.")


def delete_patient():
    print("\n========== DELETE PATIENT ==========")

    patient_id = input("Enter Patient ID: ")

    result = patients_collection.delete_one(
        {"patient_id": patient_id}
    )

    if result.deleted_count > 0:
        print("Patient deleted successfully.")
    else:
        print("Patient not found.")