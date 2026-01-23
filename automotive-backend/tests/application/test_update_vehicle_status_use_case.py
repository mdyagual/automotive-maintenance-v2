"""Tests for UpdateVehicleStatusUseCase following TDD approach."""

import pytest

from src.application.dtos.vehicle_dtos import UpdateStatusCommand, VehicleDTO
from src.application.use_cases.update_vehicle_status_use_case import (
    UpdateVehicleStatusUseCase,
)
from src.domain.entities.vehicle import Vehicle
from src.domain.entities.vehicle_status import VehicleStatus
from src.domain.exceptions.invalid_status_exception import InvalidStatusException
from src.domain.exceptions.vehicle_not_found_exception import VehicleNotFoundException


class TestUpdateVehicleStatusUseCase:
    """Test cases for UpdateVehicleStatusUseCase - HU-005."""

    def test_update_status_to_in_maintenance_successfully(self, vehicle_repository) -> None:
        """
        Given: A vehicle with status 'active'
        When: Updating status to 'in_maintenance'
        Then: Vehicle status should be updated
        And: Vehicle should be persisted
        And: Status timestamp should be updated

        Business Rules: RN-025, RN-028
        """
        # Arrange
        vehicle = Vehicle(id="V-123", plate="ABC-123", model="Toyota", current_mileage=5000, status=VehicleStatus.ACTIVE)
        vehicle_repository.save(vehicle)

        use_case = UpdateVehicleStatusUseCase(vehicle_repository=vehicle_repository)
        command = UpdateStatusCommand(vehicle_id="V-123", new_status="in_maintenance")

        # Act
        result = use_case.execute(command)

        # Assert
        assert isinstance(result, VehicleDTO)
        assert result.status == "in_maintenance"

        updated_vehicle = vehicle_repository.get_by_id("V-123")
        assert updated_vehicle.status == VehicleStatus.IN_MAINTENANCE

    def test_update_status_to_retired_successfully(self, vehicle_repository) -> None:
        """
        Given: A vehicle with status 'active'
        When: Updating status to 'retired'
        Then: Vehicle status should be updated to retired

        Business Rules: RN-025, RN-026
        """
        # Arrange
        vehicle = Vehicle(id="V-123", plate="ABC-123", model="Toyota", current_mileage=5000, status=VehicleStatus.ACTIVE)
        vehicle_repository.save(vehicle)

        use_case = UpdateVehicleStatusUseCase(vehicle_repository=vehicle_repository)
        command = UpdateStatusCommand(vehicle_id="V-123", new_status="retired")

        # Act
        result = use_case.execute(command)

        # Assert
        assert result.status == "retired"
        updated_vehicle = vehicle_repository.get_by_id("V-123")
        assert updated_vehicle.status == VehicleStatus.RETIRED

    def test_update_status_to_inactive_successfully(self, vehicle_repository) -> None:
        """
        Given: A vehicle with status 'active'
        When: Updating status to 'inactive'
        Then: Vehicle status should be updated to inactive

        Business Rules: RN-025
        """
        # Arrange
        vehicle = Vehicle(id="V-123", plate="ABC-123", model="Toyota", current_mileage=5000, status=VehicleStatus.ACTIVE)
        vehicle_repository.save(vehicle)

        use_case = UpdateVehicleStatusUseCase(vehicle_repository=vehicle_repository)
        command = UpdateStatusCommand(vehicle_id="V-123", new_status="inactive")

        # Act
        result = use_case.execute(command)

        # Assert
        assert result.status == "inactive"
        updated_vehicle = vehicle_repository.get_by_id("V-123")
        assert updated_vehicle.status == VehicleStatus.INACTIVE

    def test_update_status_with_invalid_status_raises_exception(self, vehicle_repository) -> None:
        """
        Given: A vehicle with status 'active'
        When: Attempting to update with invalid status 'invalid_status'
        Then: Should raise InvalidStatusException

        Business Rules: RN-025
        """
        # Arrange
        vehicle = Vehicle(id="V-123", plate="ABC-123", model="Toyota", current_mileage=5000, status=VehicleStatus.ACTIVE)
        vehicle_repository.save(vehicle)

        use_case = UpdateVehicleStatusUseCase(vehicle_repository=vehicle_repository)
        command = UpdateStatusCommand(vehicle_id="V-123", new_status="invalid_status")

        # Act & Assert
        with pytest.raises(InvalidStatusException) as exc_info:
            use_case.execute(command)

        assert "Estado inválido 'invalid_status'" in str(exc_info.value)

    def test_update_status_with_nonexistent_vehicle_raises_exception(self, vehicle_repository) -> None:
        """
        Given: No vehicle exists with ID 'V-999'
        When: Attempting to update status
        Then: Should raise VehicleNotFoundException
        """
        # Arrange
        use_case = UpdateVehicleStatusUseCase(vehicle_repository=vehicle_repository)
        command = UpdateStatusCommand(vehicle_id="V-999", new_status="inactive")

        # Act & Assert
        with pytest.raises(VehicleNotFoundException):
            use_case.execute(command)

    def test_update_status_case_insensitive(self, vehicle_repository) -> None:
        """
        Given: A vehicle with status 'active'
        When: Updating status with uppercase 'IN_MAINTENANCE'
        Then: Should accept and convert to lowercase
        And: Vehicle status should be updated
        """
        # Arrange
        vehicle = Vehicle(id="V-123", plate="ABC-123", model="Toyota", current_mileage=5000, status=VehicleStatus.ACTIVE)
        vehicle_repository.save(vehicle)

        use_case = UpdateVehicleStatusUseCase(vehicle_repository=vehicle_repository)
        command = UpdateStatusCommand(vehicle_id="V-123", new_status="IN_MAINTENANCE")

        # Act
        result = use_case.execute(command)

        # Assert
        assert result.status == "in_maintenance"
        updated_vehicle = vehicle_repository.get_by_id("V-123")
        assert updated_vehicle.status == VehicleStatus.IN_MAINTENANCE
