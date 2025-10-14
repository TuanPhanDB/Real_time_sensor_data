Reasons to use Kafka
- Robust in handling real-time large data
- Streaming data
- Responding to changes in environmental conditions
- IoT ecosystems often involve a wide variety of devices and sensors, each producing data in different formats and protocols
- https://cimpleo.com/blog/kafka-in-iot-revolutionizing-data-management-for-connected-devices/

1. Install Kafka, Cassandra, and PostgreSQL in Docker
 - mkdir kafka-kraft
 - Create a YAML compose file
 - docker compose up -d
 - Access to Kafka bash: docker exec -it kafka bash
   - Create topics: /usr/bin/kafka-topics --create --bootstrap-server localhost:29092 --replication-factor 1 --partitions 1 --topic sensor-topic
   - List topics: /usr/bin/kafka-topics --list --bootstrap-server localhost:29092
   - Create producer: /usr/bin/kafka-console-producer --bootstrap-server localhost:29092 --topic sensor-topic
   - Open a new terminal window to create a consumer, access Kafka bash, and run consumer: /usr/bin/kafka-console-consumer --bootstrap-server localhost:29092 --topic sensor-topic --from-beginning
 - Test connection to Cassandra: docker exec -it cassandra cqlsh
 - Test connection to PostgreSQL: docker exec -it postgres psql -U admin -d testdb
2. Create env and main.py
 - Install quixstreams: pip install quixstreams
 - Make the main file and run it. Open the Kafka consumer to see the data
3. Create app.py that simulates sensor data
 - pip install fastapi uvicorn kafka-python
 - Run file: python app.py
 - Run APIg: uvicorn data_generator:app --reload
 - The data is now streamed on: http://localhost:8000/stream
4. Set up Cassandra
 - Make a file: cass-db-setup.sql
 - Every time making a change to cass-db-setup.sql, run 2 commands:
   - If table existed: docker exec -it cassandra cqlsh
   - Drop table first: DROP TABLE <name>;
   - In terminal: docker cp F:\kafka-kraft\src\cass-db-setup.sql cassandra:/cass-db-setup.sql
   - docker exec -it cassandra cqlsh -f /cass-db-setup.sql
   - 
 - cqlsh Commands:
   - DESCRIBE keyspaces  : show all keyspaces
   - USE <keyspace-name> : choose keyspace 
   - DESCRIBE TABLES     : show all tables
   - DESCRIBE TABLE <table-name> : show table info
5. Set up PostgreSQL
   - Copy script into postgres: docker cp F:\kafka-kraft\src\psql-db-setup.sql postgres:/psql-db-setup.sql
   - Execute script: docker exec -it postgres psql -U admin -d testdb -W -f /psql-db-setup.sql
   - Open postgres bash: docker exec -it postgres psql -U admin -d testdb -W
6. Grafana
   - http://localhost:3000/
7. f
8. f
9. g
10. h
11. h
12. hj
