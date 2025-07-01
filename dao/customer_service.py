import mysql.connector
from entity.customer import Customer
from exception.authentication_exception import AuthenticationException
from exception.invalid_input_exception import InvalidInputException
from util.db_conn_util import DBConnUtil
from util.db_property_util import DBPropertyUtil


class CustomerService:
    def __init__(self):
        self.__connection_string = DBPropertyUtil.get_connection_string('db_config.properties')

    def get_customer_by_id(self, customer_id):
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM Customer WHERE CustomerID = %s"
            cursor.execute(query, (customer_id,))
            customer_data = cursor.fetchone()

            if customer_data:
                customer = Customer(
                    customer_id=customer_data['CustomerID'],
                    first_name=customer_data['FirstName'],
                    last_name=customer_data['LastName'],
                    email=customer_data['Email'],
                    phone_number=customer_data['PhoneNumber'],
                    address=customer_data['Address'],
                    username=customer_data['Username'],
                    password=customer_data['Password'],
                    registration_date=customer_data['RegistrationDate']
                )
                return customer
            else:
                return None
        except Exception as e:
            raise Exception(f"Error getting customer by ID: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_customer_by_username(self, username):
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM Customer WHERE Username = %s"
            cursor.execute(query, (username,))
            customer_data = cursor.fetchone()

            if customer_data:
                customer = Customer(
                    customer_id=customer_data['CustomerID'],
                    first_name=customer_data['FirstName'],
                    last_name=customer_data['LastName'],
                    email=customer_data['Email'],
                    phone_number=customer_data['PhoneNumber'],
                    address=customer_data['Address'],
                    username=customer_data['Username'],
                    password=customer_data['Password'],
                    registration_date=customer_data['RegistrationDate']
                )
                return customer
            else:
                return None
        except Exception as e:
            raise Exception(f"Error getting customer by username: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def register_customer(self, customer_data):
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor()

            # Check if username or email already exists
            check_query = "SELECT COUNT(*) FROM Customer WHERE Username = %s OR Email = %s"
            cursor.execute(check_query, (customer_data.username, customer_data.email))
            count = cursor.fetchone()[0]

            if count > 0:
                raise InvalidInputException("Username or email already exists")

            insert_query = """
                INSERT INTO Customer (FirstName, LastName, Email, PhoneNumber, Address, Username, Password, RegistrationDate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                customer_data.first_name,
                customer_data.last_name,
                customer_data.email,
                customer_data.phone_number,
                customer_data.address,
                customer_data.username,
                customer_data.password,
                customer_data.registration_date
            ))

            connection.commit()
            return cursor.lastrowid
        except Exception as e:
            connection.rollback()
            raise Exception(f"Error registering customer: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update_customer(self, customer_data):
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor()

            update_query = """
                UPDATE Customer 
                SET FirstName = %s, LastName = %s, Email = %s, PhoneNumber = %s, 
                    Address = %s, Password = %s
                WHERE CustomerID = %s
            """
            cursor.execute(update_query, (
                customer_data.first_name,
                customer_data.last_name,
                customer_data.email,
                customer_data.phone_number,
                customer_data.address,
                customer_data.password,
                customer_data.customer_id
            ))

            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise Exception(f"Error updating customer: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def delete_customer(self, customer_id):
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor()

            delete_query = "DELETE FROM Customer WHERE CustomerID = %s"
            cursor.execute(delete_query, (customer_id,))

            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise Exception(f"Error deleting customer: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def authenticate_customer(self, username, password):
        customer = self.get_customer_by_username(username)
        if customer and customer.authenticate(password):
            return customer
        else:
            raise AuthenticationException("Invalid username or password")