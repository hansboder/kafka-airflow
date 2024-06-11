# kafka-airflow
experiments with kafka and airflow

Based off of https://medium.com/apache-airflow/data-engineering-end-to-end-project-part-1-airflow-kafka-cassandra-mongodb-docker-a87f2daec55e and 
https://github.com/dogukannulu/airflow_kafka_cassandra_mongodb

# kafka_produce_messages.py
Sends random messages into a kafka topic

# kafka_batch_consume_messages.py
Waits until it has a full batch before processing

# settings.py 
modify with your topic / kafka broker endpoints.

