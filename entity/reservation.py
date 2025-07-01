from datetime import datetime


class Reservation:
    def __init__(self, reservation_id=None, customer_id=None, vehicle_id=None,
                 start_date=None, end_date=None, total_cost=None, status="Pending"):
        self.__reservation_id = reservation_id
        self.__customer_id = customer_id
        self.__vehicle_id = vehicle_id
        self.__start_date = start_date
        self.__end_date = end_date
        self.__total_cost = total_cost
        self.__status = status

    # Getters
    @property
    def reservation_id(self):
        return self.__reservation_id

    @property
    def customer_id(self):
        return self.__customer_id

    @property
    def vehicle_id(self):
        return self.__vehicle_id

    @property
    def start_date(self):
        return self.__start_date

    @property
    def end_date(self):
        return self.__end_date

    @property
    def total_cost(self):
        return self.__total_cost

    @property
    def status(self):
        return self.__status

    # Setters
    @reservation_id.setter
    def reservation_id(self, value):
        self.__reservation_id = value

    @customer_id.setter
    def customer_id(self, value):
        self.__customer_id = value

    @vehicle_id.setter
    def vehicle_id(self, value):
        self.__vehicle_id = value

    @start_date.setter
    def start_date(self, value):
        self.__start_date = value

    @end_date.setter
    def end_date(self, value):
        self.__end_date = value

    @total_cost.setter
    def total_cost(self, value):
        self.__total_cost = value

    @status.setter
    def status(self, value):
        self.__status = value

    def calculate_total_cost(self, daily_rate):
        if self.__start_date and self.__end_date and daily_rate:
            days = (self.__end_date - self.__start_date).days
            self.__total_cost = days * daily_rate
            return self.__total_cost
        return 0

    def __str__(self):
        return (f"Reservation ID: {self.__reservation_id}, Customer ID: {self.__customer_id}, "
                f"Vehicle ID: {self.__vehicle_id}, From: {self.__start_date} To: {self.__end_date}, "
                f"Total Cost: ${self.__total_cost:.2f}, Status: {self.__status}")