import sys
from datetime import datetime
from dao.customer_service import CustomerService
from dao.vehicle_service import VehicleService
from dao.reservation_service import ReservationService
from dao.admin_service import AdminService
from entity.customer import Customer
from entity.vehicle import Vehicle
from entity.admin import Admin
from entity.reservation import Reservation
from util.db_conn_util import DBConnUtil
from exception.authentication_exception import AuthenticationException
from exception.reservation_exception import ReservationException
from exception.vehicle_not_found_exception import VehicleNotFoundException
from exception.admin_not_found_exception import AdminNotFoundException
from exception.customer_not_found_exception import CustomerNotFoundException


class MainModule:
    def __init__(self):
        self.customer_service = CustomerService()
        self.vehicle_service = VehicleService()
        self.reservation_service = ReservationService()
        self.admin_service = AdminService()
        self.current_customer = None
        self.current_admin = None

    def display_main_menu(self):
        while True:
            print("\n===== CarConnect Main Menu =====")
            print("1. Login as Admin")
            print("2. Login as Customer")
            print("3. Register New Customer")
            print("4. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.admin_login()
            elif choice == "2":
                self.customer_login()
            elif choice == "3":
                self.register_customer()
            elif choice == "4":
                print("Thank you for using CarConnect. Goodbye!")
                sys.exit()
            else:
                print("Invalid choice. Please try again.")

    def admin_login(self):
        print("\n===== Admin Login =====")
        username = input("Enter username: ")
        password = input("Enter password: ")

        try:
            admin = self.admin_service.authenticate_admin(username, password)
            self.current_admin = admin
            print(f"\nWelcome, {admin.first_name} {admin.last_name} ({admin.role})")
            self.display_admin_menu()
        except AuthenticationException as e:
            print(f"Login failed: {str(e)}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def display_admin_menu(self):
        while True:
            print("\n===== Admin Menu =====")
            print("1. Manage Customers")
            print("2. Manage Vehicles")
            print("3. Manage Reservations")
            print("4. Manage Admins")
            print("5. Back to Main Menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.manage_customers()
            elif choice == "2":
                self.manage_vehicles()
            elif choice == "3":
                self.manage_reservations()
            elif choice == "4":
                self.manage_admins()
            elif choice == "5":
                self.current_admin = None
                return
            else:
                print("Invalid choice. Please try again.")

    def manage_customers(self):
        while True:
            print("\n===== Customer Management =====")
            print("1. Get Customer by ID")
            print("2. Get Customer by Username")
            print("3. Register New Customer")
            print("4. Update Customer")
            print("5. Delete Customer")
            print("6. View All Customers")
            print("7. Back to Admin Menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.get_customer_by_id()
            elif choice == "2":
                self.get_customer_by_username()
            elif choice == "3":
                self.register_customer()
            elif choice == "4":
                self.update_customer()
            elif choice == "5":
                self.delete_customer()
            elif choice == "6":
                self.view_all_customers()
            elif choice == "7":
                return
            else:
                print("Invalid choice. Please try again.")

    def get_customer_by_id(self):
        try:
            customer_id = input("Enter Customer ID: ")
            customer = self.customer_service.get_customer_by_id(int(customer_id))
            print("\nCustomer Details:")
            print(f"ID: {customer.customer_id}")
            print(f"Name: {customer.first_name} {customer.last_name}")
            print(f"Email: {customer.email}")
            print(f"Phone: {customer.phone_number}")
            print(f"Username: {customer.username}")
            print(f"Registered: {customer.registration_date}")
        except CustomerNotFoundException as e:
            print(f"Error: {str(e)}")
        except ValueError:
            print("Error: Invalid customer ID format")
        except Exception as e:
            print(f"Error: {str(e)}")

    def get_customer_by_username(self):
        try:
            username = input("Enter Username: ")
            customer = self.customer_service.get_customer_by_username(username)
            print("\nCustomer Details:")
            print(f"ID: {customer.customer_id}")
            print(f"Name: {customer.first_name} {customer.last_name}")
            print(f"Email: {customer.email}")
            print(f"Phone: {customer.phone_number}")
            print(f"Username: {customer.username}")
            print(f"Registered: {customer.registration_date}")
        except CustomerNotFoundException as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def view_all_customers(self):
        try:
            connection = DBConnUtil.get_connection(self.customer_service._CustomerService__connection_string)
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM Customer ORDER BY RegistrationDate ASC"
            cursor.execute(query)
            customers = cursor.fetchall()

            print("\n===== All Customers =====")
            if not customers:
                print("No customers found.")
                return

            print("\n{:<5} {:<20} {:<15} {:<30} {:<15} {:<10}".format(
                "ID", "Name", "Phone", "Email", "Username", "Registered"
            ))
            print("-" * 95)

            for customer in customers:
                print("{:<5} {:<20} {:<15} {:<30} {:<15} {:<10}".format(
                    customer['CustomerID'],
                    f"{customer['FirstName']} {customer['LastName']}",
                    customer['PhoneNumber'],
                    customer['Email'],
                    customer['Username'],
                    str(customer['RegistrationDate'])
                ))
        except Exception as e:
            print(f"\nError viewing customers: {str(e)}")
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def register_customer(self):
        try:
            print("\n===== Customer Registration =====")
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")
            phone_number = input("Enter phone number: ")
            address = input("Enter address: ")
            username = input("Enter username: ")
            password = input("Enter password: ")

            customer = Customer(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                address=address,
                username=username,
                password=password
            )

            customer_id = self.customer_service.register_customer(customer)
            print(f"\nRegistration successful! Customer ID: {customer_id}")
        except Exception as e:
            print(f"Registration failed: {str(e)}")

    def update_customer(self):
        try:
            customer_id = input("Enter Customer ID to update: ")
            existing_customer = self.customer_service.get_customer_by_id(int(customer_id))

            print("\nLeave blank to keep current value")
            first_name = input(f"First name [{existing_customer.first_name}]: ") or existing_customer.first_name
            last_name = input(f"Last name [{existing_customer.last_name}]: ") or existing_customer.last_name
            email = input(f"Email [{existing_customer.email}]: ") or existing_customer.email
            phone_number = input(f"Phone number [{existing_customer.phone_number}]: ") or existing_customer.phone_number
            address = input(f"Address [{existing_customer.address}]: ") or existing_customer.address
            password = input("New password (leave blank to keep current): ") or existing_customer.password

            updated_customer = Customer(
                customer_id=int(customer_id),
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                address=address,
                username=existing_customer.username,
                password=password,
                registration_date=existing_customer.registration_date
            )

            success = self.customer_service.update_customer(updated_customer)
            if success:
                print("Customer updated successfully")
            else:
                print("Failed to update customer")
        except Exception as e:
            print(f"Error updating customer: {str(e)}")

    def delete_customer(self):
        try:
            customer_id = input("Enter Customer ID to delete: ")
            confirm = input(f"Are you sure you want to delete customer {customer_id}? (y/n): ")
            if confirm.lower() == 'y':
                success = self.customer_service.delete_customer(int(customer_id))
                if success:
                    print("Customer deleted successfully")
                else:
                    print("Failed to delete customer")
        except Exception as e:
            print(f"Error deleting customer: {str(e)}")

    def manage_vehicles(self):
        while True:
            print("\n===== Vehicle Management =====")
            print("1. Get Vehicle by ID")
            print("2. Get Available Vehicles")
            print("3. Add New Vehicle")
            print("4. Update Vehicle")
            print("5. Remove Vehicle")
            print("6. View All Vehicles")
            print("7. Back to Admin Menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.get_vehicle_by_id()
            elif choice == "2":
                self.get_available_vehicles()
            elif choice == "3":
                self.add_new_vehicle()
            elif choice == "4":
                self.update_vehicle()
            elif choice == "5":
                self.remove_vehicle()
            elif choice == "6":
                self.view_all_vehicles()
            elif choice == "7":
                return
            else:
                print("Invalid choice. Please try again.")

    def get_vehicle_by_id(self):
        try:
            vehicle_id = input("Enter Vehicle ID: ")
            vehicle = self.vehicle_service.get_vehicle_by_id(int(vehicle_id))
            print("\nVehicle Details:")
            print(f"ID: {vehicle.vehicle_id}")
            print(f"Make: {vehicle.make}")
            print(f"Model: {vehicle.model}")
            print(f"Year: {vehicle.year}")
            print(f"Color: {vehicle.color}")
            print(f"Registration: {vehicle.registration_number}")
            print(f"Available: {'Yes' if vehicle.availability else 'No'}")
            print(f"Daily Rate: ${vehicle.daily_rate:.2f}")
        except VehicleNotFoundException as e:
            print(f"Error: {str(e)}")
        except ValueError:
            print("Error: Invalid vehicle ID format")
        except Exception as e:
            print(f"Error: {str(e)}")

    def get_available_vehicles(self):
        try:
            vehicles = self.vehicle_service.get_available_vehicles()
            print("\n===== Available Vehicles =====")
            if not vehicles:
                print("No available vehicles found.")
                return

            print("\n{:<5} {:<15} {:<15} {:<10} {:<10} {:<15} {:<10}".format(
                "ID", "Make", "Model", "Year", "Color", "Reg Number", "Daily Rate"
            ))
            print("-" * 80)

            for vehicle in vehicles:
                print("{:<5} {:<15} {:<15} {:<10} {:<10} {:<15} ${:<10.2f}".format(
                    vehicle.vehicle_id,
                    vehicle.make,
                    vehicle.model,
                    vehicle.year,
                    vehicle.color,
                    vehicle.registration_number,
                    vehicle.daily_rate
                ))
        except Exception as e:
            print(f"Error viewing available vehicles: {str(e)}")

    def view_all_vehicles(self):
        try:
            vehicles = self.vehicle_service.get_all_vehicles()
            print("\n===== All Vehicles =====")
            if not vehicles:
                print("No vehicles found.")
                return

            print("\n{:<5} {:<15} {:<15} {:<10} {:<10} {:<15} {:<10} {:<10}".format(
                "ID", "Make", "Model", "Year", "Color", "Reg Number", "Available", "Daily Rate"
            ))
            print("-" * 100)

            for vehicle in vehicles:
                print("{:<5} {:<15} {:<15} {:<10} {:<10} {:<15} {:<10} ${:<10.2f}".format(
                    vehicle.vehicle_id,
                    vehicle.make,
                    vehicle.model,
                    vehicle.year,
                    vehicle.color,
                    vehicle.registration_number,
                    "Yes" if vehicle.availability else "No",
                    vehicle.daily_rate
                ))
        except Exception as e:
            print(f"Error viewing vehicles: {str(e)}")

    def add_new_vehicle(self):
        try:
            print("\n===== Add New Vehicle =====")
            model = input("Enter model: ")
            make = input("Enter make: ")
            year = input("Enter year: ")
            color = input("Enter color: ")
            registration_number = input("Enter registration number: ")
            daily_rate = input("Enter daily rate: ")

            vehicle = Vehicle(
                model=model,
                make=make,
                year=int(year),
                color=color,
                registration_number=registration_number,
                availability=True,
                daily_rate=float(daily_rate)
            )

            vehicle_id = self.vehicle_service.add_vehicle(vehicle)
            print(f"\nVehicle added successfully with ID: {vehicle_id}")
        except ValueError:
            print("Invalid input. Please enter valid numbers for year and daily rate.")
        except Exception as e:
            print(f"Error adding vehicle: {str(e)}")

    def update_vehicle(self):
        try:
            vehicle_id = input("Enter Vehicle ID to update: ")
            existing_vehicle = self.vehicle_service.get_vehicle_by_id(int(vehicle_id))

            print("\nLeave blank to keep current value")
            model = input(f"Model [{existing_vehicle.model}]: ") or existing_vehicle.model
            make = input(f"Make [{existing_vehicle.make}]: ") or existing_vehicle.make
            year = input(f"Year [{existing_vehicle.year}]: ") or existing_vehicle.year
            color = input(f"Color [{existing_vehicle.color}]: ") or existing_vehicle.color
            reg_num = input(
                f"Registration Number [{existing_vehicle.registration_number}]: ") or existing_vehicle.registration_number
            daily_rate = input(f"Daily Rate [{existing_vehicle.daily_rate}]: ") or existing_vehicle.daily_rate
            availability = input(f"Availability (True/False) [{existing_vehicle.availability}]: ")

            if availability == "":
                availability = existing_vehicle.availability
            else:
                availability = availability.lower() == 'true'

            updated_vehicle = Vehicle(
                vehicle_id=int(vehicle_id),
                model=model,
                make=make,
                year=int(year),
                color=color,
                registration_number=reg_num,
                availability=availability,
                daily_rate=float(daily_rate)
            )

            success = self.vehicle_service.update_vehicle(updated_vehicle)
            if success:
                print("\nVehicle updated successfully")
            else:
                print("\nFailed to update vehicle")
        except ValueError:
            print("Invalid input. Please enter valid numbers for year and daily rate.")
        except Exception as e:
            print(f"Error updating vehicle: {str(e)}")

    def remove_vehicle(self):
        try:
            vehicle_id = input("Enter Vehicle ID to remove: ")
            confirm = input(f"Are you sure you want to remove vehicle {vehicle_id}? (y/n): ")
            if confirm.lower() == 'y':
                force = input("Force remove (ignore availability)? (y/n): ").lower() == 'y'
                success = self.vehicle_service.remove_vehicle(int(vehicle_id), force=force)
                if success:
                    print("Vehicle removed successfully")
                else:
                    print("Failed to remove vehicle")
        except Exception as e:
            print(f"Error removing vehicle: {str(e)}")

    def manage_reservations(self):
        while True:
            print("\n===== Reservation Management =====")
            print("1. Get Reservation by ID")
            print("2. Get Reservations by Customer ID")
            print("3. Create Reservation")
            print("4. Update Reservation")
            print("5. Cancel Reservation")
            print("6. View All Reservations")
            print("7. Back to Admin Menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.get_reservation_by_id()
            elif choice == "2":
                self.get_reservations_by_customer_id()
            elif choice == "3":
                self.create_reservation()
            elif choice == "4":
                self.update_reservation()
            elif choice == "5":
                self.cancel_reservation()
            elif choice == "6":
                self.view_all_reservations()
            elif choice == "7":
                return
            else:
                print("Invalid choice. Please try again.")

    def get_reservation_by_id(self):
        try:
            reservation_id = input("Enter Reservation ID: ")
            reservation = self.reservation_service.get_reservation_by_id(int(reservation_id))
            print("\nReservation Details:")
            print(f"ID: {reservation.reservation_id}")
            print(f"Customer ID: {reservation.customer_id}")
            print(f"Vehicle ID: {reservation.vehicle_id}")
            print(f"Start Date: {reservation.start_date}")
            print(f"End Date: {reservation.end_date}")
            print(f"Total Cost: ${reservation.total_cost:.2f}")
            print(f"Status: {reservation.status}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def get_reservations_by_customer_id(self):
        try:
            customer_id = input("Enter Customer ID: ")
            reservations = self.reservation_service.get_reservations_by_customer_id(int(customer_id))
            print("\n===== Customer Reservations =====")
            if not reservations:
                print("No reservations found for this customer.")
                return

            print("\n{:<5} {:<10} {:<10} {:<20} {:<15} {:<10}".format(
                "ID", "Vehicle ID", "Status", "Dates", "Total Cost", "Days"
            ))
            print("-" * 80)

            for res in reservations:
                start_date = res.start_date.strftime('%Y-%m-%d')
                end_date = res.end_date.strftime('%Y-%m-%d')
                days = (res.end_date - res.start_date).days

                print("{:<5} {:<10} {:<10} {:<20} ${:<15.2f} {:<10}".format(
                    res.reservation_id,
                    res.vehicle_id,
                    res.status,
                    f"{start_date} to {end_date}",
                    float(res.total_cost),
                    days
                ))
        except Exception as e:
            print(f"Error: {str(e)}")

    def view_all_reservations(self):
        try:
            connection = DBConnUtil.get_connection(self.reservation_service._ReservationService__connection_string)
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT r.*, c.FirstName, c.LastName, v.Model, v.Make 
                FROM Reservation r
                JOIN Customer c ON r.CustomerID = c.CustomerID
                JOIN Vehicle v ON r.VehicleID = v.VehicleID
                ORDER BY r.StartDate ASC
            """
            cursor.execute(query)
            reservations = cursor.fetchall()

            print("\n===== All Reservations =====")
            if not reservations:
                print("No reservations found.")
                return

            print("\n{:<5} {:<20} {:<15} {:<20} {:<15} {:<15} {:<10}".format(
                "ID", "Customer", "Vehicle", "Dates", "Total Cost", "Status", "Days"
            ))
            print("-" * 100)

            for res in reservations:
                start_date = res['StartDate'].strftime('%Y-%m-%d')
                end_date = res['EndDate'].strftime('%Y-%m-%d')
                days = (res['EndDate'] - res['StartDate']).days

                print("{:<5} {:<20} {:<15} {:<20} {:<15.2f} {:<15} {:<10}".format(
                    res['ReservationID'],
                    f"{res['FirstName']} {res['LastName']}",
                    f"{res['Make']} {res['Model']}",
                    f"{start_date} to {end_date}",
                    float(res['TotalCost']),
                    res['Status'],
                    days
                ))
        except Exception as e:
            print(f"\nError viewing reservations: {str(e)}")
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def create_reservation(self):
        try:
            print("\n===== Create Reservation =====")
            customer_id = input("Enter Customer ID: ")
            vehicle_id = input("Enter Vehicle ID: ")
            start_date = input("Enter Start Date (YYYY-MM-DD): ")
            end_date = input("Enter End Date (YYYY-MM-DD): ")

            reservation = Reservation(
                customer_id=int(customer_id),
                vehicle_id=int(vehicle_id),
                start_date=datetime.strptime(start_date, "%Y-%m-%d"),
                end_date=datetime.strptime(end_date, "%Y-%m-%d")
            )

            reservation_id = self.reservation_service.create_reservation(reservation)
            print(f"\nReservation created successfully! ID: {reservation_id}")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
        except Exception as e:
            print(f"Error creating reservation: {str(e)}")

    def update_reservation(self):
        try:
            print("\n===== Update Reservation =====")
            reservation_id = input("Enter Reservation ID: ")
            existing_res = self.reservation_service.get_reservation_by_id(int(reservation_id))

            print("\nLeave blank to keep current value")
            start_date = input(f"Start Date [{existing_res.start_date}]: ")
            end_date = input(f"End Date [{existing_res.end_date}]: ")
            status = input(f"Status [{existing_res.status}]: ")

            if start_date:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
            else:
                start_date = existing_res.start_date

            if end_date:
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
            else:
                end_date = existing_res.end_date

            if not status:
                status = existing_res.status

            updated_res = Reservation(
                reservation_id=int(reservation_id),
                customer_id=existing_res.customer_id,
                vehicle_id=existing_res.vehicle_id,
                start_date=start_date,
                end_date=end_date,
                total_cost=existing_res.total_cost,
                status=status
            )

            success = self.reservation_service.update_reservation(updated_res)
            if success:
                print("\nReservation updated successfully")
            else:
                print("\nFailed to update reservation")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
        except Exception as e:
            print(f"Error updating reservation: {str(e)}")

    def cancel_reservation(self):
        try:
            reservation_id = input("Enter Reservation ID to cancel: ")
            confirm = input(f"Are you sure you want to cancel reservation {reservation_id}? (y/n): ")
            if confirm.lower() == 'y':
                success = self.reservation_service.cancel_reservation(int(reservation_id))
                if success:
                    print("Reservation cancelled successfully")
                else:
                    print("Failed to cancel reservation")
        except Exception as e:
            print(f"Error cancelling reservation: {str(e)}")

    def manage_admins(self):
        while True:
            print("\n===== Admin Management =====")
            print("1. Get Admin by ID")
            print("2. Get Admin by Username")
            print("3. Register New Admin")
            print("4. Update Admin")
            print("5. Delete Admin")
            print("6. View All Admins")
            print("7. Back to Admin Menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.get_admin_by_id()
            elif choice == "2":
                self.get_admin_by_username()
            elif choice == "3":
                self.register_admin()
            elif choice == "4":
                self.update_admin()
            elif choice == "5":
                self.delete_admin()
            elif choice == "6":
                self.view_all_admins()
            elif choice == "7":
                return
            else:
                print("Invalid choice. Please try again.")

    def get_admin_by_id(self):
        try:
            admin_id = input("Enter Admin ID: ")
            admin = self.admin_service.get_admin_by_id(int(admin_id))
            print("\nAdmin Details:")
            print(f"ID: {admin.admin_id}")
            print(f"Name: {admin.first_name} {admin.last_name}")
            print(f"Email: {admin.email}")
            print(f"Phone: {admin.phone_number}")
            print(f"Username: {admin.username}")
            print(f"Role: {admin.role}")
            print(f"Joined: {admin.join_date}")
        except AdminNotFoundException as e:
            print(f"Error: {str(e)}")
        except ValueError:
            print("Error: Invalid admin ID format")
        except Exception as e:
            print(f"Error: {str(e)}")

    def get_admin_by_username(self):
        try:
            username = input("Enter Username: ")
            admin = self.admin_service.get_admin_by_username(username)
            print("\nAdmin Details:")
            print(f"ID: {admin.admin_id}")
            print(f"Name: {admin.first_name} {admin.last_name}")
            print(f"Email: {admin.email}")
            print(f"Phone: {admin.phone_number}")
            print(f"Username: {admin.username}")
            print(f"Role: {admin.role}")
            print(f"Joined: {admin.join_date}")
        except AdminNotFoundException as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def view_all_admins(self):
        try:
            connection = DBConnUtil.get_connection(self.admin_service._AdminService__connection_string)
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM Admin ORDER BY JoinDate ASC"
            cursor.execute(query)
            admins = cursor.fetchall()

            print("\n===== All Admins =====")
            if not admins:
                print("No admins found.")
                return

            print("\n{:<5} {:<20} {:<15} {:<30} {:<15} {:<15}".format(
                "ID", "Name", "Phone", "Email", "Username", "Role"
            ))
            print("-" * 95)

            for admin in admins:
                print("{:<5} {:<20} {:<15} {:<30} {:<15} {:<15}".format(
                    admin['AdminID'],
                    f"{admin['FirstName']} {admin['LastName']}",
                    admin['PhoneNumber'],
                    admin['Email'],
                    admin['Username'],
                    admin['Role']
                ))
        except Exception as e:
            print(f"\nError viewing admins: {str(e)}")
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def register_admin(self):
        try:
            print("\n===== Admin Registration =====")
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")
            phone_number = input("Enter phone number: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = input("Enter role: ")

            admin = Admin(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                username=username,
                password=password,
                role=role
            )

            admin_id = self.admin_service.register_admin(admin)
            print(f"\nAdmin registered successfully with ID: {admin_id}")
        except Exception as e:
            print(f"Error adding admin: {str(e)}")

    def update_admin(self):
        try:
            admin_id = input("Enter Admin ID to update: ")
            existing_admin = self.admin_service.get_admin_by_id(int(admin_id))

            print("\nLeave blank to keep current value")
            first_name = input(f"First name [{existing_admin.first_name}]: ") or existing_admin.first_name
            last_name = input(f"Last name [{existing_admin.last_name}]: ") or existing_admin.last_name
            email = input(f"Email [{existing_admin.email}]: ") or existing_admin.email
            phone_number = input(f"Phone number [{existing_admin.phone_number}]: ") or existing_admin.phone_number
            password = input("New password (leave blank to keep current): ") or existing_admin.password
            role = input(f"Role [{existing_admin.role}]: ") or existing_admin.role

            updated_admin = Admin(
                admin_id=int(admin_id),
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                username=existing_admin.username,
                password=password,
                role=role,
                join_date=existing_admin.join_date
            )

            success = self.admin_service.update_admin(updated_admin)
            if success:
                print("\nAdmin updated successfully")
            else:
                print("\nFailed to update admin")
        except Exception as e:
            print(f"Error updating admin: {str(e)}")

    def delete_admin(self):
        try:
            admin_id = input("Enter Admin ID to delete: ")
            confirm = input(f"Are you sure you want to delete admin {admin_id}? (y/n): ")
            if confirm.lower() == 'y':
                success = self.admin_service.delete_admin(int(admin_id))
                if success:
                    print("Admin deleted successfully")
                else:
                    print("Failed to delete admin")
        except Exception as e:
            print(f"Error deleting admin: {str(e)}")

    def customer_login(self):
        print("\n===== Customer Login =====")
        username = input("Enter username: ")
        password = input("Enter password: ")

        try:
            customer = self.customer_service.authenticate_customer(username, password)
            self.current_customer = customer
            print(f"\nWelcome, {customer.first_name} {customer.last_name}!")
            self.display_customer_menu()
        except AuthenticationException as e:
            print(f"Login failed: {str(e)}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def display_customer_menu(self):
        while True:
            print("\n===== Customer Menu =====")
            print("1. Update My Data")
            print("2. View My Reservations")
            print("3. Make a Reservation")
            print("4. Back to Main Menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.update_customer_data()
            elif choice == "2":
                self.view_customer_reservations()
            elif choice == "3":
                self.make_reservation()
            elif choice == "4":
                self.current_customer = None
                return
            else:
                print("Invalid choice. Please try again.")

    def update_customer_data(self):
        try:
            print("\n===== Update Your Information =====")
            print("Leave blank to keep current value")

            current_customer = self.current_customer
            first_name = input(f"First name [{current_customer.first_name}]: ") or current_customer.first_name
            last_name = input(f"Last name [{current_customer.last_name}]: ") or current_customer.last_name
            email = input(f"Email [{current_customer.email}]: ") or current_customer.email
            phone_number = input(f"Phone number [{current_customer.phone_number}]: ") or current_customer.phone_number
            address = input(f"Address [{current_customer.address}]: ") or current_customer.address
            password = input("New password (leave blank to keep current): ") or current_customer.password

            updated_customer = Customer(
                customer_id=current_customer.customer_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                address=address,
                username=current_customer.username,
                password=password,
                registration_date=current_customer.registration_date
            )

            success = self.customer_service.update_customer(updated_customer)
            if success:
                print("Your information has been updated successfully")
                self.current_customer = updated_customer
            else:
                print("Failed to update your information")
        except Exception as e:
            print(f"Error updating customer data: {str(e)}")

    def view_customer_reservations(self):
        try:
            reservations = self.reservation_service.get_reservations_by_customer_id(self.current_customer.customer_id)
            print("\n===== Your Reservations =====")
            if not reservations:
                print("You have no reservations yet.")
                return

            for i, reservation in enumerate(reservations, 1):
                print(f"\nReservation {i}:")
                print(f"Vehicle ID: {reservation.vehicle_id}")
                print(f"From: {reservation.start_date} To: {reservation.end_date}")
                print(f"Total Cost: ${reservation.total_cost:.2f}")
                print(f"Status: {reservation.status}")
        except Exception as e:
            print(f"Error viewing reservations: {str(e)}")

    def make_reservation(self):
        try:
            print("\n===== Make a Reservation =====")

            vehicles = self.vehicle_service.get_available_vehicles()
            if not vehicles:
                print("No vehicles available for reservation at this time.")
                return

            print("\nAvailable Vehicles:")
            for i, vehicle in enumerate(vehicles, 1):
                print(f"{i}. {vehicle.model} {vehicle.make} ({vehicle.year}) - ${vehicle.daily_rate:.2f}/day")

            vehicle_choice = int(input("Select vehicle (number): ")) - 1
            if vehicle_choice < 0 or vehicle_choice >= len(vehicles):
                raise Exception("Invalid vehicle selection")

            selected_vehicle = vehicles[vehicle_choice]

            start_date_str = input("Enter start date (YYYY-MM-DD): ")
            end_date_str = input("Enter end date (YYYY-MM-DD): ")

            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

            if start_date >= end_date:
                raise Exception("End date must be after start date")

            if start_date.date() < datetime.now().date():
                raise Exception("Start date cannot be in the past")

            reservation = Reservation(
                customer_id=self.current_customer.customer_id,
                vehicle_id=selected_vehicle.vehicle_id,
                start_date=start_date,
                end_date=end_date
            )

            reservation_id = self.reservation_service.create_reservation(reservation)
            print(f"\nReservation created successfully! Reservation ID: {reservation_id}")

            days = (end_date - start_date).days
            total_cost = days * selected_vehicle.daily_rate
            print(f"Total cost for {days} days: ${total_cost:.2f}")

        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
        except VehicleNotFoundException as e:
            print(f"Vehicle error: {str(e)}")
        except ReservationException as e:
            print(f"Reservation error: {str(e)}")
        except Exception as e:
            print(f"Error making reservation: {str(e)}")


if __name__ == "__main__":
    main_module = MainModule()
    main_module.display_main_menu()