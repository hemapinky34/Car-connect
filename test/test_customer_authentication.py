import pytest
from exception.authentication_exception import AuthenticationException


def test_customer_authentication_invalid_credentials(customer_service, unique_customer):
    """Test customer authentication with invalid credentials"""
    # Register test customer first
    customer_id = customer_service.register_customer(unique_customer)

    with pytest.raises(AuthenticationException):
        customer_service.authenticate_customer(unique_customer.username, "wrongpassword")

    # Clean up
    customer_service.delete_customer(customer_id)


def test_customer_authentication_valid_credentials(customer_service, unique_customer):
    """Test customer authentication with valid credentials"""
    customer_id = customer_service.register_customer(unique_customer)
    customer = customer_service.authenticate_customer(unique_customer.username, "testpass")
    assert customer.customer_id == customer_id

    # Clean up
    customer_service.delete_customer(customer_id)