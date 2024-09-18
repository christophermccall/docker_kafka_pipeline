#!/bin/bash
kafka-topics --create --topic customer_transactions --bootstrap-server kafka:9092 --partitions 3 --replication-factor 1

