import requests
import os
from dotenv import load_dotenv

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        load_dotenv()
        self.sheety_endpoint = os.getenv("SHEETY_ENDPOINT")
        self.sheet_data = {}

    def get_destination_data(self):
        response = requests.get(self.sheety_endpoint)
        data = response.json()
        self.sheet_data = data["prices"]
        return self.sheet_data
