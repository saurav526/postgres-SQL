# Hospital Management System

Python + Tkinter + MongoDB desktop application.

## Features
- Login page
- Dashboard with statistics
- Patient management: add, update, delete, search
- Doctor management: add, update, delete, search
- Appointment management: add, cancel, delete
- Billing management: create, delete, search
- MongoDB persistence
- Logout

## Requirements
- Python 3.10+
- MongoDB Community Server running locally
- MongoDB Compass is optional

## Installation

```bash
pip install -r requirements.txt
python main.py
```

MongoDB URI:
`mongodb://localhost:27017/`

Database:
`hospital_management`

Default login:
- Username: `admin`
- Password: `admin123`

Change the default password in `database.py` after first setup if this is used beyond a college/demo project.

## Project structure

hospital_management_gui/
- main.py
- database.py
- ui.py
- requirements.txt
- README.md
