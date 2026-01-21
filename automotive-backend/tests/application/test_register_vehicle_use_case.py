"""Tests for RegisterVehicleUseCase following TDD approach."""

import pytest
from unittest.mock import Mock
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
        
        This test FAILS because:
        - RegisterVehicleUseCase.execute() returns a Vehicle (domain entity)
        - Domain entities should NEVER be exposed outside domain/application layers
        - Use cases should return DTOs, not entities
        
        CORRECT IMPLEMENTATION should:
        - Return a VehicleDTO (application layer DTO)
        - Keep domain entities encapsulated
        - Provide clear layer boundaries
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
        
        # Act
        result = use_case.execute(
            vehicle_id="V-001",
            plate="ABC-123",
            model="Toyota Corolla",
            initial_mileage=5000
        )
        
        # Assert - THIS SHOULD FAIL
        # The result should NOT be a domain entity
        assert not isinstance(result, Vehicle), (
            "ARCHITECTURAL VIOLATION: Use case returns domain entity (Vehicle) "
            "instead of a DTO. Domain entities should never leave the application layer. "
            "Expected: VehicleDTO or similar DTO class. "
            "Got: Vehicle domain entity."
        )

    def test_use_case_should_accept_command_dto_not_primitives(self):
        """
        ARCHITECTURAL VIOLATION TEST: Use case accepts primitive parameters instead of Command DTO.
        
        This test FAILS because:
        - RegisterVehicleUseCase.execute() accepts individual primitive parameters
        - Should accept a single Command DTO (e.g., RegisterVehicleCommand)
        - Primitive parameters make validation and evolution difficult
        
        CORRECT IMPLEMENTATION should:
        - Accept RegisterVehicleCommand DTO as single parameter
        - Validate the command at application boundary
        - Provide clear contract for use case input
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
        
        # Act & Assert - THIS SHOULD FAIL
        # The execute method should accept a Command DTO, not primitives
        import inspect
        sig = inspect.signature(use_case.execute)
        params = list(sig.parameters.keys())
        
        # Check if it accepts multiple primitive parameters (violation)
        has_primitive_params = len(params) > 2  # More than self and command
        
        assert not has_primitive_params, (
            "ARCHITECTURAL VIOLATION: Use case accepts primitive parameters "
            "(vehicle_id, plate, model, initial_mileage) instead of a Command DTO. "
            f"Current parameters: {params}. "
            "Expected: execute(self, command: RegisterVehicleCommand). "
            "Using DTOs provides better encapsulation and validation."
        )

    def test_domain_entity_should_not_be_mutable_by_web_layer(self):
        """
        ARCHITECTURAL VIOLATION TEST: Domain entity is exposed and can be modified by web layer.
        
        This test FAILS because:
        - Use case returns mutable domain entity
        - Web layer can modify the entity's state
        - Business rules can be bypassed
        - Breaks encapsulation
        
        CORRECT IMPLEMENTATION should:
        - Return immutable DTO (frozen dataclass)
        - Prevent outer layers from modifying domain state
        - Enforce business rules at domain boundary
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
        
        # Act
        result = use_case.execute(
            vehicle_id="V-001",
            plate="ABC-123",
            model="Toyota Corolla",
            initial_mileage=5000
        )
        
        # Simulate web layer modifying the entity (SHOULD NOT BE POSSIBLE)
        original_mileage = result.current_mileage
        
        # Web layer can directly modify domain entity - THIS IS THE VIOLATION
        result.current_mileage = 999999  # Bypassing business rules!
        result.plate = "HACKED"  # Bypassing validation!
        
        # Assert - THIS SHOULD FAIL
        # The result should be immutable or at least not a domain entity
        is_mutable = (result.current_mileage != original_mileage)
        
        assert not is_mutable, (
            "ARCHITECTURAL VIOLATION: Domain entity returned by use case is mutable "
            "and can be modified by outer layers (web layer). "
            "This allows bypassing business rules and validation. "
            "Expected: Immutable DTO (frozen dataclass). "
            "Got: Mutable Vehicle domain entity that can be modified directly."
        )

    def test_use_case_return_type_should_be_dto_not_entity(self):
        """
        ARCHITECTURAL VIOLATION TEST: Use case return type annotation shows domain entity.
        
        This test FAILS because:
        - Method signature shows -> Vehicle (domain entity)
        - Should show -> VehicleDTO (application DTO)
        - Type hints reveal architectural violation
        
        CORRECT IMPLEMENTATION should:
        - Use -> VehicleDTO in method signature
        - Keep domain entities internal
        - Provide clear API contract
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
        
        # Assert - THIS SHOULD FAIL
        # Return type should NOT be Vehicle (domain entity)
        is_domain_entity = (return_annotation == Vehicle or 
                           return_annotation.__name__ == 'Vehicle' if hasattr(return_annotation, '__name__') else False)
        
        assert not is_domain_entity, (
            "ARCHITECTURAL VIOLATION: Use case method signature declares return type "
            f"as '{return_annotation}' (domain entity). "
            "Domain entities should never be exposed in use case signatures. "
            "Expected: VehicleDTO or similar application layer DTO. "
            "This violates the Dependency Rule of Clean Architecture."
        )

    def test_web_layer_should_not_access_domain_entity_properties(self):
        """
        ARCHITECTURAL VIOLATION TEST: Web layer accesses domain entity properties directly.
        
        This test simulates what happens in main.py where:
        - Web layer receives domain entity from use case
        - Web layer accesses entity.id, entity.plate, etc.
        - Creates tight coupling between layers
        
        CORRECT IMPLEMENTATION should:
        - Web layer receives DTO from use case
        - Web layer maps DTO to response model
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
        
        # Act - Simulate what web layer does (from main.py lines 145-149)
        vehicle = use_case.execute(
            vehicle_id="V-001",
            plate="ABC-123",
            model="Toyota Corolla",
            initial_mileage=5000
        )
        
        # Web layer accesses domain entity properties directly
        response_data = {
            "id": vehicle.id,  # Direct access to domain entity
            "plate": vehicle.plate,  # Direct access to domain entity
            "model": vehicle.model,  # Direct access to domain entity
            "current_mileage": vehicle.current_mileage,  # Direct access to domain entity
        }
        
        # Assert - THIS SHOULD FAIL
        # Check if we're accessing a domain entity (has domain-specific methods)
        has_domain_methods = (
            hasattr(vehicle, 'attach') and  # Observer pattern method
            hasattr(vehicle, 'update_mileage') and  # Business logic method
            hasattr(vehicle, '_notify_observers')  # Internal domain method
        )
        
        assert not has_domain_methods, (
            "ARCHITECTURAL VIOLATION: Web layer is accessing a domain entity directly. "
            "The object returned by use case has domain-specific methods "
            "(attach, update_mileage, _notify_observers), proving it's a domain entity. "
            "Web layer should only receive DTOs without business logic methods. "
            "This creates tight coupling and exposes domain internals to outer layers."
        )
