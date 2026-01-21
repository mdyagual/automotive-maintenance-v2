"""Tests for RegisterVehicleUseCase following TDD approach."""

import pytest
from unittest.mock import Mock
from src.application.dtos.vehicle_dtos import RegisterVehicleCommand, VehicleDTO
from src.application.use_cases.register_vehicle_use_case import RegisterVehicleUseCase
from src.domain.entities.vehicle import Vehicle
from src.domain.exceptions.vehicle_not_found_exception import VehicleNotFoundException


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
        use_case = RegisterVehicleUseCase(vehicle_repository=vehicle_repository)
        
        command = RegisterVehicleCommand(
            vehicle_id="V-456",
            plate="XYZ-789",
            model="Honda Civic",
            initial_mileage=0
        )

        # Act
        result = use_case.execute(command)

        # Assert
        assert isinstance(result, VehicleDTO)
        assert result.id == "V-456"
        assert result.plate == "XYZ-789"
        assert result.model == "Honda Civic"
        assert result.current_mileage == 0
        
        # Verify it was saved
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
        from src.domain.exceptions.duplicate_vehicle_exception import (
            DuplicateVehicleException,
        )

        # Create existing vehicle
        existing_vehicle = Vehicle(
            id="V-123", plate="ABC-123", model="Toyota Corolla", current_mileage=5000
        )
        vehicle_repository.save(existing_vehicle)

        use_case = RegisterVehicleUseCase(vehicle_repository=vehicle_repository)
        
        command = RegisterVehicleCommand(
            vehicle_id="V-123",
            plate="XYZ-999",
            model="Different Model",
            initial_mileage=0
        )

        # Act & Assert
        with pytest.raises(
            DuplicateVehicleException, match="Ya existe un vehículo con ID V-123"
        ):
            use_case.execute(command)
    """
    Tests to demonstrate Clean Architecture violation: Missing Application Layer DTOs.

    ARCHITECTURAL FLAW:
    - Use cases return domain entities (Vehicle) instead of DTOs
    - Web layer receives and accesses domain entities directly
    - Domain entities can be modified by outer layers
    - No clear boundary between application and web layers

    EXPECTED BEHAVIOR (after fix):
    - Use cases should accept Command DTOs as input
    - Use cases should return Data DTOs as output
    - Domain entities should never leave the domain/application layers
    - Web layer should only work with DTOs
    """

    def test_use_case_should_not_return_domain_entity(self):
        """
        ARCHITECTURAL VIOLATION TEST: Use case returns domain entity instead of DTO.
        
        This test PASSES NOW because:
        - RegisterVehicleUseCase.execute() returns a VehicleDTO (application DTO)
        - Domain entities are kept encapsulated
        - Clear layer boundaries are maintained
        """
        # Arrange
        mock_repository = Mock()
        mock_repository.get_by_id.side_effect = VehicleNotFoundException("Not found")
        mock_repository.save = Mock()
        
        use_case = RegisterVehicleUseCase(
            vehicle_repository=mock_repository,
            alert_repository=None,
            strategies=[]
        )
        
        command = RegisterVehicleCommand(
            vehicle_id="V-001",
            plate="ABC-123",
            model="Toyota Corolla",
            initial_mileage=5000
        )
        
        # Act
        result = use_case.execute(command)
        
        # Assert - THIS SHOULD NOW PASS
        # The result should be a DTO, not a domain entity
        assert isinstance(result, VehicleDTO), (
            f"Expected VehicleDTO, got {type(result).__name__}"
        )
        assert not isinstance(result, Vehicle), (
            "Use case should return DTO, not domain entity"
        )

    def test_use_case_should_accept_command_dto_not_primitives(self):
        """
        ARCHITECTURAL VIOLATION TEST: Use case accepts primitive parameters instead of Command DTO.
        
        This test PASSES NOW because:
        - RegisterVehicleUseCase.execute() accepts RegisterVehicleCommand DTO
        - Clear contract for use case input
        - Better encapsulation and validation
        """
        # Arrange
        mock_repository = Mock()
        mock_repository.get_by_id.side_effect = VehicleNotFoundException("Not found")
        mock_repository.save = Mock()
        
        use_case = RegisterVehicleUseCase(
            vehicle_repository=mock_repository,
            alert_repository=None,
            strategies=[]
        )
        
        # Act & Assert - THIS SHOULD NOW PASS
        # The execute method should accept a Command DTO
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
        
        # Verify the parameter is named 'command'
        assert 'command' in params, (
            f"Expected parameter named 'command', got: {params}"
        )

    def test_domain_entity_should_not_be_mutable_by_web_layer(self):
        """
        ARCHITECTURAL VIOLATION TEST: Domain entity is exposed and can be modified by web layer.
        
        This test PASSES NOW because:
        - Use case returns immutable DTO (frozen dataclass)
        - Web layer cannot modify the DTO's state
        - Business rules are enforced at domain boundary
        """
        # Arrange
        mock_repository = Mock()
        mock_repository.get_by_id.side_effect = VehicleNotFoundException("Not found")
        mock_repository.save = Mock()
        
        use_case = RegisterVehicleUseCase(
            vehicle_repository=mock_repository,
            alert_repository=None,
            strategies=[]
        )
        
        command = RegisterVehicleCommand(
            vehicle_id="V-001",
            plate="ABC-123",
            model="Toyota Corolla",
            initial_mileage=5000
        )
        
        # Act
        result = use_case.execute(command)
        
        # Assert - THIS SHOULD NOW PASS
        # The result should be immutable (frozen dataclass)
        original_mileage = result.current_mileage
        
        # Try to modify the DTO (should raise FrozenInstanceError)
        try:
            result.current_mileage = 999999
            is_mutable = True
        except (AttributeError, Exception):
            is_mutable = False
        
        assert not is_mutable, (
            "DTO should be immutable (frozen dataclass). "
            "Web layer should not be able to modify it."
        )

    def test_use_case_return_type_should_be_dto_not_entity(self):
        """
        ARCHITECTURAL VIOLATION TEST: Use case return type annotation shows domain entity.
        
        This test PASSES NOW because:
        - Method signature shows -> VehicleDTO (application DTO)
        - Domain entities are kept internal
        - Clear API contract
        """
        # Arrange
        use_case = RegisterVehicleUseCase(
            vehicle_repository=Mock(),
            alert_repository=None,
            strategies=[]
        )
        
        # Act - Check return type annotation
        import inspect
        sig = inspect.signature(use_case.execute)
        return_annotation = sig.return_annotation
        
        # Assert - THIS SHOULD NOW PASS
        # Return type should be VehicleDTO
        is_dto = (return_annotation == VehicleDTO or 
                 (hasattr(return_annotation, '__name__') and return_annotation.__name__ == 'VehicleDTO'))
        
        assert is_dto, (
            f"Use case should return VehicleDTO. "
            f"Got: {return_annotation}"
        )
        
        # Ensure it's NOT a domain entity
        is_domain_entity = (return_annotation == Vehicle or 
                           (hasattr(return_annotation, '__name__') and return_annotation.__name__ == 'Vehicle'))
        
        assert not is_domain_entity, (
            "Use case should not return domain entity in type signature"
        )

    def test_web_layer_should_not_access_domain_entity_properties(self):
        """
        ARCHITECTURAL VIOLATION TEST: Web layer accesses domain entity properties directly.
        
        This test PASSES NOW because:
        - Web layer receives DTO from use case
        - DTO has no business logic methods
        - No direct access to domain entities
        """
        # Arrange
        mock_repository = Mock()
        mock_repository.get_by_id.side_effect = VehicleNotFoundException("Not found")
        mock_repository.save = Mock()
        
        use_case = RegisterVehicleUseCase(
            vehicle_repository=mock_repository,
            alert_repository=None,
            strategies=[]
        )
        
        command = RegisterVehicleCommand(
            vehicle_id="V-001",
            plate="ABC-123",
            model="Toyota Corolla",
            initial_mileage=5000
        )
        
        # Act - Simulate what web layer does
        vehicle_dto = use_case.execute(command)
        
        # Web layer accesses DTO properties (this is correct)
        response_data = {
            "id": vehicle_dto.id,
            "plate": vehicle_dto.plate,
            "model": vehicle_dto.model,
            "current_mileage": vehicle_dto.current_mileage,
        }
        
        # Assert - THIS SHOULD NOW PASS
        # Check that we're NOT accessing a domain entity (no business logic methods)
        has_domain_methods = (
            hasattr(vehicle_dto, 'attach') and
            hasattr(vehicle_dto, 'update_mileage') and
            hasattr(vehicle_dto, '_notify_observers')
        )
        
        assert not has_domain_methods, (
            "Web layer should receive DTO without business logic methods. "
            f"Got object with methods: {[m for m in dir(vehicle_dto) if not m.startswith('_')]}"
        )
        
        # Verify it's a DTO
        assert isinstance(vehicle_dto, VehicleDTO), (
            f"Expected VehicleDTO, got {type(vehicle_dto).__name__}"
        )
