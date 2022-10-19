

class FlightData:
    def __init__(self, price, dep_city, dep_city_code, arr_city, arr_city_code,
                 out_date, inbound_date, link, stopovers=0, via_city=""):
        self.price = price
        self.departure_city = dep_city
        self.departure_city_code = dep_city_code
        self.arrival_city = arr_city
        self.arrival_city_code = arr_city_code
        self.departure_date = out_date
        self.return_date = inbound_date
        self.connection_city_code = via_city
        self.link = link

    def format_message(self):
        if self.connection_city_code == "":
            return f"Low Price Alert! Only ${self.price} to fly from {self.departure_city}-{self.departure_city_code}" \
                   f" to {self.arrival_city}-{self.arrival_city_code}, from {self.departure_date} to {self.return_date}" \
                   f"\nMore Info: {self.link}"

        return f"Low Price Alert! Only ${self.price} to fly from {self.departure_city} to {self.arrival_city} via " \
               f"{self.departure_city_code}-{self.connection_city_code}-{self.arrival_city_code}, from " \
               f"{self.departure_date} to {self.return_date}\nMore Info: {self.link}"
