from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import time, random, json

app = FastAPI()

def generate_sensor_data():
    """Generator that yields fake IoT sensor readings"""

    temperature = 25.0  # starting temperature
    humidity = 50.0     # starting humidity

    while True:
        # Add SSE heartbeats with 10% chance for testing
        if random.random() < 0.1:   
            yield ": heartbeat\n\n"
            time.sleep(1)
            continue
        
        # Add invalid json event with 5% for testing
        if random.random() < 0.05:
            yield "data: {bad_json_event}\n\n"
            time.sleep(1)
            continue

        # Valid event
        # Gradually vary temperature by ±0.2°C per step
        temperature += random.uniform(-0.2, 0.2)
        temperature = max(15.0, min(35.0, temperature))  # clamp to realistic range

        # Gradually vary humidity by ±0.5% per step
        humidity += random.uniform(-0.5, 0.5)
        humidity = max(30.0, min(70.0, humidity))  # clamp to realistic range

        data = {
            "device_id": f"sensor-00{random.randint(1, 4)}",
            "timestamp": time.time(),
            "temperature": round(random.uniform(20, 30), 2),
            "humidity": round(random.uniform(40, 60), 2)
        }
        yield f"data: {json.dumps(data)}\n\n"  # SSE format
        time.sleep(2)  # new reading every second

@app.get("/stream")
def stream_sensor_data():
    """Stream real-time sensor data"""
    return StreamingResponse(generate_sensor_data(), media_type="text/event-stream")
