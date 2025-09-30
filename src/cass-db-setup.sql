CREATE KEYSPACE IF NOT EXISTS sensor_data
WITH REPLICATION = {'class': 'SimpleStrategy',
                    'replication_factor': 1};

USE sensor_data;

CREATE TABLE IF NOT EXISTS sensor_records (
    device_id TEXT,
    date TEXT, 
    timestamp TIMESTAMP,
    temperature DOUBLE,
    humidity DOUBLE,
    PRIMARY KEY ((device_id, date), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);