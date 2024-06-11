from confluent_kafka.admin import AdminClient, NewTopic
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

admin_config = {
    'bootstrap.servers': 'kafka1:19092',
    'client.id': 'kafka_admin_client',
}

admin_client = AdminClient(admin_config)

def kafka_create_topic_main():
    """Checks if the topic email_topic exists or not. If not, creates the topic."""
    topic_name = 'batch_topic'

    try:
        logger.info(f"Checking if topic {topic_name} exists")
        existing_topics = admin_client.list_topics(timeout=10).topics
        logger.info(f"Existing topics: {existing_topics}")
        if topic_name in existing_topics:
            return "Exists"
        
        # Create the new topic
        logger.info(f"Creating topic {topic_name}")
        new_topic = NewTopic(topic_name, num_partitions=1, replication_factor=3)
        logger.info(f"New topic: {new_topic}")
        admin_client.create_topics([new_topic])
        logger.info(f"Created topic")
        return "Created"
    except Exception as e:
        logger.error(f"Error while creating topic: {e}")
        return "Error"

if __name__ == "__main__":
    result = kafka_create_topic_main()
    logger.info(result)