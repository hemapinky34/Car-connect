from datetime import date


class Customer:
    def __init__(self, customer_id=None, first_name=None, last_name=None, email=None,
                 phone_number=None, address=None, username=None, password=None,
                 registration_date=None):
        self.__customer_id = customer_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__phone_number = phone_number
        self.__address = address
        self.__username = username
        self.__password = password
        self.__registration_date = registration_date or date.today()

    # Getters
    @property
    def customer_id(self):
        return self.__customer_id

    @property
    def first_name(self):
        return self.__first_name

    @property
    def last_name(self):
        return self.__last_name

    @property
    def email(self):
        return self.__email

    @property
    def phone_number(self):
        return self.__phone_number

    @property
    def address(self):
        return self.__address

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @property
    def registration_date(self):
        return self.__registration_date

    # Setters
    @customer_id.setter
    def customer_id(self, value):
        self.__customer_id = value

    @first_name.setter
    def first_name(self, value):
        self.__first_name = value

    @last_name.setter
    def last_name(self, value):
        self.__last_name = value

    @email.setter
    def email(self, value):
        self.__email = value

    @phone_number.setter
    def phone_number(self, value):
        self.__phone_number = value

    @address.setter
    def address(self, value):
        self.__address = value

    @username.setter
    def username(self, value):
        self.__username = value

    @password.setter
    def password(self, value):
        self.__password = value

    @registration_date.setter
    def registration_date(self, value):
        self.__registration_date = value

    def authenticate(self, password):
        return self.__password == password

    def __str__(self):
        return (f"Customer ID: {self.__customer_id}, Name: {self.__first_name} {self.__last_name}, "
                f"Email: {self.__email}, Username: {self.__username}")