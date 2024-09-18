#this will allow you to view the consumer once the containers are running
docker exec -it docker_kafka_pipeline-kafka-1 kafka-console-consumer.sh --bootstrap-server localhost:9093 --topic customer_transactions --from-beginning
