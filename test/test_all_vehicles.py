import pytest


def test_get_list_all_vehicles(vehicle_service, unique_vehicle):
    """Test getting a list of all vehicles"""
    # Add test vehicle first
    vehicle_id = vehicle_service.add_vehicle(unique_vehicle)

    all_vehicles = vehicle_service.get_all_vehicles()
    assert len(all_vehicles) >= 1
    assert any(v.vehicle_id == vehicle_id for v in all_vehicles)

    # Clean up
    vehicle_service.remove_vehicle(vehicle_id)