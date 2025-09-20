import requests
import json
import logging
import time
from quixstreams import Application
from cassandra.cluster import Cluster
#import psycopg2
from datetime import datetime

#Cassandra connection
cassandra_cluster = Cluster(["localhost"])
cassandra_session = cassandra_cluster.connect()
cassandra_session.set_keyspace("sensor_data")

def main():
    app = Application(
        broker_address="localhost:29092",
        loglevel="DEBUG",
        consumer_group="sensor_reader",
        auto_offset_reset="earliest" #Start from the very beginning of the process
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
                #consumer.store_offset(msg)

                # Insert data into Cassandra
                # Convert timestamp float → datetime (Cassandra "timestamp" column)
                ts = datetime.fromtimestamp(float(value["timestamp"]))

                query = cassandra_session.prepare("INSERT INTO sensor_records (device_id, timestamp, temperature, humidity) VALUES (?, ?, ?, ?)")
                cassandra_session.execute(query, (
                    value["device_id"], 
                    ts, 
                    float(value["temperature"]), 
                    float(value["humidity"])
                    ))

                print("Successful insert")
                time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass