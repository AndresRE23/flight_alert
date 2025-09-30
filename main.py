from data_manager import DataManager
from pprint import pprint

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()

data_manager.update_destination_codes()

updated_sheet_data = data_manager.get_destination_data()
pprint(updated_sheet_data)


