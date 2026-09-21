import pandas as pd
import psycopg2
from psycopg2 import sql
from pathlib import Path


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "etl_database",
    "user": "postgres",
    "password": "your_password_here"  # Replace with your actual password
}

CSV_FILE = Path("C:\\Users\\Asus\\OneDrive\\Desktop\\coding file\\postgres SQL\\ETL_postgres\\Data\\raw_data.csv")
def extract_data():

    print("\n========== EXTRACT PHASE ==========")

    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"CSV file not found: {CSV_FILE}"
        )

    df = pd.read_csv(CSV_FILE)
    print("Raw data successfully extracted.")
    print(f"Number of rows: {len(df)}")
    print(f"Number of columns: {len(df.columns)}")

    print("\nRaw Data:")
    print(df)

    return df

def transform_data(df):

    print("\n========== TRANSFORM PHASE ==========")

    df = df.copy()

    before_duplicates = len(df)

    df.drop_duplicates(
        subset=["customer_id"],
        keep="first",
        inplace=True
    )

    after_duplicates = len(df)

    print(
        f"Duplicates removed: "
        f"{before_duplicates - after_duplicates}"
    )

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    string_columns = df.select_dtypes(
        include=["object"]
    ).columns

    for column in string_columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    df["name"] = df["name"].str.title()

    df["email"] = (
        df["email"]
        .str.lower()
        .str.strip()
    )

    df["city"] = (
        df["city"]
        .str.title()
        .str.strip()
    )

    df["age"] = pd.to_numeric(
        df["age"],
        errors="coerce"
    )

    median_age = df["age"].median()

    df["age"] = df["age"].fillna(
        median_age
    )

    df["age"] = df["age"].astype(int)

    df["salary"] = pd.to_numeric(
        df["salary"],
        errors="coerce"
    )

    median_salary = df["salary"].median()

    df["salary"] = df["salary"].fillna(
        median_salary
    )

    df["join_date"] = pd.to_datetime(
        df["join_date"],
        errors="coerce"
    )

    df["customer_id"] = pd.to_numeric(
        df["customer_id"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["customer_id"]
    )

    df["customer_id"] = df["customer_id"].astype(int)

    df = df[
        df["email"].str.contains(
            "@",
            na=False
        )
    ]

    df = df[
        [
            "customer_id",
            "name",
            "email",
            "age",
            "city",
            "salary",
            "join_date"
        ]
    ]

    print("\nTransformed Data:")
    print(df)

    print("\nData types:")
    print(df.dtypes)

    print("\nTransformation completed successfully.")

    return df


def create_database():

    print("\n========== DATABASE SETUP ==========")

    connection = psycopg2.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        database="postgres",
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )

    connection.autocommit = True

    cursor = connection.cursor()

    cursor.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s",
        (DB_CONFIG["database"],)
    )

    database_exists = cursor.fetchone()

    if not database_exists:

        cursor.execute(
            sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(DB_CONFIG["database"])
            )
        )

        print(
            f"Database '{DB_CONFIG['database']}' created."
        )

    else:

        print(
            f"Database '{DB_CONFIG['database']}' already exists."
        )

    cursor.close()
    connection.close()


def connect_database():

    connection = psycopg2.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )

    return connection


def create_table(connection):

    print("\n========== TABLE CREATION ==========")

    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(150) NOT NULL,
        age INTEGER,
        city VARCHAR(100),
        salary NUMERIC(12,2),
        join_date DATE
    );
    """

    cursor.execute(create_table_query)

    connection.commit()

    cursor.close()

    print("Customers table created successfully.")


def load_data(df, connection):

    print("\n========== LOAD PHASE ==========")

    cursor = connection.cursor()

    insert_query = """
    INSERT INTO customers
    (
        customer_id,
        name,
        email,
        age,
        city,
        salary,
        join_date
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (customer_id)
    DO UPDATE SET
        name = EXCLUDED.name,
        email = EXCLUDED.email,
        age = EXCLUDED.age,
        city = EXCLUDED.city,
        salary = EXCLUDED.salary,
        join_date = EXCLUDED.join_date;
    """

    for _, row in df.iterrows():

        cursor.execute(
            insert_query,
            (
                int(row["customer_id"]),
                row["name"],
                row["email"],
                int(row["age"]),
                row["city"],
                float(row["salary"]),
                row["join_date"].date()
                if pd.notna(row["join_date"])
                else None
            )
        )

    connection.commit()

    cursor.close()

    print(
        f"{len(df)} records loaded successfully "
        "into PostgreSQL."
    )


def verify_data(connection):

    print("\n========== VERIFICATION ==========")

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM customers;"
    )

    count = cursor.fetchone()[0]

    print(
        f"\nTotal records in database: {count}"
    )

    cursor.execute(
        """
        SELECT
            customer_id,
            name,
            email,
            age,
            city,
            salary,
            join_date
        FROM customers
        ORDER BY customer_id;
        """
    )

    rows = cursor.fetchall()

    print("\nFinal Data in PostgreSQL:")

    for row in rows:
        print(row)

    cursor.close()


def main():

    try:

        print("\n")
        print("=" * 60)
        print("       PYTHON ETL PIPELINE")
        print("       CSV → TRANSFORM → POSTGRESQL")
        print("=" * 60)

        raw_data = extract_data()

        transformed_data = transform_data(
            raw_data
        )

        create_database()

        connection = connect_database()

        print(
            "\nConnected to PostgreSQL successfully."
        )

        create_table(connection)

        load_data(
            transformed_data,
            connection
        )

        verify_data(connection)

        connection.close()

        print("\n")
        print("=" * 60)
        print("ETL PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)

    except Exception as error:

        print("\nETL PIPELINE FAILED")
        print("Error:", error)


if __name__ == "__main__":
    main()