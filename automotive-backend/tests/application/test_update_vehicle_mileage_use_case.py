"""Tests for UpdateVehicleMileageUseCase following TDD approach."""

import inspect
import pytest
from unittest.mock import Mock

from src.application.dtos.vehicle_dtos import UpdateMileageCommand, VehicleDTO
from src.application.use_cases.update_vehicle_mileage_use_case import (
    UpdateVehicleMileageUseCase,
)
from src.domain.entities.maintenance_alert import AlertType
from src.domain.entities.vehicle import Vehicle
from src.domain.exceptions.invalid_mileage_exception import InvalidMileageException
from src.domain.exceptions.vehicle_not_found_exception import VehicleNotFoundException
from src.domain.ports.observer import Observer


class TestUpdateVehicleMileageUseCase:
    """Test cases for UpdateVehicleMileageUseCase."""

    def test_update_mileage_successfully(
        self, vehicle_repository, observer_factory
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
            observer_factory=observer_factory
        )
        
        command = UpdateMileageCommand(
            vehicle_id="V-123",
            new_mileage=8000
        )

        # Act
        result = use_case.execute(command)

        # Assert
        assert isinstance(result, VehicleDTO)
        assert result.current_mileage == 8000
        
        updated_vehicle = vehicle_repository.get_by_id("V-123")
        assert updated_vehicle.current_mileage == 8000

    def test_update_mileage_with_invalid_value_raises_exception(
        self, vehicle_repository, observer_factory
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
            observer_factory=observer_factory
        )
        
        command = UpdateMileageCommand(
            vehicle_id="V-123",
            new_mileage=4000
        )

        # Act & Assert
        with pytest.raises(InvalidMileageException):
            use_case.execute(command)

    def test_update_mileage_crossing_10k_threshold_generates_alert(
        self, vehicle_repository, observer_factory, alert_repository
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
            observer_factory=observer_factory
        )
        
        command = UpdateMileageCommand(
            vehicle_id="V-123",
            new_mileage=10001
        )

        # Act
        use_case.execute(command)

        # Assert
        alerts = alert_repository.get_all()
        assert len(alerts) == 1
        alert = alerts[0]
        assert alert.vehicle_id == "V-123"
        assert alert.mileage == 10001  # Ahora el umbral exacto
        assert alert.alert_type == AlertType.BASIC_MAINTENANCE

    """
    Tests to demonstrate Clean Architecture violation: Missing Application Layer DTOs.
    
    ARCHITECTURAL FLAW:
    - Use case accepts primitive parameters instead of Command DTO
    - Use case returns None instead of DTO
    - No clear output contract
    """

    def test_use_case_should_accept_command_dto_not_primitives(self):
        """
        ARCHITECTURAL VIOLATION TEST: Use case accepts primitive parameters instead of Command DTO.
        
        This test PASSES NOW because:
        - UpdateVehicleMileageUseCase.execute() accepts UpdateMileageCommand DTO
        - Clear contract for use case input
        """
        # Arrange
        mock_repository = Mock()
        mock_observer_factory = Mock()
        
        use_case = UpdateVehicleMileageUseCase(
            vehicle_repository=mock_repository,
            observer_factory=mock_observer_factory
        )
        
        # Act & Assert - THIS SHOULD NOW PASS
        sig = inspect.signature(use_case.execute)
        params = list(sig.parameters.keys())
        
        # Check if it accepts a single command parameter (correct)
        has_primitive_params = len(params) > 2  # More than self and command
        
        assert not has_primitive_params, (
            f"Use case should accept a single Command DTO. "
            f"Current parameters: {params}. "
            f"Expected: ['self', 'command']"
        )
        
        assert 'command' in params, f"Expected parameter named 'command', got: {params}"

    def test_use_case_should_return_dto_not_none(self):
        """
        ARCHITECTURAL VIOLATION TEST: Use case returns None instead of DTO.
        
        This test PASSES NOW because:
        - UpdateVehicleMileageUseCase.execute() returns VehicleDTO
        - Clear output contract
        """
        # Arrange
        mock_repository = Mock()
        mock_observer_factory = Mock()
        mock_observer = Mock()
        
        mock_observer_factory.create_maintenance_observer.return_value = mock_observer
        
        vehicle = Vehicle(
            id="V-001",
            plate="ABC-123",
            model="Toyota Corolla",
            current_mileage=5000
        )
        mock_repository.get_by_id.return_value = vehicle
        mock_repository.save = Mock()
        
        use_case = UpdateVehicleMileageUseCase(
            vehicle_repository=mock_repository,
            observer_factory=mock_observer_factory
        )
        
        command = UpdateMileageCommand(
            vehicle_id="V-001",
            new_mileage=15000
        )
        
        # Act
        result = use_case.execute(command)
        
        # Assert - THIS SHOULD NOW PASS
        assert result is not None, "Use case should return a DTO"
        assert isinstance(result, VehicleDTO), f"Expected VehicleDTO, got {type(result).__name__}"

    def test_use_case_return_type_should_be_dto_not_none(self):
        """
        ARCHITECTURAL VIOLATION TEST: Use case return type annotation shows None.
        
        This test PASSES NOW because:
        - Method signature shows -> VehicleDTO
        - Clear API contract
        """
        # Arrange
        use_case = UpdateVehicleMileageUseCase(
            vehicle_repository=Mock(),
            observer_factory=Mock()
        )
        
        # Act - Check return type annotation
        sig = inspect.signature(use_case.execute)
        return_annotation = sig.return_annotation
        
        # Assert - THIS SHOULD NOW PASS
        is_dto = (return_annotation == VehicleDTO or 
                 (hasattr(return_annotation, '__name__') and return_annotation.__name__ == 'VehicleDTO'))
        
        assert is_dto, f"Use case should return VehicleDTO. Got: {return_annotation}"
        
        is_none_return = (return_annotation is None or 
                         return_annotation == type(None) or
                         str(return_annotation) == 'None')
        
        assert not is_none_return, "Use case should not return None"

    def test_execute_uses_factory_to_create_observer(self):
        """
        1. If the code imports direct infrastructure, it will fail when attempting to mock.
        2. If the code instantiates 'MaintenanceAlertObserver' directly, it will ignore our mock factory.
        3. If the constructor does not accept 'observer_factory', it will throw a TypeError.
        """
        # Arrange
        mock_repo = Mock()
        mock_observer_factory = Mock()
        mock_observer = Mock()
        
        # We configure the factory: "When they ask you for an observer, give them this fake one."
        mock_observer_factory.create_maintenance_observer.return_value = mock_observer
        
        vehicle_mock = Mock()
        vehicle_mock.current_mileage = 5000
        mock_repo.get_by_id.return_value = vehicle_mock

        # ACT (We try to instantiate the use case by INJECTING the factory)
        use_case = UpdateVehicleMileageUseCase(
            vehicle_repository=mock_repo,
            observer_factory=mock_observer_factory  # <--- La inyección clave
        )

        command = UpdateMileageCommand(vehicle_id="V-1", new_mileage=6000)
        
        # We execute
        use_case.execute(command)

        # ASSERT (We verify behavior, not text)
        
        # 1. We verify that the factory was used (and not a direct 'new Observer' instantiation).
        mock_observer_factory.create_maintenance_observer.assert_called_once_with(
            vehicle_id="V-1",
            initial_mileage=5000
        )
        
        #2. We verified that the observer created was attached to the vehicle.
        vehicle_mock.attach.assert_called_once_with(mock_observer)
        
        #3. We verified that the mileage was updated.
        vehicle_mock.update_mileage.assert_called_once_with(6000)

    def test_update_mileage_on_retired_vehicle_raises_exception(
        self, vehicle_repository, observer_factory
    ) -> None:
        """
        Test that updating mileage on a retired vehicle is rejected.
        
        Given: A vehicle 'V-789' with status 'retired'
        When: I attempt to update the vehicle mileage
        Then: The system should reject the operation
        And: Should raise InvalidMileageException
        And: The message should indicate "No se puede actualizar kilometraje de vehículos retirados"
        
        User Story: HU-005 - Escenario 5
        Business Rule: RN-027 - Cannot update mileage of retired vehicles
        """
        from src.domain.entities.vehicle_status import VehicleStatus
        
        # Arrange
        vehicle = Vehicle(
            id="V-789",
            plate="DEF-789",
            model="Ford Focus",
            current_mileage=200000,
            status=VehicleStatus.RETIRED
        )
        vehicle_repository.save(vehicle)

        use_case = UpdateVehicleMileageUseCase(
            vehicle_repository=vehicle_repository,
            observer_factory=observer_factory
        )
        
        command = UpdateMileageCommand(
            vehicle_id="V-789",
            new_mileage=205000
        )

        # Act & Assert
        with pytest.raises(InvalidMileageException) as exc_info:
            use_case.execute(command)
        
        # Verify error message indicates retired vehicle restriction
        error_message = str(exc_info.value)
        assert "retirado" in error_message.lower() or "retired" in error_message.lower(), \
            f"Error message should indicate retired vehicle restriction. Got: {error_message}"
        
        # Verify vehicle mileage was not updated
        unchanged_vehicle = vehicle_repository.get_by_id("V-789")
        assert unchanged_vehicle.current_mileage == 200000, \
            "Vehicle mileage should remain unchanged after failed update"