"""Tests for RegisterVehicleUseCase following TDD approach."""

import pytest


class TestRegisterVehicleUseCase:
    """Test cases for RegisterVehicleUseCase."""

    def test_register_new_vehicle_successfully(self, vehicle_repository) -> None:
        """
        Given: No vehicle with ID 'V-456' exists
        When: Registering a new vehicle with valid data
        Then: Vehicle should be saved to repository
        And: Vehicle should be retrievable by ID
        """
        # Arrange
        from src.application.use_cases.register_vehicle_use_case import (
            RegisterVehicleUseCase,
        )

        use_case = RegisterVehicleUseCase(vehicle_repository=vehicle_repository)

        # Act
        use_case.execute(
            vehicle_id="V-456",
            plate="XYZ-789",
            model="Honda Civic",
            initial_mileage=0,
        )

        # Assert
        saved_vehicle = vehicle_repository.get_by_id("V-456")
        assert saved_vehicle.id == "V-456"
        assert saved_vehicle.plate == "XYZ-789"
        assert saved_vehicle.model == "Honda Civic"
        assert saved_vehicle.current_mileage == 0

    def test_register_vehicle_with_duplicate_id_raises_exception(
        self, vehicle_repository
    ) -> None:
        """
        Given: A vehicle with ID 'V-123' already exists
        When: Attempting to register another vehicle with same ID
        Then: Should raise DuplicateVehicleException with appropriate message
        """
        # Arrange
        from src.application.use_cases.register_vehicle_use_case import (
            RegisterVehicleUseCase,
        )
        from src.domain.entities.vehicle import Vehicle
        from src.domain.exceptions.duplicate_vehicle_exception import (
            DuplicateVehicleException,
        )

        # Create existing vehicle
        existing_vehicle = Vehicle(
            id="V-123", plate="ABC-123", model="Toyota Corolla", current_mileage=5000
        )
        vehicle_repository.save(existing_vehicle)

        use_case = RegisterVehicleUseCase(vehicle_repository=vehicle_repository)

        # Act & Assert
        with pytest.raises(
            DuplicateVehicleException, match="Ya existe un vehículo con ID V-123"
        ):
            use_case.execute(
                vehicle_id="V-123",
                plate="XYZ-999",
                model="Different Model",
                initial_mileage=0,
            )
