CREATE KEYSPACE IF NOT EXISTS sensor_data
WITH REPLICATION = {'class': 'SimpleStrategy',
                    'replication_factor': 1};

USE sensor_data;

CREATE TABLE IF NOT EXISTS sensor_records (
    device_id TEXT,
    timestamp TIMESTAMP,
    temperature FLOAT,
    humidity FLOAT,
    PRIMARY KEY (device_id, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);