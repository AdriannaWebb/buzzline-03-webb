"""
csv_consumer_webb.py

Consume billing monitoring messages and detect consumer protection violations.

Example Kafka message format:
{"timestamp": "2025-09-14T15:00:00Z", "company": "MegaCorp", "amount": 29.99, "complaint_type": "unexpected_charge"}
"""

#####################################
# Import Modules
#####################################

# Import packages from Python Standard Library
import os
import json

# Use a deque ("deck") - a double-ended queue data structure
# A deque is a good way to monitor a certain number of "most recent" messages
# A deque is a great data structure for time windows (e.g. the last 5 messages)
from collections import deque, defaultdict

# Import external packages
from dotenv import load_dotenv

# Import functions from local modules
from utils.utils_consumer import create_kafka_consumer
from utils.utils_logger import logger

#####################################
# Load Environment Variables
#####################################

# Load environment variables from .env
load_dotenv()

#####################################
# Getter Functions for .env Variables
#####################################


def get_kafka_topic() -> str:
    """Fetch Kafka topic from environment or use default."""
    topic = os.getenv("SMOKER_TOPIC", "unknown_topic")
    logger.info(f"Kafka topic: {topic}")
    return topic


def get_kafka_consumer_group_id() -> str:
    """Fetch Kafka consumer group id from environment or use default."""
    group_id: str = os.getenv("SMOKER_CONSUMER_GROUP_ID", "default_group")
    logger.info(f"Kafka consumer group id: {group_id}")
    return group_id


def get_stall_threshold() -> float:
    """Fetch message interval from environment or use default."""
    temp_variation = float(os.getenv("SMOKER_STALL_THRESHOLD_F", 0.2))
    logger.info(f"Max stall temperature range: {temp_variation} F")
    return temp_variation


def get_rolling_window_size() -> int:
    """Fetch rolling window size from environment or use default."""
    window_size = int(os.getenv("SMOKER_ROLLING_WINDOW_SIZE", 5))
    logger.info(f"Rolling window size: {window_size}")
    return window_size

company_complaint_counts: defaultdict[str, int] = defaultdict(int)

#####################################
# Define a function to detect a stall
#####################################


def process_message(message: str, rolling_window: deque, window_size: int) -> None:
       """
       Process a billing monitoring message and check for violations.

       Args:
           message (str): JSON message received from Kafka.
           rolling_window (deque): Rolling window of complaint data (not used in this version).
           window_size (int): Size of the rolling window (not used in this version).
       """
       try:
           # Log the raw message for debugging
           logger.debug(f"Raw message: {message}")

           # Parse the JSON string into a Python dictionary
           data: dict = json.loads(message)
           company = data.get("company")
           amount = data.get("amount")
           complaint_type = data.get("complaint_type")
           timestamp = data.get("timestamp")
           
           logger.info(f"Processed billing message: {data}")

           # Ensure the required fields are present
           if company is None or amount is None or complaint_type is None:
               logger.error(f"Invalid message format: {message}")
               return

           # Track complaints (ignore "none" complaint types)
           if complaint_type != "none":
               company_complaint_counts[company] += 1
               complaint_count = company_complaint_counts[company]
               
               logger.info(f" Billing complaint from {company}: ${amount} - {complaint_type}")
               
               if complaint_count >= 3:
                   logger.warning(f"BILLING VIOLATION ALERT: {company} has {complaint_count} complaints - potential consumer protection issue!")
               elif complaint_count >= 2:
                   logger.warning(f"WATCH LIST: {company} has {complaint_count} complaints - monitoring closely")
               else:
                   logger.info(f"{company}: First complaint recorded ({complaint_type})")
           else:
               logger.info(f"Clean transaction: {company} - ${amount}")

           # Log current complaint status
           if company_complaint_counts:
               logger.info(f"Current complaint counts: {dict(company_complaint_counts)}")

       except json.JSONDecodeError as e:
           logger.error(f"JSON decoding error for message '{message}': {e}")
       except Exception as e:
           logger.error(f"Error processing message '{message}': {e}")

#####################################
# Define main function for this module
#####################################


def main() -> None:
    """
    Main entry point for the consumer.

    - Reads the Kafka topic name and consumer group ID from environment variables.
    - Creates a Kafka consumer using the `create_kafka_consumer` utility.
    - Polls and processes messages from the Kafka topic.
    """
    logger.info("START consumer.")

    # fetch .env content
    topic = get_kafka_topic()
    group_id = get_kafka_consumer_group_id()
    window_size = get_rolling_window_size()
    logger.info(f"Consumer: Topic '{topic}' and group '{group_id}'...")
    logger.info(f"Rolling window size: {window_size}")

    rolling_window = deque(maxlen=window_size)

    # Create the Kafka consumer using the helpful utility function.
    consumer = create_kafka_consumer(topic, group_id)

    # Poll and process messages
    logger.info(f"Polling messages from topic '{topic}'...")
    try:
        for message in consumer:
            message_str = message.value
            logger.debug(f"Received message at offset {message.offset}: {message_str}")
            process_message(message_str, rolling_window, window_size)
    except KeyboardInterrupt:
        logger.warning("Consumer interrupted by user.")
    except Exception as e:
        logger.error(f"Error while consuming messages: {e}")
    finally:
        consumer.close()
        logger.info(f"Kafka consumer for topic '{topic}' closed.")


#####################################
# Conditional Execution
#####################################

# Ensures this script runs only when executed directly (not when imported as a module).
if __name__ == "__main__":
    main()
