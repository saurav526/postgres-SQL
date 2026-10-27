
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count

spark = SparkSession.builder \
    .appName("LargeStudentDataset") \
    .master("local[*]") \
    .getOrCreate()

# Generate a CSV dataset containing 10,000 students
output_path = "students.csv"

with open(output_path, "w", encoding="utf-8") as file:
    file.write("student_id,name,age,department,marks,attendance\n")

    departments = ["CSE", "AI", "IT", "ECE", "MECH"]

    for i in range(1, 10001):
        name = f"Student_{i}"
        age = 18 + (i % 8)
        department = departments[i % len(departments)]
        marks = 40 + (i % 61)
        attendance = 60 + (i % 41)

        file.write(
            f"{i},{name},{age},{department},"
            f"{marks},{attendance}\n"
        )

# Read the CSV into a Spark DataFrame
df = spark.read.csv(
    output_path,
    header=True,
    inferSchema=True
)

# Display sample records and schema
df.show(10)
df.printSchema()

# Count total records
print("Total students:", df.count())

# Calculate average marks by department
df.groupBy("department").agg(
    count("*").alias("total_students"),
    avg("marks").alias("average_marks")
).show()

# Filter students scoring above 80
df.filter(col("marks") > 80).show(10)

spark.stop()
