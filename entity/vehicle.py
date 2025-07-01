class Vehicle:
    def __init__(self, vehicle_id=None, model=None, make=None, year=None, color=None,
                 registration_number=None, availability=True, daily_rate=None):
        self.__vehicle_id = vehicle_id
        self.__model = model
        self.__make = make
        self.__year = year
        self.__color = color
        self.__registration_number = registration_number
        self.__availability = availability
        self.__daily_rate = daily_rate

    # Getters
    @property
    def vehicle_id(self):
        return self.__vehicle_id

    @property
    def model(self):
        return self.__model

    @property
    def make(self):
        return self.__make

    @property
    def year(self):
        return self.__year

    @property
    def color(self):
        return self.__color

    @property
    def registration_number(self):
        return self.__registration_number

    @property
    def availability(self):
        return self.__availability

    @property
    def daily_rate(self):
        return self.__daily_rate

    # Setters
    @vehicle_id.setter
    def vehicle_id(self, value):
        self.__vehicle_id = value

    @model.setter
    def model(self, value):
        self.__model = value

    @make.setter
    def make(self, value):
        self.__make = value

    @year.setter
    def year(self, value):
        self.__year = value

    @color.setter
    def color(self, value):
        self.__color = value

    @registration_number.setter
    def registration_number(self, value):
        self.__registration_number = value

    @availability.setter
    def availability(self, value):
        self.__availability = value

    @daily_rate.setter
    def daily_rate(self, value):
        self.__daily_rate = value

    def __str__(self):
        return (f"Vehicle ID: {self.__vehicle_id}, Model: {self.__model}, Make: {self.__make}, "
                f"Year: {self.__year}, Color: {self.__color}, Available: {'Yes' if self.__availability else 'No'}, "
                f"Daily Rate: ${self.__daily_rate:.2f}")