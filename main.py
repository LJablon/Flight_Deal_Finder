from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from customer_data import CustomerData
from credentials import ORIGIN

# Create objects
data_manager = DataManager()

# Get location and price information
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
message_manager = NotificationManager()
customer_data_manager = CustomerData()

# Get a list of all the emails
mailing_list = customer_data_manager.get_customer_emails()

# Add customer if that is prompted
response = input("Welcome to Flight Finders\n\nPress 1 to enter a new entry or any other key to continue: ")
if response == "1":
    customer_data_manager.put_customer_data()
    mailing_list = customer_data_manager.get_customer_emails()
print(mailing_list)


if sheet_data[0]["iataCode"] == "":

    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    print(f"sheet_data:\n {sheet_data}")
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

message = ""
for row in sheet_data:
    destination = flight_search.find_flights(row["iataCode"], row["lowestPrice"])
    if destination:
        message += destination
        message += "\n\n"

message_manager.send_message(message)
message_manager.send_emails(message, mailing_list)
