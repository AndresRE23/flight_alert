from data_manager import DataManager
from flight_search import FlightSearch
from pprint import pprint

data_manager = DataManager()
flight_search = FlightSearch()
sheet_data = data_manager.get_destination_data()

for flight in sheet_data:
    if flight['iataCode'] == "":
        code = flight_search.get_destination_code(flight['city'])
        flight["iataCode"] = code

pprint(sheet_data)


