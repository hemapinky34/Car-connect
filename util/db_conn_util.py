import mysql.connector
from exception.db_connection_exception import DatabaseConnectionException


class DBConnUtil:
    @staticmethod
    def get_connection(connection_string):
        try:
            # Parse the connection string
            params = {}
            for item in connection_string.split():
                key, value = item.split('=', 1)
                params[key] = value

            # Establish connection
            connection = mysql.connector.connect(
                host=params['host'],
                database=params['database'],
                user=params['user'],
                password=params['password']
            )

            if connection.is_connected():
                print("Successfully connected to the database")
                return connection
            else:
                raise DatabaseConnectionException("Failed to connect to the database")
        except Exception as e:
            raise DatabaseConnectionException(f"Database connection error: {str(e)}")