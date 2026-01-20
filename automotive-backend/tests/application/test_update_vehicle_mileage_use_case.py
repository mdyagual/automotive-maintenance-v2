"""Tests for UpdateVehicleMileageUseCase following TDD approach."""

import pytest

from src.application.use_cases.update_vehicle_mileage_use_case import (
    UpdateVehicleMileageUseCase,
)
from src.domain.entities.maintenance_alert import AlertType
from src.domain.entities.vehicle import Vehicle
from src.domain.exceptions.invalid_mileage_exception import InvalidMileageException


class TestUpdateVehicleMileageUseCase:
    """Test cases for UpdateVehicleMileageUseCase."""

    def test_update_mileage_successfully(
        self, vehicle_repository, alert_repository
    ) -> None:
        """
        Given: A vehicle with 5,000 km
        When: Updating mileage to 8,000 km
        Then: Vehicle mileage should be updated
        And: Vehicle should be persisted
        """
        # Arrange
        vehicle = Vehicle(
            id="V-123", plate="ABC-123", model="Toyota", current_mileage=5000
        )
        vehicle_repository.save(vehicle)

        use_case = UpdateVehicleMileageUseCase(
            vehicle_repository=vehicle_repository,
            alert_repository=alert_repository
        )

        # Act
        use_case.execute(vehicle_id="V-123", new_mileage=8000)

        # Assert
        updated_vehicle = vehicle_repository.get_by_id("V-123")
        assert updated_vehicle.current_mileage == 8000

    def test_update_mileage_with_invalid_value_raises_exception(
        self, vehicle_repository, alert_repository
    ) -> None:
        """
        Given: A vehicle with 5,000 km
        When: Attempting to update with invalid mileage (4,000 km)
        Then: Should raise InvalidMileageException
        """
        # Arrange
        vehicle = Vehicle(
            id="V-123", plate="ABC-123", model="Toyota", current_mileage=5000
        )
        vehicle_repository.save(vehicle)

        use_case = UpdateVehicleMileageUseCase(
            vehicle_repository=vehicle_repository,
            alert_repository=alert_repository
        )

        # Act & Assert
        with pytest.raises(InvalidMileageException):
            use_case.execute(vehicle_id="V-123", new_mileage=4000)

    def test_update_mileage_crossing_10k_threshold_generates_alert(
        self, vehicle_repository, alert_repository
    ) -> None:
        """
        Given: A vehicle with 5,000 km and basic maintenance strategy
        When: Updating mileage to 10,001 km
        Then: Should generate and persist a basic maintenance alert
        """
        # Arrange
        vehicle = Vehicle(
            id="V-123", plate="ABC-123", model="Toyota", current_mileage=5000
        )
        vehicle_repository.save(vehicle)

        use_case = UpdateVehicleMileageUseCase(
            vehicle_repository=vehicle_repository,
            alert_repository=alert_repository
        )

        # Act
        use_case.execute(vehicle_id="V-123", new_mileage=10001)

        # Assert
        alerts = alert_repository.get_all()
        assert len(alerts) == 1
        alert = alerts[0]
        assert alert.vehicle_id == "V-123"
        assert alert.mileage == 10001  # Ahora el umbral exacto
        assert alert.alert_type == AlertType.BASIC_MAINTENANCE
