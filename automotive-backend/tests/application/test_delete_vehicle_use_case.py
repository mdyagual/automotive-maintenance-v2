"""Tests for DeleteVehicleUseCase - Application layer."""

from datetime import datetime

import pytest
from unittest.mock import Mock

from src.application.use_cases.delete_vehicle_use_case import DeleteVehicleUseCase
from src.domain.entities.maintenance_alert import AlertType, MaintenanceAlert
from src.domain.entities.vehicle import Vehicle
from src.domain.exceptions.vehicle_not_found_exception import (
    VehicleNotFoundException,
)


class TestDeleteVehicleUseCase:
    """Test suite for DeleteVehicleUseCase."""

    def test_delete_vehicle_successfully(self, vehicle_repository):
        """
        Test deleting an existing vehicle.

        Given a vehicle exists in the system
        When delete use case is executed with the vehicle ID
        Then the vehicle should be removed from the database
        And subsequent queries for the vehicle should raise VehicleNotFoundException
        """
        # Arrange
        vehicle = Vehicle(
            id="V-999", plate="XYZ-999", model="Honda Accord", current_mileage=20000
        )
        vehicle_repository.save(vehicle)

        use_case = DeleteVehicleUseCase(vehicle_repository=vehicle_repository)

        # Act
        use_case.execute(vehicle_id="V-999")

        # Assert
        with pytest.raises(VehicleNotFoundException):
            vehicle_repository.get_by_id("V-999")

    def test_delete_nonexistent_vehicle_raises_exception(self, vehicle_repository):
        """
        Test deleting a vehicle that doesn't exist.

        Given no vehicle exists with the given ID
        When delete use case is executed
        Then VehicleNotFoundException should be raised
        And the error message should indicate vehicle not found
        """
        # Arrange
        use_case = DeleteVehicleUseCase(vehicle_repository=vehicle_repository)

        # Act & Assert
        with pytest.raises(VehicleNotFoundException) as exc_info:
            use_case.execute(vehicle_id="V-NONEXISTENT")

        assert "Vehículo con ID V-NONEXISTENT no encontrado" in str(exc_info.value)

    """
    Tests to demonstrate Clean Architecture violation: Missing Application Layer DTOs.
    
    ARCHITECTURAL FLAW:
    - Use case accepts primitive parameter instead of Command DTO
    - Use case returns None instead of DTO
    - No confirmation of deletion operation
    """

    def test_use_case_should_accept_command_dto_not_primitive(self):
        """
        ARCHITECTURAL VIOLATION TEST: Use case accepts primitive parameter instead of Command DTO.
        
        This test FAILS because:
        - DeleteVehicleUseCase.execute() accepts a primitive string parameter
        - Should accept a single Command DTO (e.g., DeleteVehicleCommand)
        
        CORRECT IMPLEMENTATION should:
        - Accept DeleteVehicleCommand DTO as single parameter
        - Provide clear contract for use case input
        """
        # Arrange
        mock_repository = Mock()
        
        use_case = DeleteVehicleUseCase(vehicle_repository=mock_repository)
        
        # Act & Assert - THIS SHOULD FAIL
        import inspect
        sig = inspect.signature(use_case.execute)
        params = list(sig.parameters.keys())
        
        # Check if it accepts primitive parameter (violation)
        has_primitive_params = len(params) > 2  # More than self and command
        
        assert not has_primitive_params, (
            "ARCHITECTURAL VIOLATION: Use case accepts primitive parameter "
            "(vehicle_id: str) instead of a Command DTO. "
            f"Current parameters: {params}. "
            "Expected: execute(self, command: DeleteVehicleCommand). "
            "Using DTOs provides better encapsulation and validation."
        )

    def test_use_case_should_return_confirmation_dto_not_none(self):
        """
        ARCHITECTURAL VIOLATION TEST: Use case returns None instead of confirmation DTO.
        
        This test FAILS because:
        - DeleteVehicleUseCase.execute() returns None
        - Should return a DTO confirming the deletion
        - No way to verify operation success without querying repository
        
        CORRECT IMPLEMENTATION should:
        - Return DeleteVehicleResultDTO with confirmation
        - Include deleted vehicle ID and timestamp
        - Provide clear output contract
        """
        # Arrange
        mock_repository = Mock()
        vehicle = Vehicle(
            id="V-001",
            plate="ABC-123",
            model="Toyota Corolla",
            current_mileage=5000
        )
        mock_repository.get_by_id.return_value = vehicle
        mock_repository.delete = Mock()
        
        use_case = DeleteVehicleUseCase(vehicle_repository=mock_repository)
        
        # Act
        result = use_case.execute(vehicle_id="V-001")
        
        # Assert - THIS SHOULD FAIL
        assert result is not None, (
            "ARCHITECTURAL VIOLATION: Use case returns None instead of a confirmation DTO. "
            "Expected: DeleteVehicleResultDTO with operation confirmation. "
            "Got: None. "
            "Use cases should return DTOs to provide clear output contracts "
            "and enable result verification (e.g., deleted_vehicle_id, timestamp)."
        )

    def test_use_case_return_type_should_be_dto_not_none(self):
        """
        ARCHITECTURAL VIOLATION TEST: Use case return type annotation shows None.
        
        This test FAILS because:
        - Method signature shows -> None
        - Should show -> DeleteVehicleResultDTO
        - Type hints reveal missing output contract
        
        CORRECT IMPLEMENTATION should:
        - Use -> DeleteVehicleResultDTO in method signature
        - Provide clear API contract
        """
        # Arrange
        use_case = DeleteVehicleUseCase(vehicle_repository=Mock())
        
        # Act - Check return type annotation
        import inspect
        sig = inspect.signature(use_case.execute)
        return_annotation = sig.return_annotation
        
        # Assert - THIS SHOULD FAIL
        is_none_return = (return_annotation is None or 
                         return_annotation == type(None) or
                         str(return_annotation) == 'None')
        
        assert not is_none_return, (
            "ARCHITECTURAL VIOLATION: Use case method signature declares return type "
            f"as '{return_annotation}' (None). "
            "Use cases should return DTOs to provide clear output contracts. "
            "Expected: DeleteVehicleResultDTO or similar application layer DTO. "
            "This violates Clean Architecture principles of clear boundaries."
        )

    def test_delete_vehicle_cascades_alerts(
        self, vehicle_repository, alert_repository
    ):
        """
        Test that deleting a vehicle also deletes all associated alerts (cascade).

        Given a vehicle exists with multiple alerts
        When the vehicle is deleted
        Then all alerts associated with that vehicle should also be deleted
        And no orphan alerts should remain in the database
        """
        # Arrange
        vehicle = Vehicle(
            id="V-777", plate="ABC-777", model="Toyota Camry", current_mileage=30000
        )
        vehicle_repository.save(vehicle)

        # Create multiple alerts for the vehicle
        alert1 = MaintenanceAlert(
            id="A-001",
            vehicle_id="V-777",
            alert_type=AlertType.BASIC_MAINTENANCE,
            mileage=10000,
            timestamp=datetime.now(),
        )
        alert2 = MaintenanceAlert(
            id="A-002",
            vehicle_id="V-777",
            alert_type=AlertType.MAJOR_MAINTENANCE,
            mileage=50000,
            timestamp=datetime.now(),
        )
        alert3 = MaintenanceAlert(
            id="A-003",
            vehicle_id="V-777",
            alert_type=AlertType.CRITICAL_THRESHOLD,
            mileage=100000,
            timestamp=datetime.now(),
        )
        alert_repository.save(alert1)
        alert_repository.save(alert2)
        alert_repository.save(alert3)

        # Verify alerts exist before deletion
        alerts_before = alert_repository.get_by_vehicle_id("V-777")
        assert len(alerts_before) == 3

        use_case = DeleteVehicleUseCase(vehicle_repository=vehicle_repository)

        # Act
        use_case.execute(vehicle_id="V-777")

        # Assert - Vehicle deleted
        with pytest.raises(VehicleNotFoundException):
            vehicle_repository.get_by_id("V-777")

        # Assert - Alerts cascaded (deleted automatically)
        alerts_after = alert_repository.get_by_vehicle_id("V-777")
        assert len(alerts_after) == 0, "No orphan alerts should remain after vehicle deletion"
