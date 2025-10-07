import os
from dotenv import load_dotenv
import smtplib

class NotificationManager:

    def __init__(self):
        load_dotenv()
        self.mail = os.getenv("MY_EMAIL")
        self.password = os.getenv("PASSWORD")

    def send_mail(self, flight_data):
        message = f"""
            Cheap flight found!
            {flight_data.origin_airport} -> {flight_data.destination_airport}
            Price: {flight_data.price} USD
            Departure: {flight_data.out_date}
            Return: {flight_data.return_date}
            """

        with smtplib.SMTP(host="smtp.gmail.com", port=587) as cn:
            cn.starttls()
            cn.login(self.mail, self.password)
            cn.sendmail(self.mail, self.mail, message)


