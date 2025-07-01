from datetime import date


class Admin:
    def __init__(self, admin_id=None, first_name=None, last_name=None, email=None,
                 phone_number=None, username=None, password=None, role=None, join_date=None):
        self.__admin_id = admin_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__phone_number = phone_number
        self.__username = username
        self.__password = password
        self.__role = role
        self.__join_date = join_date or date.today()

    # Getters
    @property
    def admin_id(self):
        return self.__admin_id

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
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @property
    def role(self):
        return self.__role

    @property
    def join_date(self):
        return self.__join_date

    # Setters
    @admin_id.setter
    def admin_id(self, value):
        self.__admin_id = value

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

    @username.setter
    def username(self, value):
        self.__username = value

    @password.setter
    def password(self, value):
        self.__password = value

    @role.setter
    def role(self, value):
        self.__role = value

    @join_date.setter
    def join_date(self, value):
        self.__join_date = value

    def authenticate(self, password):
        return self.__password == password

    def __str__(self):
        return (f"Admin ID: {self.__admin_id}, Name: {self.__first_name} {self.__last_name}, "
                f"Role: {self.__role}, Username: {self.__username}")