from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, sum
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# Initialize Spark session
spark = SparkSession.builder.appName("CustomerTransactions").getOrCreate()

# Define schema for Kafka value (JSON structure)
schema = StructType([
    StructField("customer_id", StringType(), True),
    StructField("amount", DoubleType(), True)
])

# Read real-time transactions from Kafka
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka:9093") \
  .option("subscribe", "customer_transactions") \
  .load()

# Convert Kafka 'value' from binary to string and parse JSON
transactions = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.customer_id", "data.amount")

# Aggregate sales by customer_id
aggregated_sales = transactions.groupBy("customer_id").agg(sum("amount").alias("total_sales"))

# Output the result to the console (or write to another sink)
query = aggregated_sales.writeStream.outputMode("update").format("console").start()
query.awaitTermination()
