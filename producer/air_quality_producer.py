import requests, json, time, os
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv("../config/.env")

API_KEY = os.getenv("API_KEY")

cities = [
    {"name": "Delhi", "lat": 28.6139, "lon": 77.2090},
    {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777},
    {"name": "Bengaluru", "lat": 12.9716, "lon": 77.5946},
    {"name": "Kolkata", "lat": 22.5726, "lon": 88.3639},
    {"name": "Chennai", "lat": 13.0827, "lon": 80.2707},
    {"name": "Hyderabad", "lat": 17.3850, "lon": 78.4867},
    {"name": "Ahmedabad", "lat": 23.0225, "lon": 72.5714},
    {"name": "Pune", "lat": 18.5204, "lon": 73.8567},
    {"name": "Jaipur", "lat": 26.9124, "lon": 75.7873},
    {"name": "Lucknow", "lat": 26.8467, "lon": 80.9462},
    {"name": "Bhopal", "lat": 23.2599, "lon": 77.4126},
    {"name": "Patna", "lat": 25.5941, "lon": 85.1376},
    {"name": "Indore", "lat": 22.7196, "lon": 75.8577},
    {"name": "Nagpur", "lat": 21.1458, "lon": 79.0882},
    {"name": "Chandigarh", "lat": 30.7333, "lon": 76.7794}
]

producer = KafkaProducer(
    bootstrap_servers = 'localhost:9092',
    value_serializer = lambda v: json.dumps(v).encode("utf-8")
)

while True:
    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={city['lat']}&lon={city['lon']}&appid={API_KEY}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            entry = data['list'][0]
            message = {
                "city": city['name'],
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "aqi": entry["main"]["aqi"],
                "pm2_5": entry["components"]["pm2_5"],
                "pm10": entry["components"]["pm10"],
                "co": entry["components"]["co"]
            }
            producer.send("air_quality",value=message)
            print("Sent to Kafka",message)
            
        else:
            print("Failed for City:",city["name"])
            
    time.sleep(60)