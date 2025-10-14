from datetime import datetime, timezone, timedelta
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import pandas as pd
from sqlalchemy import create_engine

#Cassandra connection
auth_provider = PlainTextAuthProvider(username='admin', password='admin123')
cassandra_cluster = Cluster(["localhost"], auth_provider=auth_provider)
cassandra_session = cassandra_cluster.connect()
cassandra_session.set_keyspace("sensor_data")

# Connection parameters
user="admin"
password="admin123"
host ="localhost"
database="testdb"
port=5432

#SQL connection
sql_connection = f"postgresql://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(sql_connection)


#Get last hour to aggregate data for PostgreSQL
cur = datetime.now()

# Start and end of yesterday
window_start = (cur - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
window_end = (window_start + timedelta(days=1))

print(cur, window_start, window_end)

#Prepare Query
query = f"""
    SELECT 
        device_id, 
        date, 
        timestamp, 
        temperature, 
        humidity
    FROM sensor_records
    WHERE date = '{window_start.strftime('%Y-%m-%d')}'
        AND timestamp >= '{window_start.isoformat()}'
        AND timestamp < '{window_end.isoformat()}'
    ALLOW FILTERING
"""
rows = cassandra_session.execute(query)
df = pd.DataFrame(rows)
print(df)

if not df.empty:
    df['start_time'] = df['timestamp'].dt.floor('min')

    agg = (
        df.groupby(['device_id', 'start_time']).agg(
            avg_temp=('temperature', 'mean'),
            min_temp=('temperature', 'min'),
            max_temp=('temperature', 'max'),
            avg_humidity=('humidity', 'mean'),
            count=('temperature', 'count'))
        .reset_index()
    )

    agg.to_sql('sensor_aggregates', engine, if_exists='append', index=False, chunksize=1000)

    print(f"Wrote {len(agg)} aggregates from {window_start} → {window_end}")
else:
    print("No new data found.")