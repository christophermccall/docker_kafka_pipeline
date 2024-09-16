from pyspark.sql import SparkSession
from pyspark.sql.functions import sum

# Initialize Spark session
spark = SparkSession.builder.appName("CustomerTransactions").getOrCreate()

# Read real-time transactions from Kafka
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka:9092") \
  .option("subscribe", "customer_transactions") \
  .load()

# Convert Kafka values to strings and process
transactions = df.selectExpr("CAST(value AS STRING)")
aggregated_sales = transactions.groupBy("customer_id").agg(sum("amount").alias("total_sales"))

# Output the result to the console (or write to another sink)
query = aggregated_sales.writeStream.outputMode("update").format("console").start()
query.awaitTermination()
