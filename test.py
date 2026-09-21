import psycopg2

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "employee_management_system"
DB_USER = "postgres"
DB_PASSWORD = "your_password_here"  # Replace with your actual password

connection_string = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

try:
    with psycopg2.connect(connection_string, connect_timeout=10) as conn:
        print("SUCCESS: Connected to PostgreSQL!")

        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            print(cur.fetchone())

except Exception as e:
    print("Connection failed:")
    print(e)


try:
    with psycopg2.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            # SQL to create all tables
            create_tables_sql = """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                age INTEGER
            );

            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                age INTEGER
            );

            CREATE TABLE IF NOT EXISTS departments (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                description TEXT
            );

            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                description TEXT
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                description TEXT
            );
            """

            cursor.execute(create_tables_sql)
            conn.commit()
            print("All tables ('users', 'employees', 'departments', 'projects', 'tasks') created successfully or already exist.")
except Exception as e:
    print(f"Error creating tables. Please check your connection string and database accessibility: {e}")



try:
    with psycopg2.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            # --- Insert Data into users table ---
            insert_query_users = """
            INSERT INTO users (name, email, age)
            VALUES (%s, %s, %s)
            ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name, age = EXCLUDED.age;
            """
            users_data = [
                ("Alice Smith", "alice.smith@example.com", 30),
                ("Bob Johnson", "bob.johnson@example.com", 25),
                ("Charlie Brown", "charlie.brown@example.com", 35)
            ]
            for user in users_data:
                cursor.execute(insert_query_users, user)
            print("Sample data inserted into 'users' table.")

            # --- Insert Data into employees table ---
            insert_query_employees = """
            INSERT INTO employees (name, email, age)
            VALUES (%s, %s, %s)
            ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name, age = EXCLUDED.age;
            """
            employees_data = [
                ("David Lee", "david.lee@company.com", 40),
                ("Eve Davis", "eve.davis@company.com", 28),
                ("Frank Green", "frank.green@company.com", 32)
            ]
            for employee in employees_data:
                cursor.execute(insert_query_employees, employee)
            print("Sample data inserted into 'employees' table.")

            # --- Insert Data into departments table ---
            insert_query_departments = """
            INSERT INTO departments (name, description)
            VALUES (%s, %s)
            ON CONFLICT (name) DO UPDATE SET description = EXCLUDED.description;
            """
            departments_data = [
                ("Human Resources", "Manages employee relations and benefits."),
                ("Engineering", "Develops and maintains software products."),
                ("Marketing", "Handles product promotion and brand awareness.")
            ]
            for department in departments_data:
                cursor.execute(insert_query_departments, department)
            print("Sample data inserted into 'departments' table.")

            # --- Insert Data into projects table ---
            insert_query_projects = """
            INSERT INTO projects (name, description)
            VALUES (%s, %s)
            ON CONFLICT (name) DO UPDATE SET description = EXCLUDED.description;
            """
            projects_data = [
                ("Website Redesign", "Complete overhaul of the company website."),
                ("Mobile App Development", "Creation of a new mobile application."),
                ("Database Optimization", "Improving performance of the main database.")
            ]
            for project in projects_data:
                cursor.execute(insert_query_projects, project)
            print("Sample data inserted into 'projects' table.")

            # --- Insert Data into tasks table ---
            insert_query_tasks = """
            INSERT INTO tasks (name, description)
            VALUES (%s, %s)
            ON CONFLICT (name) DO UPDATE SET description = EXCLUDED.description;
            """
            tasks_data = [
                ("Develop Login Page", "Implement user authentication for the website."),
                ("Design UI/UX Mockups", "Create visual designs for the mobile app."),
                ("Prepare Q3 Report", "Compile and analyze quarterly sales data."),
                ("Optimize Query Performance", "Refactor slow database queries.")
            ]
            for task in tasks_data:
                cursor.execute(insert_query_tasks, task)
            print("Sample data inserted into 'tasks' table.")

            conn.commit()
            print("All sample data insertion/update operations completed successfully!")
except Exception as e:
    print(f"Error inserting data. Please check your connection string and database accessibility: {e}")