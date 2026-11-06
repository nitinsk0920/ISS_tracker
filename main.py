import requests
from datetime import datetime
import smtplib
from dotenv import load_dotenv
import os
import time

load_dotenv()

mail=os.environ.get("EMAIL")
password=os.environ.get("PASSWORD")

MY_LAT = 15.458924 # Your latitude
MY_LONG = 75.007805 # Your longitude


def issoverhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT+5 >= iss_latitude >= MY_LAT-5 and MY_LONG+5 >= iss_longitude >= MY_LONG-5:
        return True

def iss_night():
    parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
                }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour
    if time_now <= sunrise and time_now >= sunset:
        return True

def send_email():
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(user=mail, password=password)
        connection.sendmail(from_addr=mail, to_addrs=mail, msg=f"subject: Look up 👆\n\n iss 🛰️ has reached your location at {datetime.now()} in the sky")
    print("Email sent")

prev_cond= False
while True:
    time.sleep(60)
    try:
        cond= issoverhead() and iss_night()
        if cond and not prev_cond:
            send_email()
        prev_cond = cond

    except Exception as error:
        print(f"Error: {error}")

# BONUS: run the code every 60 seconds.



