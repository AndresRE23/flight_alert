from data_manager import DataManager
from flight_search import FlightSearch
from pprint import pprint

data_manager = DataManager()
flight_search = FlightSearch()

data_manager.get_destination_data()
data_manager.update_destination_codes()

updated_sheet_data = data_manager.get_destination_data()
pprint(updated_sheet_data)


