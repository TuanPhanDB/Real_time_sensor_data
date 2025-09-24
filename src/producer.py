import requests
import json
import logging
import time
from quixstreams import Application
from requests.adapters import HTTPAdapter, Retry

# Retry when errors occur
def retry_function():
    session = requests.Session()
    retries = Retry(
        total=5,            #Total retries
        backoff_factor=1,   #Increase sleep time every retries
        status_forcelist=[500, 502, 503, 504], #Retry on these error
        allowed_methods=["GET"]
    )
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

def get_sensor_data_stream(producer):
    session = retry_function()
    """
    Connects to the FastAPI SSE endpoint and yields each JSON data event.
    """
    response = requests.get(
        "http://localhost:8000/stream", 
        stream=True, 
        timeout=(5, 30)
        )
    logging.info("Connected to SSE stream")

    # Handle SSE
    for line in response.iter_lines():
        # Ignore empty line
        if not line:
            continue
        
        # Convert raw bytes into Python string
        decoded_line = line.decode("utf-8")

        # Handling SSE heartbeats
        if decoded_line.startswith(":"):
            logging.debug("Receive SSE comment: %s", decoded_line)
            continue
        
        # SSE msg example: data:{"key": "value"}
        if decoded_line.startswith("data: "):
            try:
                data = json.loads(decoded_line[len("data: "):])
                yield data
            except json.JSONDecodeError as e:
                logging.error("Failed to decode JSON: %s", e)

                # Send bad event to Dead Letter Queue topic
                producer.produce(
                    topic="sensor-topic-dlq",
                    value=decoded_line.encode("utf-8"),
                    key=b"json_error"
                )
                producer.flush(1)

def main():
    logging.basicConfig(
        level=logging.DEBUG, 
        format="%(asctime)s [%(levelname)s] %(message)s", 
        force=True
    )

    app = Application(
        broker_address="localhost:29092",
        loglevel="DEBUG",
    )

    with app.get_producer() as producer:
        logging.info("Starting to consume SSE and produce to Kafka")
        for sensor_data in get_sensor_data_stream(producer):
            logging.debug("Got sensor data: %s", sensor_data)

            # Use sensor_id as key
            key = str(sensor_data.get("device_id", "unknown")).encode("utf-8")

            producer.produce(
                topic="sensor-topic",
                key=key,
                value=json.dumps(sensor_data).encode("utf-8"),
            )
            logging.info("Produced data to Kafka")

            # Optional: remove sleep for real-time streaming
            time.sleep(0.1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
