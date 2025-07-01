import mysql.connector
from entity.vehicle import Vehicle
from exception.vehicle_not_found_exception import VehicleNotFoundException
from util.db_conn_util import DBConnUtil
from util.db_property_util import DBPropertyUtil


class VehicleService:
    def __init__(self):
        self.__connection_string = DBPropertyUtil.get_connection_string('db_config.properties')

    def get_vehicle_by_id(self, vehicle_id):
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM Vehicle WHERE VehicleID = %s"
            cursor.execute(query, (vehicle_id,))
            vehicle_data = cursor.fetchone()

            if vehicle_data:
                vehicle = Vehicle(
                    vehicle_id=vehicle_data['VehicleID'],
                    model=vehicle_data['Model'],
                    make=vehicle_data['Make'],
                    year=vehicle_data['Year'],
                    color=vehicle_data['Color'],
                    registration_number=vehicle_data['RegistrationNumber'],
                    availability=bool(vehicle_data['Availability']),
                    daily_rate=float(vehicle_data['DailyRate'])
                )
                return vehicle
            else:
                raise VehicleNotFoundException(f"Vehicle with ID {vehicle_id} not found")
        except Exception as e:
            raise Exception(f"Error getting vehicle by ID: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_available_vehicles(self):
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM Vehicle WHERE Availability = TRUE"
            cursor.execute(query)
            vehicles = []

            for vehicle_data in cursor.fetchall():
                vehicle = Vehicle(
                    vehicle_id=vehicle_data['VehicleID'],
                    model=vehicle_data['Model'],
                    make=vehicle_data['Make'],
                    year=vehicle_data['Year'],
                    color=vehicle_data['Color'],
                    registration_number=vehicle_data['RegistrationNumber'],
                    availability=bool(vehicle_data['Availability']),
                    daily_rate=float(vehicle_data['DailyRate'])
                )
                vehicles.append(vehicle)

            return vehicles
        except Exception as e:
            raise Exception(f"Error getting available vehicles: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def add_vehicle(self, vehicle_data):
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor()

            # Check if registration number already exists
            check_query = "SELECT COUNT(*) FROM Vehicle WHERE RegistrationNumber = %s"
            cursor.execute(check_query, (vehicle_data.registration_number,))
            count = cursor.fetchone()[0]

            if count > 0:
                raise Exception("Vehicle with this registration number already exists")

            insert_query = """
                INSERT INTO Vehicle (Model, Make, Year, Color, RegistrationNumber, Availability, DailyRate)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                vehicle_data.model,
                vehicle_data.make,
                vehicle_data.year,
                vehicle_data.color,
                vehicle_data.registration_number,
                vehicle_data.availability,
                vehicle_data.daily_rate
            ))

            connection.commit()
            return cursor.lastrowid
        except Exception as e:
            connection.rollback()
            raise Exception(f"Error adding vehicle: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update_vehicle(self, vehicle_data):
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor()

            update_query = """
                UPDATE Vehicle 
                SET Model = %s, Make = %s, Year = %s, Color = %s, 
                    RegistrationNumber = %s, Availability = %s, DailyRate = %s
                WHERE VehicleID = %s
            """
            cursor.execute(update_query, (
                vehicle_data.model,
                vehicle_data.make,
                vehicle_data.year,
                vehicle_data.color,
                vehicle_data.registration_number,
                vehicle_data.availability,
                vehicle_data.daily_rate,
                vehicle_data.vehicle_id
            ))

            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise Exception(f"Error updating vehicle: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def remove_vehicle(self, vehicle_id):
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor()

            # Check if vehicle is available
            check_query = "SELECT Availability FROM Vehicle WHERE VehicleID = %s"
            cursor.execute(check_query, (vehicle_id,))
            result = cursor.fetchone()

            if not result:
                raise Exception("Vehicle not found")

            if not result[0]:  # If not available
                raise Exception("Cannot remove vehicle that is currently rented")

            delete_query = "DELETE FROM Vehicle WHERE VehicleID = %s"
            cursor.execute(delete_query, (vehicle_id,))

            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise Exception(f"Error removing vehicle: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update_vehicle_availability(self, vehicle_id, availability):
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor()

            update_query = "UPDATE Vehicle SET Availability = %s WHERE VehicleID = %s"
            cursor.execute(update_query, (availability, vehicle_id))

            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise Exception(f"Error updating vehicle availability: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_vehicle_by_id(self, vehicle_id):
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM Vehicle WHERE VehicleID = %s"
            cursor.execute(query, (vehicle_id,))
            vehicle_data = cursor.fetchone()

            if vehicle_data:
                vehicle = Vehicle(
                    vehicle_id=vehicle_data['VehicleID'],
                    model=vehicle_data['Model'],
                    make=vehicle_data['Make'],
                    year=vehicle_data['Year'],
                    color=vehicle_data['Color'],
                    registration_number=vehicle_data['RegistrationNumber'],
                    availability=bool(vehicle_data['Availability']),
                    daily_rate=float(vehicle_data['DailyRate'])
                )
                return vehicle
            else:
                raise VehicleNotFoundException(f"Vehicle with ID {vehicle_id} not found")
        except Exception as e:
            raise Exception(f"Error getting vehicle by ID: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def add_vehicle(self, vehicle_data):
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor()

            # Check if registration number already exists
            check_query = "SELECT COUNT(*) FROM Vehicle WHERE RegistrationNumber = %s"
            cursor.execute(check_query, (vehicle_data.registration_number,))
            count = cursor.fetchone()[0]

            if count > 0:
                raise Exception("Vehicle with this registration number already exists")

            insert_query = """
                INSERT INTO Vehicle (Model, Make, Year, Color, RegistrationNumber, Availability, DailyRate)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                vehicle_data.model,
                vehicle_data.make,
                vehicle_data.year,
                vehicle_data.color,
                vehicle_data.registration_number,
                vehicle_data.availability,
                vehicle_data.daily_rate
            ))

            connection.commit()
            return cursor.lastrowid
        except Exception as e:
            connection.rollback()
            raise Exception(f"Error adding vehicle: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update_vehicle(self, vehicle_data):
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor()

            update_query = """
                UPDATE Vehicle 
                SET Model = %s, Make = %s, Year = %s, Color = %s, 
                    RegistrationNumber = %s, Availability = %s, DailyRate = %s
                WHERE VehicleID = %s
            """
            cursor.execute(update_query, (
                vehicle_data.model,
                vehicle_data.make,
                vehicle_data.year,
                vehicle_data.color,
                vehicle_data.registration_number,
                vehicle_data.availability,
                vehicle_data.daily_rate,
                vehicle_data.vehicle_id
            ))

            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise Exception(f"Error updating vehicle: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_all_vehicles(self):
        """Get all vehicles regardless of availability"""
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM Vehicle ORDER BY Make, Model"
            cursor.execute(query)

            vehicles = []
            for vehicle_data in cursor.fetchall():
                vehicle = Vehicle(
                    vehicle_id=vehicle_data['VehicleID'],
                    model=vehicle_data['Model'],
                    make=vehicle_data['Make'],
                    year=vehicle_data['Year'],
                    color=vehicle_data['Color'],
                    registration_number=vehicle_data['RegistrationNumber'],
                    availability=bool(vehicle_data['Availability']),
                    daily_rate=float(vehicle_data['DailyRate'])
                )
                vehicles.append(vehicle)

            return vehicles
        except Exception as e:
            raise Exception(f"Error getting all vehicles: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()