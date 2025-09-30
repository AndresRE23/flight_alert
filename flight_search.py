import requests
import os
from dotenv import load_dotenv

class FlightSearch:

    def __init__(self):
        load_dotenv()
        self.endpoint = "https://test.api.amadeus.com/v1/security/oauth2/token"
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")
        self.token = self.get_new_token()

    def get_destination_code(self, city_name):
        endpoint = f"https://test.api.amadeus.com/v1/reference-data/locations?subType=CITY&keyword={city_name}"

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        response = requests.get(endpoint, headers=headers)

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