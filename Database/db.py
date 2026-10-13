
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, upper, trim, round as spark_round
)
from pyspark.ml.feature import Imputer

# 1. Create Spark Session
spark = SparkSession.builder \
    .appName("DataFrame_Manipulation_and_Cleaning") \
    .master("local[8501]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# 2. Create a sample dataset
data = [
    (1, " Saurav ", 21, 85000.0, "AI", 85.0),
    (2, "Rahul", 22, 65000.0, "Data Science", 78.0),
    (3, "Priya", None, 72000.0, "AI", 92.0),
    (4, "Ananya", 23, None, "ML", 88.0),
    (5, "Amit", 21, 55000.0, None, 67.0),
    (6, "Rahul", 22, 65000.0, "Data Science", 78.0),
    (7, None, 24, 90000.0, "ML", None),
    (8, "Neha", 22, 68000.0, "AI", 81.0)
]

columns = [
    "id", "name", "age", "salary",
    "department", "score"
]

df = spark.createDataFrame(data, columns)

print("\n1. ORIGINAL DATAFRAME")
df.show(truncate=False)
df.printSchema()

# 3. Select specific columns
print("\n2. SELECT NAME, AGE AND SALARY")
df.select("name", "age", "salary").show()

# 4. Filter rows
print("\n3. EMPLOYEES WITH SALARY ABOVE 70000")
df.filter(col("salary") > 70000).show()

# 5. Add a new column
print("\n4. ADD BONUS COLUMN")
df = df.withColumn(
    "bonus",
    spark_round(col("salary") * 0.10, 2)
)
df.show()

# 6. Rename a column
print("\n5. RENAME SCORE TO PERFORMANCE_SCORE")
df = df.withColumnRenamed("score", "performance_score")
df.show()

# 7. Handle missing values
print("\n6. COUNT MISSING VALUES")
for column in df.columns:
    missing_count = df.filter(col(column).isNull()).count()
    print(f"{column}: {missing_count}")

print("\n7. FILL MISSING DEPARTMENT")
df = df.fillna({"department": "Unknown"})

# 8. Impute missing numerical values using the mean
print("\n8. IMPUTE NUMERICAL MISSING VALUES")
imputer = Imputer(
    inputCols=["age", "salary", "performance_score"],
    outputCols=[
        "age_imputed",
        "salary_imputed",
        "performance_score_imputed"
    ]
).setStrategy("mean")

df = imputer.fit(df).transform(df)

df.show(truncate=False)

# 9. Clean text columns
print("\n9. CLEAN NAME AND DEPARTMENT")
df = df.withColumn("name", trim(col("name")))
df = df.withColumn("name", upper(col("name")))
df = df.fillna({"name": "UNKNOWN"})

df.show(truncate=False)

# 10. Remove duplicate records
print("\n10. REMOVE DUPLICATE RECORDS")
df = df.dropDuplicates()
df.show(truncate=False)

# 11. Create a categorical feature
print("\n11. CREATE PERFORMANCE CATEGORY")
df = df.withColumn(
    "performance_category",
    when(col("performance_score_imputed") >= 85, "High")
    .when(col("performance_score_imputed") >= 70, "Medium")
    .otherwise("Low")
)

df.show(truncate=False)

# 12. Create a conditional feature
print("\n12. CREATE SALARY CATEGORY")
df = df.withColumn(
    "salary_category",
    when(col("salary_imputed") >= 70000, "High Salary")
    .otherwise("Standard Salary")
)

df.show(truncate=False)

# 13. Sort data
print("\n13. SORT BY SALARY IN DESCENDING ORDER")
df.orderBy(col("salary_imputed").desc()).show()

# 14. Group and aggregate data
print("\n14. AVERAGE SALARY BY DEPARTMENT")
df.groupBy("department").avg("salary_imputed").show()

# 15. Display the final processed DataFrame
print("\n15. FINAL PROCESSED DATAFRAME")
df.select(
    "id",
    "name",
    "age_imputed",
    "salary_imputed",
    "department",
    "performance_score_imputed",
    "performance_category",
    "salary_category",
    "bonus"
).show(truncate=False)

# 16. Stop Spark Session
spark.stop()

