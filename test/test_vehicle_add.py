import pytest
from entity.vehicle import Vehicle


def test_add_new_vehicle(vehicle_service, unique_vehicle):
    """Test adding a new vehicle"""
    vehicle_id = vehicle_service.add_vehicle(unique_vehicle)
    assert vehicle_id is not None

    # Clean up
    vehicle_service.remove_vehicle(vehicle_id)