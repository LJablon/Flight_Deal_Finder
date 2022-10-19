import requests
from credentials import *
from datetime import datetime as dt, timedelta
from flight_data import FlightData


class FlightSearch:
    def __init__(self):
        self.header = {
            "apikey": TEQUILA_API_KEY,
        }

    def get_destination_code(self, city_name):
        config = {
            "term": city_name
        }
        response = requests.get(url=TEQUILA_ENDPOINT, headers=self.header, params=config)
        response.raise_for_status()
        return (response.json()["locations"][0]["code"])

    def find_flights(self, city_code, max_price, origin_city="LAX"):
        min_date = dt.now() + timedelta(days=1)
        max_date = dt.now() + timedelta(days=185)

        config = {
            "fly_from": origin_city,
            "fly_to": city_code,
            "date_from": min_date.strftime("%d/%m/%Y"),
            "date_to": max_date.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "curr": "USD",
            "limit": 180,
            "price_to": max_price,
            "max_stopovers": 0,
        }

        one_stop_found = False
        response = requests.get(url=PRICE_TEQUILA_ENDPOINT, headers=self.header, params=config)
        response.raise_for_status()
        try:
            data = response.json()["data"][0]
            print("Found")
            print(data)
        except IndexError:
            config["max_stopovers"] = 1
            response = requests.get(url=PRICE_TEQUILA_ENDPOINT, headers=self.header, params=config)
            response.raise_for_status()
            try:
                data = response.json()["data"][0]
                print(data)
                one_stop_found = True
            except IndexError:
                print(f"There are no flights under the price of {max_price} to {city_code}.")
                return None

        # retrieving the desired data for the flight data class
        temp = data["dTime"]
        out_date = dt.fromtimestamp(float(temp))
        out_date = out_date.strftime("%m/%d/%y")
        temp1 = data["route"][1]["dTime"]
        return_date = dt.fromtimestamp(float(temp1))
        return_date = return_date.strftime("%m/%d/%y")
        print(return_date)
        price = data["price"]
        dep_city_code = data["flyFrom"]
        arr_city_code = data["flyTo"]
        dep_city = data["cityFrom"]
        arr_city = data["cityTo"]
        link = data["deep_link"]
        if one_stop_found:
            via_city = data["route"][0]["flyTo"]
            arr_city_code = data["route"][1]["flyTo"]
            return_date = dt.fromtimestamp(float(data["route"][2]["dTime"]))
            return_date = return_date.strftime("%m/%d/%y")
        else:
            via_city = ""

        flightData = FlightData(price=price, dep_city=dep_city, dep_city_code=dep_city_code, arr_city=arr_city,
                                arr_city_code=arr_city_code, out_date=out_date, link=link,
                                via_city=via_city, inbound_date=return_date)

        return flightData.format_message()

