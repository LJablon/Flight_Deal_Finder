import requests
from credentials import *


class CustomerData:
    def __init__(self):
        self.customer_count = 0

    def get_customer_emails(self):
        response = requests.get(url=CUSTOMERS_GOOGLE_SHEET_ENDPOINT)
        response.raise_for_status()
        self.customer_count = len(response.json()["customers"])
        return response.json()["customers"]

    def put_customer_data(self):
        first_name = input("Please enter your first name: ")
        last_name = input("Please enter your last name: ")
        email_address = input("Please enter your email address: ")
        confirm_email = input("Please re-enter your email address: ")
        customer_data = {
            "customer": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email_address
            }
        }
        if email_address == confirm_email:
            response = requests.post(url=CUSTOMERS_GOOGLE_SHEET_ENDPOINT, json=customer_data)
            response.raise_for_status()
        else:
            print("Emails do not match")
            self.put_customer_data()

