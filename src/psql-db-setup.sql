CREATE TABLE IF NOT EXISTS sensor_aggregates (
    device_id TEXT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    avg_temp DOUBLE PRECISION,
    min_temp DOUBLE PRECISION,
    max_temp DOUBLE PRECISION,
    avg_humidity DOUBLE PRECISION,
    count INT,
    PRIMARY KEY (device_id, start_time)
);
