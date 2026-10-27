
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("CSVToDataFrame") \
    .master("local[*]") \
    .getOrCreate()

df = spark.read.csv(
    "students.csv",
    header=True,
    inferSchema=True
)

df.show()
df.printSchema()

spark.stop()
