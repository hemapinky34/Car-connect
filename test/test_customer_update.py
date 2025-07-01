import pytest
from datetime import date
from entity.customer import Customer  # Add this import


def test_update_customer_information(customer_service, unique_customer):
    """Test updating customer information"""
    # Register test customer first
    customer_id = customer_service.register_customer(unique_customer)

    updated_customer = Customer(
        customer_id=customer_id,
        first_name="Updated",
        last_name="Name",
        email=f"updated_{unique_customer.email}",
        phone_number="9876543210",
        address="456 Updated St",
        username=unique_customer.username,
        password="newpass",
        registration_date=date.today()
    )

    success = customer_service.update_customer(updated_customer)
    assert success

    # Verify update
    customer = customer_service.get_customer_by_id(customer_id)
    assert customer.first_name == "Updated"
    assert customer.last_name == "Name"

    # Clean up
    customer_service.delete_customer(customer_id)