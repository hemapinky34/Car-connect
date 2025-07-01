import pytest
from entity.vehicle import Vehicle


def test_update_vehicle_details(vehicle_service, unique_vehicle):
    """Test updating vehicle details"""
    # Add test vehicle first
    vehicle_id = vehicle_service.add_vehicle(unique_vehicle)

    updated_vehicle = Vehicle(
        vehicle_id=vehicle_id,
        model="UpdatedModel",
        make="UpdatedMake",
        year=unique_vehicle.year,
        color="Blue",
        registration_number=f"UPD{unique_vehicle.registration_number[3:]}",
        availability=True,  # Changed to True to allow removal
        daily_rate=69.99
    )

    success = vehicle_service.update_vehicle(updated_vehicle)
    assert success

    # Verify update
    vehicle = vehicle_service.get_vehicle_by_id(vehicle_id)
    assert vehicle.model == "UpdatedModel"
    assert vehicle.daily_rate == 69.99

    # Make sure vehicle is available before removal
    vehicle_service.update_vehicle_availability(vehicle_id, True)

    # Clean up
    vehicle_service.remove_vehicle(vehicle_id)