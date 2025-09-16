import requests
import json
import logging
import time
from quixstreams import Application

def main():
    app = Application(
        broker_address="localhost:29092",
        loglevel="DEBUG",
        consumer_group="sensor_reader",
    )

    with app.get_consumer() as consumer:
        consumer.subscribe(["test-topic"])

        while True:
            msg = consumer.poll(1)    #Fetch msg every 1 second

            if msg is None:
                print("Waiting... ")
            elif msg.error() is not None:
                raise Exception(msg.error())
            else:
                key = msg.key()
                value = json.loads(msg.value())
                offset = msg.offset()

                print(f"{offset} {key} {value}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass