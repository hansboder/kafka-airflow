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


# Prometheus setup

* run docker compose up -d
* Check localhost:9090 -> Status -> Targets
* There should be 4 endpoints
  * kafka-broker, kafka-connect, kafka-lag-exporter-prometheus.
  
# Grafana
* Log into localhost:3000 with username / password specified in docker-compose.yaml on the grafana container.
* The datasource for prometheus and dashboards should already be loaded.
* The kafka cluster is an overview of cluster health
* The lag exporter dashboard shows kafka consumer lag on the cluster.
* These are taken from the confluent examples here https://github.com/confluentinc/jmx-monitoring-stacks/tree/main/jmxexporter-prometheus-grafana/assets/grafana/provisioning/dashboards


# JMX configs

The jmx jar agent that is mounted to each kafka cluster exposes a metrics endpoint for prometheus. The configuration in `/config` defines the metrics. These configuration files are taken from https://github.com/confluentinc/jmx-monitoring-stacks/blob/main/shared-assets/jmx-exporter/kafka_broker.yml

* Lag Exporter