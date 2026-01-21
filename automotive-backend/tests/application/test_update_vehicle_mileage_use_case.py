"""Tests for UpdateVehicleMileageUseCase following TDD approach."""

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
        
        command = UpdateMileageCommand(
            vehicle_id="V-123",
            new_mileage=4000
        )

        # Act & Assert
        with pytest.raises(InvalidMileageException):
            use_case.execute(command)

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
        mock_alert_repository = Mock()
        
        use_case = UpdateVehicleMileageUseCase(
            vehicle_repository=mock_repository,
            alert_repository=mock_alert_repository,
            strategies=[]
        )
        
        # Act & Assert - THIS SHOULD NOW PASS
        import inspect
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
        mock_alert_repository = Mock()
        
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
            alert_repository=mock_alert_repository,
            strategies=[]
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
            alert_repository=Mock(),
            strategies=[]
        )
        
        # Act - Check return type annotation
        import inspect
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

