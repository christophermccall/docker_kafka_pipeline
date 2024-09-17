import json
from kafka import KafkaProducer
from time import sleep
from random import randint, uniform

# Define the Kafka producer to connect to the Kafka broker in Docker
producer = KafkaProducer(
    bootstrap_servers='kafka:9093',  # Internal Docker network Kafka address
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize data as JSON
)

# Function to simulate customer transactions
def produce_transaction():
    customer_id = str(randint(10000, 99999))  # Random customer ID
    amount = round(uniform(10.0, 1000.0), 2)  # Random transaction amount
    return {"customer_id": customer_id, "amount": amount}

# Infinite loop to continuously send data to Kafka
while True:
    transaction = produce_transaction()
    print(f"Sending transaction: {transaction}")
    producer.send('customer_transactions', value=transaction)  # Send to the topic
    producer.flush()  # Ensure the message is delivered to Kafka
    sleep(1)  # Send one message every second (adjust as needed)
