from prometheus_client import start_http_server, Counter
from confluent_kafka import Producer
import time
import json

# Start Prometheus metrics server
METRIC_PORT = 8000  # Change if needed
start_http_server(METRIC_PORT)

# Define Prometheus metrics
events_sent = Counter('events_sent_total', 'Total number of events sent by the sensor')

# Kafka configuration
producer_config = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'sensor-producer'
}

producer = Producer(producer_config)

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed for record {msg.key()}: {err}")
    else:
        print(f"Record {msg.key()} successfully produced to {msg.topic()}")

# Generate dummy events
topic = "sensor-events"
for i in range(10):
    event = {
        "event_type": "dummy_event",
        "timestamp": time.time(),
        "message": f"Dummy event {i}"
    }
    producer.produce(topic, key=str(i), value=json.dumps(event), callback=delivery_report)
    producer.poll(0)  # Serve delivery reports
    
    # Increment Prometheus metric
    events_sent.inc()
    
    time.sleep(1)  # Simulate periodic events

producer.flush()
