import pytest
import random
import string
from datetime import date
from dao.customer_service import CustomerService
from dao.vehicle_service import VehicleService
from entity.customer import Customer
from entity.vehicle import Vehicle

def random_string(length=8):
    """Generate a random string of fixed length"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

@pytest.fixture(scope="function")
def customer_service():
    return CustomerService()

@pytest.fixture(scope="function")
def vehicle_service():
    return VehicleService()

@pytest.fixture(scope="function")
def unique_customer():
    """Generate a customer with unique details"""
    random_str = random_string()
    return Customer(
        first_name=f"Test_{random_str}",
        last_name=f"User_{random_str}",
        email=f"test_{random_str}@example.com",
        phone_number=f"123{random.randint(1000000, 9999999)}",
        address=f"123 {random_str} St",
        username=f"user_{random_str}",
        password="testpass"
    )

@pytest.fixture(scope="function")
def unique_vehicle():
    """Generate a vehicle with unique details"""
    random_str = random_string()
    return Vehicle(
        model=f"Model_{random_str}",
        make=f"Make_{random_str}",
        year=random.randint(2000, 2023),
        color=random.choice(["Red", "Blue", "Green", "Black"]),
        registration_number=f"REG{random.randint(1000, 9999)}",
        availability=True,
        daily_rate=round(random.uniform(20.0, 100.0), 2)
    )