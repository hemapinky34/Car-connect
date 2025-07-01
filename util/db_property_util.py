import configparser
import os


class DBPropertyUtil:
    @staticmethod
    def get_connection_string(property_file_name):
        try:
            config = configparser.ConfigParser()

            # Get the absolute path to the property file
            property_file_path = os.path.join(os.path.dirname(__file__), '..', 'resources', property_file_name)

            config.read(property_file_path)

            if 'Database' not in config:
                raise Exception("Database section not found in the property file")

            db_config = config['Database']

            required_keys = ['host', 'database', 'user', 'password']
            for key in required_keys:
                if key not in db_config:
                    raise Exception(f"Missing required database configuration: {key}")

            connection_string = (
                f"host={db_config['host']} "
                f"database={db_config['database']} "
                f"user={db_config['user']} "
                f"password={db_config['password']}"
            )

            return connection_string
        except Exception as e:
            raise Exception(f"Error reading database properties: {str(e)}")