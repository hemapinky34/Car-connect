import mysql.connector
from entity.admin import Admin
from exception.authentication_exception import AuthenticationException
from exception.admin_not_found_exception import AdminNotFoundException
from util.db_conn_util import DBConnUtil
from util.db_property_util import DBPropertyUtil


class AdminService:
    def __init__(self):
        self.__connection_string = DBPropertyUtil.get_connection_string('db_config.properties')

    def get_admin_by_id(self, admin_id):
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM Admin WHERE AdminID = %s"
            cursor.execute(query, (admin_id,))
            admin_data = cursor.fetchone()

            if admin_data:
                admin = Admin(
                    admin_id=admin_data['AdminID'],
                    first_name=admin_data['FirstName'],
                    last_name=admin_data['LastName'],
                    email=admin_data['Email'],
                    phone_number=admin_data['PhoneNumber'],
                    username=admin_data['Username'],
                    password=admin_data['Password'],
                    role=admin_data['Role'],
                    join_date=admin_data['JoinDate']
                )
                return admin
            else:
                raise AdminNotFoundException(f"Admin with ID {admin_id} not found")
        except Exception as e:
            raise Exception(f"Error getting admin by ID: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_admin_by_username(self, username):
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM Admin WHERE Username = %s"
            cursor.execute(query, (username,))
            admin_data = cursor.fetchone()

            if admin_data:
                admin = Admin(
                    admin_id=admin_data['AdminID'],
                    first_name=admin_data['FirstName'],
                    last_name=admin_data['LastName'],
                    email=admin_data['Email'],
                    phone_number=admin_data['PhoneNumber'],
                    username=admin_data['Username'],
                    password=admin_data['Password'],
                    role=admin_data['Role'],
                    join_date=admin_data['JoinDate']
                )
                return admin
            else:
                return None
        except Exception as e:
            raise Exception(f"Error getting admin by username: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def register_admin(self, admin_data):
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor()

            # Check if username or email already exists
            check_query = "SELECT COUNT(*) FROM Admin WHERE Username = %s OR Email = %s"
            cursor.execute(check_query, (admin_data.username, admin_data.email))
            count = cursor.fetchone()[0]

            if count > 0:
                raise Exception("Username or email already exists")

            insert_query = """
                INSERT INTO Admin (FirstName, LastName, Email, PhoneNumber, Username, Password, Role, JoinDate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                admin_data.first_name,
                admin_data.last_name,
                admin_data.email,
                admin_data.phone_number,
                admin_data.username,
                admin_data.password,
                admin_data.role,
                admin_data.join_date
            ))

            connection.commit()
            return cursor.lastrowid
        except Exception as e:
            connection.rollback()
            raise Exception(f"Error registering admin: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update_admin(self, admin_data):
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor()

            update_query = """
                UPDATE Admin 
                SET FirstName = %s, LastName = %s, Email = %s, PhoneNumber = %s, 
                    Password = %s, Role = %s
                WHERE AdminID = %s
            """
            cursor.execute(update_query, (
                admin_data.first_name,
                admin_data.last_name,
                admin_data.email,
                admin_data.phone_number,
                admin_data.password,
                admin_data.role,
                admin_data.admin_id
            ))

            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise Exception(f"Error updating admin: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def delete_admin(self, admin_id):
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor()

            # Prevent deletion of the last admin
            count_query = "SELECT COUNT(*) FROM Admin"
            cursor.execute(count_query)
            count = cursor.fetchone()[0]

            if count <= 1:
                raise Exception("Cannot delete the last admin")

            delete_query = "DELETE FROM Admin WHERE AdminID = %s"
            cursor.execute(delete_query, (admin_id,))

            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise Exception(f"Error deleting admin: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def authenticate_admin(self, username, password):
        admin = self.get_admin_by_username(username)
        if admin and admin.authenticate(password):
            return admin
        else:
            raise AuthenticationException("Invalid username or password")