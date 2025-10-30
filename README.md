## Real-time Sensor Data

This project simulates an IoT data pipeline for monitoring and controlling temperature and humidity in environments such as greenhouses, warehouses, or smart homes.

It demonstrates how to generate, stream, store, and visualize sensor data in real time using **Kafka**, **Cassandra**, **PostgreSQL**, and **Grafana**.

### 🧠 Overview

**Core features:**

- Simulate real-time IoT sensor data with **FastAPI**.

- Stream data through **Apache Kafka**.

- Store raw data in **Cassandra** and aggregated data in **PostgreSQL**.

- Visualize live metrics with **Grafana** dashboards.

### 📂 Project Structure

```bash
├── database-setup/
│   ├── cass_db_setup.sql      # Set-up for Cassandra database
│   └── psql_db_setup.sql      # Set-up for PostgreSQL database
│
├── src/
│   ├── data_generator.py      # Generates real-time temperature/humidity data via FastAPI
│   ├── producer.py            # Publishes sensor data to Kafka topics
│   ├── consumer.py            # Consumes Kafka messages and stores data in Cassandra
│   ├── aggregate_data.py      # Aggregates raw data and writes results to PostgreSQL
│   ├── requirements.txt
│
├── docker-compose.yml         # Defines Kafka, Cassandra, PostgreSQL, and Grafana services
├── start_services.py          # Automates starting all modules (Windows PowerShell)
```

### ⚙️ Components
#### 1. Data Generator
- Simulates IoT devices producing temperature and humidity data.

- Streams data in real time using FastAPI at:

```bash
http://localhost:8000/stream
```

- Each device periodically emits JSON payloads representing sensor readings.

#### 2. Kafka Streaming Services
- **Producer:**

  Collects generated data and publishes it to Kafka topics.

- **Consumer:**

  Subscribes to Kafka topics, writes raw data to Cassandra, and aggregates metrics into PostgreSQL for analytics.

#### 3. Database
- **Cassandra:**

  Stores unprocessed, time-series sensor data for live visualization and history.

- **PostgreSQL:**

  Stores aggregated metrics for reports, analytics, and trend visualization.

#### 4. Dashboard
- Connects directly to Cassandra to display real-time temperature and humidity data per device.

- Allows configuration of thresholds, units, and time ranges for dynamic monitoring.
  
  ![dashboard](https://github.com/user-attachments/assets/5603b1d6-ef86-4514-88f6-5a942a6aaf58)

### 🚀 Getting Started
**Note:** `start_services.py` currently supports **Windows PowerShell** only.

Modify the shell commands in the script to use it on **Linux**.

#### 1. Clone the Repository
  ```terminal
  git clone https://github.com/TuanPhanDB/Real_time_sensor_data.git
  ```
#### 2. Start Required Services
  ```terminal
  docker compose up -d
  ```
#### 3. Create a Virtual Environment
  ```terminal
  py -m venv .venv
  ```
#### 4. Install Dependencies
  ```terminal
  pip install -r requirements.txt
  ```
#### 5. Start All Services
  ```terminal
  py start_services.py
  ```
This runs:
- data_generator.py
- producer.py
- consumer.py
- aggregate_data.py

### 📊 Grafana Configuration
#### 1. Access Grafana
  ```terminal
  http://localhost:3000/
  ```
  - Login: admin/admin123
#### 2. Create a New Dashboard
#### 3. Add a Dynamic Variable
- Navigate to Settings → Variables → New Variable
- Type: Query
- Name: selected_device
- Data Source: Cassandra-db
- Query:
    ```sql
    SELECT device_id FROM sensor_records;
    ```
#### 4. Add a Time-Series Visualization
- Create a new panel → Choose “Time series”.
- Use this query:
    ```sql
    SELECT 
     device_id, 
     timestamp, 
     temperature
    FROM sensor_records
    WHERE device_id = '$selected_device'
     AND timestamp >= ${__from} AND timestamp <= ${__to}
    ALLOW FILTERING;
    ```
- Set the time range to “now - 5m → now”
- Set the time zone to UTC
- Adjust thresholds, units, and display options as needed.
  
### 🧩 Tech Stack
| Layer            | Technology Used                         |
|------------------|------------------------------------------|
| Data Simulation  | Python, FastAPI                         |
| Messaging        | Apache Kafka                            |
| Storage          | Cassandra (raw), PostgreSQL (aggregated) |
| Visualization    | Grafana                                 |
| Containerization | Docker, Docker Compose                  |

### 💡 Future Improvements
- [ ] Add alerting mechanisms in Grafana for threshold breaches.
- [ ] Add report using aggregated data in PostgreSQL.
- [ ] Deploy via Kubernetes for scalability.
- [ ] Implement REST APIs for historical data retrieval.
    


  
