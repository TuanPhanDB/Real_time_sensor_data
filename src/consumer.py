import requests
import json
import logging
import time
from quixstreams import Application
from cassandra.cluster import Cluster
from cassandra.concurrent import execute_concurrent
from cassandra.auth import PlainTextAuthProvider
from datetime import datetime, timezone
import pandas as pd

#Cassandra connection
auth_provider = PlainTextAuthProvider(username='admin', password='admin123')
cassandra_cluster = Cluster(["localhost"], auth_provider=auth_provider)
cassandra_session = cassandra_cluster.connect()
cassandra_session.set_keyspace("sensor_data")

#Prepare Query
query = cassandra_session.prepare(
"""
    INSERT INTO sensor_records (device_id, date, timestamp, temperature, humidity)
    VALUES (?, ?, ?, ?, ?)

"""    
)

#Batch config
BATCH_SIZE = 100    #rows
BATCH_INTERVAL = 5  #seconds

buffer = []
last_flush_time = time.time()

def flush_batch():
    global buffer, last_flush_time
    if not buffer:
        return
    
    logging.info("Flushing %d events to Cassandra...", len(buffer))

    #Flush concurrent events 
    try:
        results = execute_concurrent(cassandra_session, buffer, concurrency=20)
        #result examples:
        #(True, <cassandra.cluster.ResultSet object at 0x7...>)
        #(False, Error: ...)
        #Value Trur/False come from execute_concurrent
        failed = [r for r in results if not r[0]]
        if failed:
            logging.error("Some inserts failed: %s", failed)
        else:
            logging.debug("Batch insert successful.")
    except Exception as e:
        logging.exception("Batch insert failed: %s", e)

    #Reset buffer and last_flush_time
    buffer = []
    last_flush_time = time.time()

def process_valid_msg(msg):
    global buffer, last_flush_time

    value = json.loads(msg.value())

    #Convert timestamp float → datetime (Cassandra "timestamp" column)
    ts = datetime.fromtimestamp(float(value["timestamp"]), timezone.utc)
    date_str = ts.strftime("%Y-%m-%d")

    buffer.append((
        query, 
        (
        value["device_id"], date_str, ts, float(value["temperature"]), float(value["humidity"])
        )
    ))

    #Flush if batch size or time exceed
    if len(buffer) >= BATCH_SIZE or (time.time() - last_flush_time) > BATCH_INTERVAL:
        flush_batch()

#DLQ = Dead Letter Queue
def process_dlq_msg(msg):
    raw_msg = msg.value().decode("utf-8", errors="ignore")
    logging.warning("DLQ event: %s", raw_msg)

def main():
    #Set log level and format logs
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        force=True,
    )
    app = Application(
        broker_address="localhost:29092",
        loglevel="DEBUG",
        consumer_group="sensor_reader",
        auto_offset_reset="earliest" #Start from the very beginning of the process
    )

    with app.get_consumer() as consumer:
        consumer.subscribe(["sensor-topic", "sensor-topic-dlq"])

        try:
            while True:
                msg = consumer.poll(1)    #Fetch msg every 1 second

                if msg is None:
                    flush_batch()
                    continue

                if msg.error() is not None:
                    logging.error("Kafka error: %s", msg.error())
                    continue

                #Process msg into correspond topic
                topic = msg.topic()
                if topic == "sensor-topic":
                    process_valid_msg(msg)
                elif topic == "sensor-topic-dlq":
                    process_dlq_msg(msg)

                consumer.store_offsets(msg)

        finally:
            #Final flush before shut down
            flush_batch()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        flush_batch()
        pass