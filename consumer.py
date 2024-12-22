from confluent_kafka import Consumer, KafkaException

# Kafka configuration
consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'sensor-consumer-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_config)
topic = "sensor-events"
consumer.subscribe([topic])

print(f"Subscribed to topic: {topic}")

try:
    while True:
        msg = consumer.poll(1.0)  # Poll for new messages
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        else:
            print(f"Received message: {msg.value().decode('utf-8')}")

except KeyboardInterrupt:
    print("Consumer interrupted by user")
finally:
    consumer.close()
from confluent_kafka import Consumer, KafkaException

# Kafka configuration
consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'sensor-consumer-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_config)
topic = "sensor-events"
consumer.subscribe([topic])

print(f"Subscribed to topic: {topic}")

try:
    while True:
        msg = consumer.poll(1.0)  # Poll for new messages
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        else:
            print(f"Received message: {msg.value().decode('utf-8')}")

except KeyboardInterrupt:
    print("Consumer interrupted by user")
finally:
    consumer.close()
