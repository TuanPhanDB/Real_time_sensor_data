import requests
import json
import logging
import time
from quixstreams import Application

def get_sensor_data_stream():
    """
    Connects to the FastAPI SSE endpoint and yields each JSON data event.
    """
    response = requests.get("http://localhost:8000/stream", stream=True)
    logging.info("Connected to SSE stream")

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode("utf-8")
            if decoded_line.startswith("data: "):
                try:
                    data = json.loads(decoded_line[len("data: "):])
                    yield data
                except json.JSONDecodeError as e:
                    logging.error("Failed to decode JSON: %s", e)

def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s", force=True)

    app = Application(
        broker_address="localhost:29092",
        loglevel="DEBUG",
    )

    with app.get_producer() as producer:
        logging.info("Starting to consume SSE and produce to Kafka")
        for sensor_data in get_sensor_data_stream():
            logging.debug("Got sensor data: %s", sensor_data)
            producer.produce(
                topic="test-topic",
                value=json.dumps(sensor_data),
            )
            logging.info("Produced data to Kafka")
            # Optional: remove sleep for real-time streaming
            time.sleep(0.1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
