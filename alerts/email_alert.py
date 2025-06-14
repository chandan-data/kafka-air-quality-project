import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv("../config/.env")

def send_email_alert(city,pm25):
    sender = os.getenv("EMAIL_USER")
    receiver = os.getenv("ALERT_RECEIVER")
    password = os.getenv("EMAIL_PASS")
    
    # Create the subject and body of the email
    subject = f"High PM2.5 Alert in {city}"
    body = f"PM2.5 level in city {city} has reached {pm25} µg/m³. Take precautions!"
    
    # Creats the email message using MIMEText
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver
    
    try:
        with smtplib.SMTP(os.getenv("EMAIL_HOST"), int(os.getenv("EMAIL_PORT"))) as server:
            server.starttls()
            server.login(sender,password)
            server.sendmail(sender,receiver,msg.as_string())
            print(f"Email alert sent to {receiver}")
    except Exception as e:
        print(f"Failed to sent: ",e)