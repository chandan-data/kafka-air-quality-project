# Kafka Air Quality Monitoring Project

This project demonstrates an end-to-end real-time data pipeline using **Kafka**, **PostgreSQL**, and **Python** to monitor air quality data from an API.

## 🔧 Technologies Used

- Apache Kafka
- Python
- PostgreSQL
- Kafka-Python
- psycopg2
- dotenv
- Email Alerts via SMTP

## 📦 Features

- Fetch air quality data from API
- Produce and consume data using Kafka
- Store data in PostgreSQL
- Trigger email alerts if PM2.5 exceeds a threshold

## 🚀 How to Run

1. Clone the repository
2. Set up `.env` in the `config/` folder
3. Run the producer, consumer, and email alert scripts
4. Check your PostgreSQL DB for updates

## ⚠️ Alert Rule

- Email is sent if **PM2.5 > 100**

## 📁 Project Structure

kafka-air-quality-project/
├── producer/
│ └── fetch_data.py
├── consumer/
│ └── save_to_db.py
├── alerts/
│ └── email_alert.py
├── config/
│ └── .env
├── README.md


## ⚙️ How It Works

1. `fetch_data.py` fetches AQI data every few seconds for 15+ Indian cities.
2. Data is pushed to a Kafka topic named `air_quality`.
3. `save_to_db.py` consumes the data and stores it in PostgreSQL.
4. If PM2.5 > 100, `email_alert.py` triggers an alert email.

---

## 📧 Email Alerts

Email is triggered if:
PM2.5 > 100

