from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from confluent_kafka import Consumer, KafkaError

import time
import logging
import settings

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Function to process the batched messages


def process_messages(**kwargs):
    # process each message
    ti = kwargs['ti']
    messages = ti.xcom_pull(key='messages', task_ids='batch_kafka_messages')
    for message in messages:
        logger.info(f"Processing key: {message["key"]}")


# Rather than reading whats available and kicking of a new task, wait until we have a batch.
# Can be either based on number of messages or age of the oldest message
def batch_kafka_messages(**kwargs):

    # 'enable.auto.commit': 'false' is important here. We don't want to commit the messages until we are ready to do so.
    kafka_consumer = Consumer(
        {
            'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
            'group.id': settings.KAFKA_CONSUMER_GROUP_ID,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': 'false'
        }
    )
    kafka_consumer.subscribe([settings.KAFKA_TOPIC])

    messages = []
    oldest_message_timestamp = None

    start_time = time.time()
    try:
        while True:

            logger.info("Polling for messages")
            kafka_message = kafka_consumer.poll(timeout=2.0)

            elapsed_time = time.time() - start_time
            logger.info(f"elapsed_time: {elapsed_time}, message count: {len(messages)}")

            if elapsed_time >= 30:
                # if we have old messages commit them
                if datetime.now() - oldest_message_timestamp > timedelta(minutes=2) and len(messages) > 0:
                        logger.info(f"Oldest message is: {
                                    oldest_message_timestamp}, committing batch")
                        # since we aren't auto-commiting to the topic, we need to commit now.
                        kafka_consumer.commit()
                        kwargs['ti'].xcom_push(key='messages', value=messages)

                logger.info("Time is up, breaking.")
                break

            if kafka_message is None:
                continue

            if kafka_message.error():

                if kafka_message.error().code() == KafkaError._PARTITION_EOF:
                    logger.info('Reached end of partition')
                else:
                    logger.error(f"Error while consuming messages: {
                                 kafka_message.error()}")
                continue

            else:
                messages.append(
                    {
                        "key": kafka_message.key().decode('utf-8'),
                        "value": kafka_message.value().decode('utf-8')
                    }
                )
                logger.info(f"Received message: {
                            kafka_message.key().decode('utf-8')}")

                # timestamp is a bit weird, not sure why it's a tuple
                message_timestamp = datetime.fromtimestamp(
                    kafka_message.timestamp()[1] / 1000)

                if oldest_message_timestamp is None:
                    oldest_message_timestamp = message_timestamp

                if message_timestamp < oldest_message_timestamp:
                    oldest_message_timestamp = message_timestamp

                # Check if we have a full batch
                if len(messages) >= settings.KAFKA_BATCH_COUNT:
                    logger.info(
                        f"Received {settings.KAFKA_BATCH_COUNT} messages. Committing and breaking.")

                    # since we aren't auto-commiting to the topic, we need to commit now.
                    kafka_consumer.commit()
                    kwargs['ti'].xcom_push(key='messages', value=messages)
                    break

                    # return messages

            
            

    except Exception as e:
        logger.exception(f"Error while consuming messages: {e}")
    finally:
        kafka_consumer.close()
        logger.info("Closed Kafka consumer")


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False
}

dag = DAG(
    'kafka_batch_consume_messages',
    default_args=default_args,
    description='A Kafka to Airflow pipeline with message age check',
    schedule_interval='*/5 * * * *',
    max_active_runs=1,
    catchup=False,
)

# Task to batch messages from Kafka
batch_messages = PythonOperator(
    task_id='batch_kafka_messages',
    python_callable=batch_kafka_messages,
    provide_context=True,
    dag=dag,
)

# Task to process batched messages
process_messages_task = PythonOperator(
    task_id='process_messages',
    python_callable=process_messages,
    provide_context=True,
    dag=dag,
)

batch_messages >> process_messages_task
