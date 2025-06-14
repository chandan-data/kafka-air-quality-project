import json, os
import psycopg2
from kafka import KafkaConsumer
from dotenv import load_dotenv
from alerts.email_alert import send_email_alert
from pathlib import Path

env_path = Path(__file__).resolve().parents[1] / 'config' / '.env'
load_dotenv(dotenv_path=env_path)

consumer = KafkaConsumer(
    "air_quality",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cursor = conn.cursor()

cursor.execute(""" 
CREATE TABLE IF NOT EXISTS air_quality (
    city TEXT,
    timestamp TEXT,
    aqi INTEGER,
    pm2_5 REAL,
    pm10 REAL,
    co REAL
 );               
""")

conn.commit()

for message in consumer:
    data = message.value
    print("Received", data)
 
    cursor.execute("""
    INSERT INTO air_quality (city, timestamp, aqi, pm2_5, pm10, co)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (
    data["city"],
    data["timestamp"],
    data["aqi"],
    data["pm2_5"],
    data["pm10"],
    data["co"]
    ))
    
    conn.commit()
    
    # Enail Alert
    if data["pm2_5"] > 100:
        send_email_alert(data["city"], data["pm2_5"])