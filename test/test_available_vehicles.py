import pytest


def test_get_list_available_vehicles(vehicle_service, unique_vehicle):
    """Test getting a list of available vehicles"""
    # Add test vehicle first
    vehicle_id = vehicle_service.add_vehicle(unique_vehicle)

    # Ensure it's available
    vehicle_service.update_vehicle_availability(vehicle_id, True)

    vehicles = vehicle_service.get_available_vehicles()
    assert len(vehicles) >= 1
    assert any(v.vehicle_id == vehicle_id for v in vehicles)

    # Clean up
    vehicle_service.remove_vehicle(vehicle_id)