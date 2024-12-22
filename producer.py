from prometheus_client import start_http_server, Counter, Summary, Gauge
from confluent_kafka import Producer
import time
import random

# Start Prometheus metrics server on a custom port
METRIC_PORT = 8000
start_http_server(METRIC_PORT)

# Define Prometheus metrics
events_sent = Counter('sensor_events_sent_total', 'Total number of events sent by the sensor')
event_errors = Counter('sensor_event_errors_total', 'Total number of event errors')
event_processing_time = Summary('sensor_event_processing_time_seconds', 'Time taken to process an event')
sensor_status = Gauge('sensor_status', 'Status of the sensor (1=up, 0=down)')

# Kafka configuration
producer_config = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'sensor-producer'
}
producer = Producer(producer_config)

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed for record {msg.key()}: {err}")
        event_errors.inc()  # Increment error count on failure
    else:
        print(f"Record {msg.key()} successfully produced to {msg.topic()}")

# Dummy events
topic = "sensor-events"

# Set the sensor status to 'up'
sensor_status.set(1)

try:
    for i in range(20):
        # Simulate event creation
        start_time = time.time()
        event = {
            "event_type": "dummy_event",
            "timestamp": time.time(),
            "message": f"Dummy event {i}"
        }

        # Produce the event
        producer.produce(topic, key=str(i), value=str(event), callback=delivery_report)
        producer.poll(0)  # Serve delivery reports

        # Simulate processing delay
        time.sleep(random.uniform(0.1, 0.5))

        # Track processing time
        event_processing_time.observe(time.time() - start_time)

        # Increment events sent metric
        events_sent.inc()

except KeyboardInterrupt:
    print("Sensor stopped by user")

finally:
    # Set the sensor status to 'down'
    sensor_status.set(0)
    producer.flush()
