from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import datetime, timedelta

data_manager = DataManager()
flight_search = FlightSearch()
notifier = NotificationManager()

sheet_data = data_manager.get_destination_data()
data_manager.update_destination_codes()
updated_sheet_data = data_manager.get_destination_data()

today = datetime.now().date()
from_date = today + timedelta(days=1)
to_date = from_date + timedelta(days=30 * 6)

departure_date_str = from_date.strftime("%Y-%m-%d")
return_date_str = to_date.strftime("%Y-%m-%d")

all_flights = []

for city_data in updated_sheet_data:
    destination_code = city_data["iataCode"]
    flight_json = flight_search.search_flights(destination_code, departure_date_str, return_date_str)
    cheapest_flight = flight_search.find_cheapest_flight(flight_json)
    all_flights.append(cheapest_flight)

    if cheapest_flight.price != "N/A" and float(cheapest_flight.price) < city_data["lowestPrice"]:
        print(f"Cheaper flight found to {city_data['city']} for {cheapest_flight.price} USD!")
        notifier.send_mail(cheapest_flight)

for flight in all_flights:
    print(f"Flight {flight.origin_airport} -> {flight.destination_airport}")
    print(f"Price: {flight.price}")
    print(f"Departure: {flight.out_date}")
    print(f"Return: {flight.return_date}")
    print("----------------------------")






