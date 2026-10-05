import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import (
    initialize_database, authenticate,
    patients, doctors, appointments, bills
)

class HospitalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hospital Management System")
        self.geometry("1250x760")
        self.minsize(1050, 650)
        self.configure(bg="#f4f7fb")

        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.style.configure("TButton", font=("Segoe UI", 10), padding=8)
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=32)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        self.user = None
        self.current_page = None
        self.show_login()

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear()
        self.current_page = None

        outer = tk.Frame(self, bg="#edf3f9")
        outer.pack(fill="both", expand=True)

        card = tk.Frame(outer, bg="white", bd=0, highlightthickness=1,
                        highlightbackground="#dce4ee")
        card.place(relx=0.5, rely=0.5, anchor="center", width=430, height=500)

        tk.Label(card, text="HOSPITAL", bg="white", fg="#1976d2",
                 font=("Segoe UI", 26, "bold")).pack(pady=(45, 0))
        tk.Label(card, text="MANAGEMENT SYSTEM", bg="white", fg="#263238",
                 font=("Segoe UI", 16, "bold")).pack(pady=(0, 35))
        tk.Label(card, text="Username", bg="white", fg="#455a64",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=55)

        username = ttk.Entry(card, font=("Segoe UI", 11))
        username.pack(fill="x", padx=55, pady=(6, 18), ipady=7)

        tk.Label(card, text="Password", bg="white", fg="#455a64",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=55)

        password = ttk.Entry(card, show="*", font=("Segoe UI", 11))
        password.pack(fill="x", padx=55, pady=(6, 25), ipady=7)

        def login():
            user = authenticate(username.get(), password.get())
            if user:
                self.user = user
                self.show_dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")

        ttk.Button(card, text="LOGIN", command=login).pack(fill="x", padx=55, ipady=5)
        tk.Label(card, text="Default: admin / admin123", bg="white",
                 fg="#78909c", font=("Segoe UI", 9)).pack(pady=18)
        password.bind("<Return>", lambda e: login())
        username.focus()

    def base_layout(self, title):
        self.clear()

        sidebar = tk.Frame(self, bg="#172b4d", width=230)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="HOSPITAL", bg="#172b4d", fg="white",
                 font=("Segoe UI", 20, "bold")).pack(pady=(35, 0))
        tk.Label(sidebar, text="MANAGEMENT", bg="#172b4d", fg="#9fb3cc",
                 font=("Segoe UI", 11, "bold")).pack(pady=(0, 35))

        items = [
            ("Dashboard", self.show_dashboard),
            ("Patients", self.show_patients),
            ("Doctors", self.show_doctors),
            ("Appointments", self.show_appointments),
            ("Billing", self.show_billing),
        ]

        for text, command in items:
            b = tk.Button(
                sidebar, text="  " + text, command=command,
                anchor="w", relief="flat", bd=0,
                bg="#172b4d", fg="white",
                activebackground="#244a78", activeforeground="white",
                font=("Segoe UI", 11), padx=20, pady=13
            )
            b.pack(fill="x", padx=10, pady=2)

        tk.Frame(sidebar, bg="#172b4d").pack(expand=True, fill="both")
        tk.Button(sidebar, text="  Logout", command=self.logout,
                  anchor="w", relief="flat", bd=0,
                  bg="#172b4d", fg="#ffb4ab",
                  activebackground="#244a78", activeforeground="white",
                  font=("Segoe UI", 11), padx=20, pady=13).pack(
                      fill="x", padx=10, pady=15)

        content = tk.Frame(self, bg="#f4f7fb")
        content.pack(side="left", fill="both", expand=True)

        top = tk.Frame(content, bg="white", height=75)
        top.pack(fill="x")
        top.pack_propagate(False)

        tk.Label(top, text=title, bg="white", fg="#172b4d",
                 font=("Segoe UI", 22, "bold")).pack(side="left", padx=28, pady=20)

        tk.Label(top, text=f"Logged in as: {self.user['username']}",
                 bg="white", fg="#607d8b",
                 font=("Segoe UI", 10)).pack(side="right", padx=28)

        body = tk.Frame(content, bg="#f4f7fb")
        body.pack(fill="both", expand=True, padx=25, pady=20)
        self.current_page = body
        return body

    def add_stat(self, parent, title, value, column):
        card = tk.Frame(parent, bg="white", highlightthickness=1,
                        highlightbackground="#e0e6ed")
        card.grid(row=0, column=column, sticky="nsew", padx=8)
        tk.Label(card, text=title, bg="white", fg="#78909c",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=18, pady=(18, 4))
        label = tk.Label(card, text=value, bg="white", fg="#172b4d",
                         font=("Segoe UI", 26, "bold"))
        label.pack(anchor="w", padx=18, pady=(0, 18))
        return label

    def show_dashboard(self):
        body = self.base_layout("Dashboard")
        stats = tk.Frame(body, bg="#f4f7fb")
        stats.pack(fill="x")
        for i in range(4):
            stats.columnconfigure(i, weight=1)

        self.add_stat(stats, "Total Patients", patients.count_documents({}), 0)
        self.add_stat(stats, "Total Doctors", doctors.count_documents({}), 1)
        self.add_stat(stats, "Appointments", appointments.count_documents({}), 2)
        self.add_stat(stats, "Bills", bills.count_documents({}), 3)

        welcome = tk.Frame(body, bg="white", highlightthickness=1,
                           highlightbackground="#e0e6ed")
        welcome.pack(fill="both", expand=True, pady=25)
        tk.Label(welcome, text="Welcome to the Hospital Management System",
                 bg="white", fg="#172b4d",
                 font=("Segoe UI", 20, "bold")).pack(pady=(60, 10))
        tk.Label(welcome,
                 text="Use the navigation panel to manage patients, doctors, appointments and billing.",
                 bg="white", fg="#607d8b",
                 font=("Segoe UI", 11)).pack()
        tk.Label(welcome, text=datetime.now().strftime("%d %B %Y, %I:%M %p"),
                 bg="white", fg="#1976d2",
                 font=("Segoe UI", 12, "bold")).pack(pady=25)

    def make_toolbar(self, body, add_command, search_command=None):
        bar = tk.Frame(body, bg="#f4f7fb")
        bar.pack(fill="x", pady=(0, 12))
        ttk.Button(bar, text="+ Add New", command=add_command).pack(side="left")
        if search_command:
            ttk.Button(bar, text="Search / Refresh", command=search_command).pack(side="left", padx=8)

    def make_tree(self, body, columns, widths):
        frame = tk.Frame(body, bg="white")
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor="center")
        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        return tree

    def show_patients(self):
        body = self.base_layout("Patient Management")
        self.make_toolbar(body, self.patient_form)
        cols = ("ID", "Name", "Age", "Gender", "Phone", "Disease")
        tree = self.make_tree(body, cols, (100, 180, 70, 90, 140, 220))

        for p in patients.find().sort("patient_id", 1):
            tree.insert("", "end", values=(
                p.get("patient_id", ""), p.get("name", ""), p.get("age", ""),
                p.get("gender", ""), p.get("phone", ""), p.get("disease", "")
            ))

        btns = tk.Frame(body, bg="#f4f7fb")
        btns.pack(fill="x", pady=15)
        ttk.Button(btns, text="Edit Selected",
                   command=lambda: self.edit_patient(tree)).pack(side="left")
        ttk.Button(btns, text="Delete Selected",
                   command=lambda: self.delete_patient(tree)).pack(side="left", padx=8)

    def patient_form(self, patient=None):
        self.form_window("Patient", [
            ("Patient ID", patient.get("patient_id", "") if patient else ""),
            ("Name", patient.get("name", "") if patient else ""),
            ("Age", patient.get("age", "") if patient else ""),
            ("Gender", patient.get("gender", "") if patient else ""),
            ("Phone", patient.get("phone", "") if patient else ""),
            ("Address", patient.get("address", "") if patient else ""),
            ("Disease", patient.get("disease", "") if patient else ""),
        ], lambda data, win: self.save_patient(data, win, patient))

    def save_patient(self, d, win, old):
        try:
            age = int(d["Age"])
            if age < 0 or age > 130:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Age", "Enter a valid age.")
            return
        if not d["Patient ID"] or not d["Name"]:
            messagebox.showerror("Required", "Patient ID and Name are required.")
            return
        try:
            if old:
                patients.update_one({"patient_id": old["patient_id"]}, {"$set": {
                    "name": d["Name"], "age": age, "gender": d["Gender"],
                    "phone": d["Phone"], "address": d["Address"], "disease": d["Disease"]
                }})
            else:
                patients.insert_one({
                    "patient_id": d["Patient ID"], "name": d["Name"], "age": age,
                    "gender": d["Gender"], "phone": d["Phone"],
                    "address": d["Address"], "disease": d["Disease"]
                })
            win.destroy()
            self.show_patients()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def edit_patient(self, tree):
        item = tree.selection()
        if not item:
            messagebox.showwarning("Select", "Select a patient first.")
            return
        pid = tree.item(item[0])["values"][0]
        p = patients.find_one({"patient_id": pid})
        self.patient_form(p)

    def delete_patient(self, tree):
        item = tree.selection()
        if not item:
            messagebox.showwarning("Select", "Select a patient first.")
            return
        pid = tree.item(item[0])["values"][0]
        if messagebox.askyesno("Confirm", "Delete selected patient?"):
            patients.delete_one({"patient_id": pid})
            self.show_patients()

    def show_doctors(self):
        body = self.base_layout("Doctor Management")
        self.make_toolbar(body, self.doctor_form)
        cols = ("ID", "Name", "Specialization", "Phone", "Experience")
        tree = self.make_tree(body, cols, (100, 190, 220, 150, 120))
        for d in doctors.find().sort("doctor_id", 1):
            tree.insert("", "end", values=(
                d.get("doctor_id", ""), d.get("name", ""),
                d.get("specialization", ""), d.get("phone", ""),
                d.get("experience", "")
            ))
        btns = tk.Frame(body, bg="#f4f7fb")
        btns.pack(fill="x", pady=12)
        ttk.Button(btns, text="Edit Selected",
                   command=lambda: self.edit_doctor(tree)).pack(side="left")
        ttk.Button(btns, text="Delete Selected",
                   command=lambda: self.delete_doctor(tree)).pack(side="left", padx=8)

    def doctor_form(self, doctor=None):
        self.form_window("Doctor", [
            ("Doctor ID", doctor.get("doctor_id", "") if doctor else ""),
            ("Name", doctor.get("name", "") if doctor else ""),
            ("Specialization", doctor.get("specialization", "") if doctor else ""),
            ("Phone", doctor.get("phone", "") if doctor else ""),
            ("Experience", doctor.get("experience", "") if doctor else ""),
        ], lambda data, win: self.save_doctor(data, win, doctor))

    def save_doctor(self, d, win, old):
        try:
            exp = int(d["Experience"])
            if exp < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid", "Experience must be a valid number.")
            return
        if not d["Doctor ID"] or not d["Name"]:
            messagebox.showerror("Required", "Doctor ID and Name are required.")
            return
        try:
            if old:
                doctors.update_one({"doctor_id": old["doctor_id"]}, {"$set": {
                    "name": d["Name"], "specialization": d["Specialization"],
                    "phone": d["Phone"], "experience": exp
                }})
            else:
                doctors.insert_one({
                    "doctor_id": d["Doctor ID"], "name": d["Name"],
                    "specialization": d["Specialization"], "phone": d["Phone"],
                    "experience": exp
                })
            win.destroy()
            self.show_doctors()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def edit_doctor(self, tree):
        item = tree.selection()
        if not item:
            messagebox.showwarning("Select", "Select a doctor first.")
            return
        did = tree.item(item[0])["values"][0]
        self.doctor_form(doctors.find_one({"doctor_id": did}))

    def delete_doctor(self, tree):
        item = tree.selection()
        if not item:
            messagebox.showwarning("Select", "Select a doctor first.")
            return
        did = tree.item(item[0])["values"][0]
        if messagebox.askyesno("Confirm", "Delete selected doctor?"):
            doctors.delete_one({"doctor_id": did})
            self.show_doctors()

    def show_appointments(self):
        body = self.base_layout("Appointment Management")
        self.make_toolbar(body, self.appointment_form)
        cols = ("ID", "Patient", "Doctor", "Date", "Time", "Status")
        tree = self.make_tree(body, cols, (110, 190, 190, 120, 100, 120))
        for a in appointments.find().sort("date", 1):
            tree.insert("", "end", values=(
                a.get("appointment_id", ""), a.get("patient_name", ""),
                a.get("doctor_name", ""), a.get("date", ""),
                a.get("time", ""), a.get("status", "")
            ))
        btns = tk.Frame(body, bg="#f4f7fb")
        btns.pack(fill="x", pady=12)
        ttk.Button(btns, text="Cancel Selected",
                   command=lambda: self.cancel_appointment(tree)).pack(side="left")
        ttk.Button(btns, text="Delete Selected",
                   command=lambda: self.delete_appointment(tree)).pack(side="left", padx=8)

    def appointment_form(self):
        self.form_window("Appointment", [
            ("Appointment ID", ""),
            ("Patient ID", ""),
            ("Doctor ID", ""),
            ("Date (DD-MM-YYYY)", ""),
            ("Time", ""),
        ], self.save_appointment)

    def save_appointment(self, d, win):
        p = patients.find_one({"patient_id": d["Patient ID"]})
        doc = doctors.find_one({"doctor_id": d["Doctor ID"]})
        if not p or not doc:
            messagebox.showerror("Invalid", "Patient ID or Doctor ID does not exist.")
            return
        if not all(d.values()):
            messagebox.showerror("Required", "All fields are required.")
            return
        try:
            appointments.insert_one({
                "appointment_id": d["Appointment ID"],
                "patient_id": p["patient_id"], "patient_name": p["name"],
                "doctor_id": doc["doctor_id"], "doctor_name": doc["name"],
                "date": d["Date (DD-MM-YYYY)"], "time": d["Time"],
                "status": "Scheduled", "created_at": datetime.now()
            })
            win.destroy()
            self.show_appointments()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def cancel_appointment(self, tree):
        item = tree.selection()
        if not item:
            messagebox.showwarning("Select", "Select an appointment first.")
            return
        aid = tree.item(item[0])["values"][0]
        appointments.update_one({"appointment_id": aid}, {"$set": {"status": "Cancelled"}})
        self.show_appointments()

    def delete_appointment(self, tree):
        item = tree.selection()
        if not item:
            messagebox.showwarning("Select", "Select an appointment first.")
            return
        aid = tree.item(item[0])["values"][0]
        if messagebox.askyesno("Confirm", "Delete selected appointment?"):
            appointments.delete_one({"appointment_id": aid})
            self.show_appointments()

    def show_billing(self):
        body = self.base_layout("Billing Management")
        self.make_toolbar(body, self.bill_form)
        cols = ("Bill ID", "Patient", "Consultation", "Medicine", "Room", "Tests", "Total")
        tree = self.make_tree(body, cols, (100, 180, 120, 120, 110, 110, 120))
        for b in bills.find().sort("bill_id", 1):
            tree.insert("", "end", values=(
                b.get("bill_id", ""), b.get("patient_name", ""),
                f"₹{b.get('consultation_fee', 0):.2f}",
                f"₹{b.get('medicine_charges', 0):.2f}",
                f"₹{b.get('room_charges', 0):.2f}",
                f"₹{b.get('test_charges', 0):.2f}",
                f"₹{b.get('total_amount', 0):.2f}"
            ))
        btns = tk.Frame(body, bg="#f4f7fb")
        btns.pack(fill="x", pady=12)
        ttk.Button(btns, text="Delete Selected",
                   command=lambda: self.delete_bill(tree)).pack(side="left")

    def bill_form(self):
        self.form_window("Create Bill", [
            ("Bill ID", ""),
            ("Patient ID", ""),
            ("Consultation Fee", ""),
            ("Medicine Charges", ""),
            ("Room Charges", ""),
            ("Test Charges", ""),
        ], self.save_bill)

    def save_bill(self, d, win):
        p = patients.find_one({"patient_id": d["Patient ID"]})
        if not p:
            messagebox.showerror("Invalid", "Patient ID does not exist.")
            return
        try:
            values = [
                float(d["Consultation Fee"]),
                float(d["Medicine Charges"]),
                float(d["Room Charges"]),
                float(d["Test Charges"])
            ]
            if any(v < 0 for v in values):
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid", "Charges must be valid non-negative numbers.")
            return
        if not d["Bill ID"]:
            messagebox.showerror("Required", "Bill ID is required.")
            return
        try:
            total = sum(values)
            bills.insert_one({
                "bill_id": d["Bill ID"], "patient_id": p["patient_id"],
                "patient_name": p["name"],
                "consultation_fee": values[0], "medicine_charges": values[1],
                "room_charges": values[2], "test_charges": values[3],
                "total_amount": total, "created_at": datetime.now()
            })
            win.destroy()
            self.show_billing()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def delete_bill(self, tree):
        item = tree.selection()
        if not item:
            messagebox.showwarning("Select", "Select a bill first.")
            return
        bid = tree.item(item[0])["values"][0]
        if messagebox.askyesno("Confirm", "Delete selected bill?"):
            bills.delete_one({"bill_id": bid})
            self.show_billing()

    def form_window(self, title, fields, save_callback):
        win = tk.Toplevel(self)
        win.title(title)
        height = min(700, max(560, 180 + len(fields) * 70))
        win.geometry(f"480x{height}")
        win.resizable(False, False)
        win.configure(bg="white")
        win.transient(self)
        win.grab_set()

        tk.Label(win, text=title, bg="white", fg="#172b4d",
                 font=("Segoe UI", 20, "bold")).pack(pady=25)

        entries = {}
        form = tk.Frame(win, bg="white")
        form.pack(fill="both", expand=True, padx=40)

        for label, value in fields:
            tk.Label(form, text=label, bg="white", fg="#455a64",
                     font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(5, 3))
            entry = ttk.Entry(form)
            entry.pack(fill="x", ipady=5, pady=(0, 8))
            entry.insert(0, str(value))
            entries[label] = entry

        def submit():
            data = {k: v.get().strip() for k, v in entries.items()}
            save_callback(data, win)

        ttk.Button(form, text="Save", command=submit).pack(fill="x", pady=15)
        ttk.Button(form, text="Cancel", command=win.destroy).pack(fill="x")

    def logout(self):
        if messagebox.askyesno("Logout", "Do you want to logout?"):
            self.user = None
            self.show_login()

if __name__ == "__main__":
    try:
        initialize_database()
        app = HospitalApp()
        app.mainloop()
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Startup Error", str(e))
        root.destroy()
