import mysql.connector
from datetime import datetime
from entity.reservation import Reservation
from exception.reservation_exception import ReservationException
from exception.vehicle_not_found_exception import VehicleNotFoundException
from util.db_conn_util import DBConnUtil
from util.db_property_util import DBPropertyUtil
from dao.vehicle_service import VehicleService


class ReservationService:
    def __init__(self):
        self.__connection_string = DBPropertyUtil.get_connection_string('db_config.properties')

    def get_reservation_by_id(self, reservation_id):
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT r.*, v.DailyRate 
                FROM Reservation r
                JOIN Vehicle v ON r.VehicleID = v.VehicleID
                WHERE r.ReservationID = %s
            """
            cursor.execute(query, (reservation_id,))
            reservation_data = cursor.fetchone()

            if reservation_data:
                reservation = Reservation(
                    reservation_id=reservation_data['ReservationID'],
                    customer_id=reservation_data['CustomerID'],
                    vehicle_id=reservation_data['VehicleID'],
                    start_date=reservation_data['StartDate'],
                    end_date=reservation_data['EndDate'],
                    total_cost=float(reservation_data['TotalCost']),
                    status=reservation_data['Status']
                )
                return reservation
            else:
                return None
        except Exception as e:
            raise Exception(f"Error getting reservation by ID: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_reservations_by_customer_id(self, customer_id):
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT r.*, v.Model, v.Make, v.DailyRate 
                FROM Reservation r
                JOIN Vehicle v ON r.VehicleID = v.VehicleID
                WHERE r.CustomerID = %s
                ORDER BY r.StartDate DESC
            """
            cursor.execute(query, (customer_id,))

            reservations = []
            for reservation_data in cursor.fetchall():
                reservation = Reservation(
                    reservation_id=reservation_data['ReservationID'],
                    customer_id=reservation_data['CustomerID'],
                    vehicle_id=reservation_data['VehicleID'],
                    start_date=reservation_data['StartDate'],
                    end_date=reservation_data['EndDate'],
                    total_cost=float(reservation_data['TotalCost']),
                    status=reservation_data['Status']
                )
                reservation.vehicle_info = f"{reservation_data['Make']} {reservation_data['Model']}"
                reservation.daily_rate = float(reservation_data['DailyRate'])
                reservations.append(reservation)

            return reservations
        except Exception as e:
            raise Exception(f"Error getting reservations by customer ID: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def create_reservation(self, reservation_data):
        connection = None
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            connection.autocommit = False  # Start transaction

            cursor = connection.cursor()
            vehicle_service = VehicleService()

            # 1. Check vehicle availability
            vehicle = vehicle_service.get_vehicle_by_id(reservation_data.vehicle_id)
            if not vehicle.availability:
                raise ReservationException("Vehicle is not available for reservation")

            # 2. Check for overlapping reservations
            overlap_query = """
                SELECT COUNT(*) FROM Reservation 
                WHERE VehicleID = %s AND Status NOT IN ('Cancelled', 'Completed')
                AND (
                    (StartDate BETWEEN %s AND %s)
                    OR (EndDate BETWEEN %s AND %s)
                    OR (%s BETWEEN StartDate AND EndDate)
                    OR (%s BETWEEN StartDate AND EndDate)
                )
                FOR UPDATE  # Add row lock
            """
            cursor.execute(overlap_query, (
                reservation_data.vehicle_id,
                reservation_data.start_date,
                reservation_data.end_date,
                reservation_data.start_date,
                reservation_data.end_date,
                reservation_data.start_date,
                reservation_data.end_date
            ))
            overlap_count = cursor.fetchone()[0]

            if overlap_count > 0:
                raise ReservationException("Vehicle is already reserved for the selected dates")

            # 3. Calculate total cost
            days = (reservation_data.end_date - reservation_data.start_date).days
            total_cost = days * vehicle.daily_rate

            # 4. Create reservation
            insert_query = """
                INSERT INTO Reservation (CustomerID, VehicleID, StartDate, EndDate, TotalCost, Status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                reservation_data.customer_id,
                reservation_data.vehicle_id,
                reservation_data.start_date,
                reservation_data.end_date,
                total_cost,
                'Confirmed'
            ))

            # 5. Update vehicle availability
            update_query = "UPDATE Vehicle SET Availability = FALSE WHERE VehicleID = %s"
            cursor.execute(update_query, (reservation_data.vehicle_id,))

            connection.commit()  # Commit transaction
            return cursor.lastrowid

        except Exception as e:
            if connection:
                connection.rollback()
            raise Exception(f"Error creating reservation: {str(e)}")
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def update_reservation(self, reservation_data):
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor()

            # Get existing reservation
            existing_reservation = self.get_reservation_by_id(reservation_data.reservation_id)
            if not existing_reservation:
                raise ReservationException("Reservation not found")

            # Only allow updates to pending reservations
            if existing_reservation.status not in ['Pending', 'Confirmed']:
                raise ReservationException("Only pending or confirmed reservations can be updated")

            update_query = """
                UPDATE Reservation 
                SET StartDate = %s, EndDate = %s, Status = %s
                WHERE ReservationID = %s
            """
            cursor.execute(update_query, (
                reservation_data.start_date,
                reservation_data.end_date,
                reservation_data.status,
                reservation_data.reservation_id
            ))

            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise Exception(f"Error updating reservation: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def cancel_reservation(self, reservation_id):
        try:
            connection = DBConnUtil.get_connection(self.__connection_string)
            cursor = connection.cursor()

            # Get reservation details
            reservation = self.get_reservation_by_id(reservation_id)
            if not reservation:
                raise ReservationException("Reservation not found")

            # Only allow cancellation of pending or confirmed reservations
            if reservation.status not in ['Pending', 'Confirmed']:
                raise ReservationException("Only pending or confirmed reservations can be cancelled")

            # Update reservation status
            update_query = "UPDATE Reservation SET Status = 'Cancelled' WHERE ReservationID = %s"
            cursor.execute(update_query, (reservation_id,))

            # Make vehicle available again
            vehicle_service = VehicleService()
            vehicle_service.update_vehicle_availability(reservation.vehicle_id, True)

            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise Exception(f"Error cancelling reservation: {str(e)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()