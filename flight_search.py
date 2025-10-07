import requests
import os
from dotenv import load_dotenv
from flight_data import FlightData

class FlightSearch:

    def __init__(self):
        load_dotenv()
        self.endpoint = "https://test.api.amadeus.com/v1/security/oauth2/token"
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")
        self.token = self.get_new_token()

        if not self.token:
            raise Exception("Failed to retrieve Amadeus token. Check your API_KEY and API_SECRET.")

        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }

    def get_destination_code(self, city_name):
        endpoint = f"https://test.api.amadeus.com/v1/reference-data/locations?subType=CITY&keyword={city_name}"

        response = requests.get(endpoint, headers=self.headers)

        if response.status_code != 200:
            print("Error:", response.text)
            return "NOT FOUND"
        else:
            data = response.json()
            if len(data["data"]) > 0:
                iata_code = data["data"][0]["iataCode"]
                return iata_code
            else:
                return "NOT FOUND"

    def get_new_token(self):
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        body = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.api_secret
        }

        response = requests.post(url=self.endpoint, headers=header, data=body)

        if response.status_code == 200:
            token = response.json()["access_token"]
            return token
        else:
            print("Error obtaining token:", response.text)
            return None

    def search_flights(self, destination_code, from_date, to_date):
        endpoint = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        params = {
            "originLocationCode": "SJO",
            "destinationLocationCode": destination_code,
            "departureDate": from_date,
            "returnDate": to_date,
            "adults": 4,
            "nonStop": "false",
            "currencyCode": "USD"
        }

        response = requests.get(endpoint, headers=self.headers, params=params)
        if response.status_code != 200:
            print("Error:", response.text)
            return None
        else:
            return response.json()

    def find_cheapest_flight(self, flight_json):
        try:
            if "data" not in flight_json or len(flight_json["data"]) == 0:
                return FlightData("N/A", "N/A", "N/A", "N/A", "N/A")

            cheapest = flight_json["data"][0]
            price = cheapest["price"]["total"]

            origin_airport = cheapest["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            destination_airport = cheapest["itineraries"][0]["segments"][-1]["arrival"]["iataCode"]

            out_date = cheapest["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            return_date = cheapest["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

            return FlightData(price, origin_airport, destination_airport, out_date, return_date)

        except Exception as e:
            print("Error parsing flight data:", e)
            return FlightData("N/A", "N/A", "N/A", "N/A", "N/A")



