import requests
from datetime import datetime
import smtplib
import time
import os

email = os.environ.get('email')
password = os.environ.get('password')

MY_LAT = 39.952583 # Your latitude
MY_LONG = -75.165222 # Your longitude


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the ISS position.
    return MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()

    return time_now.hour >= sunset or time_now.hour <= sunrise

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP('smtp.mail.yahoo.com', 587) as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(from_addr=email,
                                to_addrs=email,
                                msg="Subject:LOOK UP!!\n\nYou should go out and look up at the sky and wave to ISS.")
