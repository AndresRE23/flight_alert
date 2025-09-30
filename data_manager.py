import requests
import os
from dotenv import load_dotenv
from flight_search import FlightSearch

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

    def update_destination_codes(self):
        endpoint = self.sheety_endpoint
        flight_search = FlightSearch()

        for data in self.sheet_data:
            if data["iataCode"] == "":
                code = flight_search.get_destination_code(data["city"])
                id = data["id"]
                data["iataCode"] = code

                body = {
                    "price": {
                        "iataCode": code
                    }
                }

                response = requests.put(url=f"{endpoint}/{id}", json=body)
                print(response.text)



