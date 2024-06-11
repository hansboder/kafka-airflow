from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from confluent_kafka import Producer, KafkaError

import settings
import uuid

import time
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class KafkaProducerWrapper:
    def __init__(self, bootstrap_servers):
        """
        Initializes the Kafka producer with the given bootstrap servers.
        """
        self.producer_config = {
            'bootstrap.servers': bootstrap_servers
        }
        self.producer = Producer(self.producer_config)

    def produce_message(self, topic, key, value):
        """
        Produces a message to the specified Kafka topic with the given key and value.
        """
        self.producer.produce(topic, key=key, value=value)
        self.producer.flush()

# Function to batch messages from Kafka


def produce_kafka_messages(**kwargs):

    try:
        bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS
        kafka_producer = KafkaProducerWrapper(bootstrap_servers)


        try:
            # produce less than whatever our batch size is to demo that the consumer waits for the batch
            for i in range(settings.KAFKA_BATCH_COUNT-1):
                key = f"{datetime.now().date()}_{uuid.uuid4().hex}"
                value = str(uuid.uuid4().int)
                kafka_producer.produce_message(
                    settings.KAFKA_TOPIC, key, value)
                logger.info("Produced message")

        except KeyboardInterrupt:
            logger.info("Received KeyboardInterrupt. Stopping producer.")
        finally:
            kafka_producer.producer.flush()
            logger.info("Producer flushed.")
    except Exception as e:
        logger.error(f"Error producing message: {e}")
        raise e


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False
}

dag = DAG(
    'kafka_producer',
    default_args=default_args,
    description='A pipeline to produce random messages',
    schedule_interval='*/5 * * * *',
    max_active_runs=1,
    catchup=False,
)

# Task to batch messages from Kafka
produce_messages = PythonOperator(
    task_id='produce_kafka_messages',
    python_callable=produce_kafka_messages,
    provide_context=True,
    dag=dag,
)

produce_messages
