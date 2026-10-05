from patients import (
    add_patient,
    view_patients,
    search_patient,
    update_patient,
    delete_patient
)

from doctors import (
    add_doctor,
    view_doctors
)

from appointments import (
    book_appointment,
    view_appointments,
    cancel_appointment
)

from billing import (
    create_bill,
    view_bills
)


def patient_menu():
    while True:

        print("\n========== PATIENT MANAGEMENT ==========")
        print("1. Add Patient")
        print("2. View Patients")
        print("3. Search Patient")
        print("4. Update Patient")
        print("5. Delete Patient")
        print("6. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            add_patient()

        elif choice == "2":
            view_patients()

        elif choice == "3":
            search_patient()

        elif choice == "4":
            update_patient()

        elif choice == "5":
            delete_patient()

        elif choice == "6":
            break

        else:
            print("Invalid choice.")


def doctor_menu():
    while True:

        print("\n========== DOCTOR MANAGEMENT ==========")
        print("1. Add Doctor")
        print("2. View Doctors")
        print("3. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            add_doctor()

        elif choice == "2":
            view_doctors()

        elif choice == "3":
            break

        else:
            print("Invalid choice.")


def appointment_menu():
    while True:

        print("\n========== APPOINTMENT MANAGEMENT ==========")
        print("1. Book Appointment")
        print("2. View Appointments")
        print("3. Cancel Appointment")
        print("4. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            book_appointment()

        elif choice == "2":
            view_appointments()

        elif choice == "3":
            cancel_appointment()

        elif choice == "4":
            break

        else:
            print("Invalid choice.")


def billing_menu():
    while True:

        print("\n========== BILLING MANAGEMENT ==========")
        print("1. Create Bill")
        print("2. View Bills")
        print("3. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            create_bill()

        elif choice == "2":
            view_bills()

        elif choice == "3":
            break

        else:
            print("Invalid choice.")


def main():

    while True:

        print("\n")
        print("==========================================")
        print("       HOSPITAL MANAGEMENT SYSTEM")
        print("==========================================")
        print("1. Patient Management")
        print("2. Doctor Management")
        print("3. Appointment Management")
        print("4. Billing Management")
        print("5. Exit")
        print("==========================================")

        choice = input("Enter choice: ")

        if choice == "1":
            patient_menu()

        elif choice == "2":
            doctor_menu()

        elif choice == "3":
            appointment_menu()

        elif choice == "4":
            billing_menu()

        elif choice == "5":
            print("Thank you for using Hospital Management System.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()