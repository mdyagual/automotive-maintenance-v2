"""
Unit tests for GetVehicleUseCase.

These tests will FAIL until GetVehicleUseCase is implemented.
They define the expected behavior of the missing use case.
"""

from unittest.mock import Mock

import pytest

from src.domain.entities.vehicle import Vehicle
from src.domain.exceptions.vehicle_not_found_exception import VehicleNotFoundException


class TestGetVehicleUseCase:
    """
    Tests for GetVehicleUseCase (currently doesn't exist - tests will FAIL).

    These tests define the expected behavior:
    1. Use case should accept vehicle_id as parameter
    2. Use case should return VehicleDTO (not domain entity)
    3. Use case should delegate to repository
    4. Use case should handle VehicleNotFoundException
    """

    @pytest.fixture
    def mock_repository(self):
        """Create a mock vehicle repository."""
        return Mock()

    @pytest.fixture
    def sample_vehicle(self):
        """Create a sample vehicle entity."""
        return Vehicle(id="V-001", plate="ABC-123", model="Toyota Corolla", current_mileage=50000)

    def test_get_vehicle_use_case_exists(self):
        """
        Test that GetVehicleUseCase class exists.

        EXPECTED TO FAIL: GetVehicleUseCase doesn't exist yet.
        """
        try:
            from src.application.use_cases.get_vehicle_use_case import GetVehicleUseCase

            assert GetVehicleUseCase is not None
        except ImportError:
            pytest.fail("GetVehicleUseCase does not exist. Please create it at src/application/use_cases/get_vehicle_use_case.py")

    def test_execute_returns_vehicle_dto_not_entity(self, mock_repository, sample_vehicle):
        """
        Test that execute() returns VehicleDTO, not domain entity.

        EXPECTED TO FAIL: GetVehicleUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - Use case should return VehicleDTO
        - Domain entity should NOT be returned
        """
        try:
            from src.application.dtos.vehicle_dtos import VehicleDTO
            from src.application.use_cases.get_vehicle_use_case import GetVehicleUseCase
        except ImportError:
            pytest.skip("GetVehicleUseCase or VehicleDTO not implemented yet")

        # Arrange
        mock_repository.get_by_id.return_value = sample_vehicle
        use_case = GetVehicleUseCase(vehicle_repository=mock_repository)

        # Act
        result = use_case.execute("V-001")

        # Assert
        assert isinstance(result, VehicleDTO), "Use case should return VehicleDTO"
        assert not isinstance(result, Vehicle), "Use case should NOT return domain entity"
        assert result.id == "V-001"
        assert result.plate == "ABC-123"
        assert result.model == "Toyota Corolla"
        assert result.current_mileage == 50000

    def test_execute_calls_repository_get_by_id(self, mock_repository, sample_vehicle):
        """
        Test that execute() delegates to repository.get_by_id().

        EXPECTED TO FAIL: GetVehicleUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - Use case should call repository.get_by_id(vehicle_id)
        - Use case should pass the correct vehicle_id
        """
        try:
            from src.application.use_cases.get_vehicle_use_case import GetVehicleUseCase
        except ImportError:
            pytest.skip("GetVehicleUseCase not implemented yet")

        # Arrange
        mock_repository.get_by_id.return_value = sample_vehicle
        use_case = GetVehicleUseCase(vehicle_repository=mock_repository)

        # Act
        use_case.execute("V-001")

        # Assert
        mock_repository.get_by_id.assert_called_once_with("V-001")

    def test_execute_raises_vehicle_not_found_exception(self, mock_repository):
        """
        Test that execute() propagates VehicleNotFoundException.

        EXPECTED TO FAIL: GetVehicleUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - If repository raises VehicleNotFoundException, use case should propagate it
        - Exception should not be caught or transformed
        """
        try:
            from src.application.use_cases.get_vehicle_use_case import GetVehicleUseCase
        except ImportError:
            pytest.skip("GetVehicleUseCase not implemented yet")

        # Arrange
        mock_repository.get_by_id.side_effect = VehicleNotFoundException("Vehículo con ID V-999 no encontrado")
        use_case = GetVehicleUseCase(vehicle_repository=mock_repository)

        # Act & Assert
        with pytest.raises(VehicleNotFoundException, match="V-999"):
            use_case.execute("V-999")

    def test_execute_with_different_vehicle_ids(self, mock_repository):
        """
        Test that execute() works with different vehicle IDs.

        EXPECTED TO FAIL: GetVehicleUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - Use case should work with any valid vehicle_id
        - Should return correct data for each vehicle
        """
        try:
            from src.application.use_cases.get_vehicle_use_case import GetVehicleUseCase
        except ImportError:
            pytest.skip("GetVehicleUseCase not implemented yet")

        # Arrange
        vehicle1 = Vehicle(id="V-001", plate="ABC-123", model="Toyota", current_mileage=10000)
        vehicle2 = Vehicle(id="V-002", plate="XYZ-789", model="Honda", current_mileage=20000)

        mock_repository.get_by_id.side_effect = [vehicle1, vehicle2]
        use_case = GetVehicleUseCase(vehicle_repository=mock_repository)

        # Act
        result1 = use_case.execute("V-001")
        result2 = use_case.execute("V-002")

        # Assert
        assert result1.id == "V-001"
        assert result1.plate == "ABC-123"
        assert result1.current_mileage == 10000

        assert result2.id == "V-002"
        assert result2.plate == "XYZ-789"
        assert result2.current_mileage == 20000

    def test_use_case_accepts_repository_in_constructor(self, mock_repository):
        """
        Test that GetVehicleUseCase accepts repository in constructor.

        EXPECTED TO FAIL: GetVehicleUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - Constructor should accept vehicle_repository parameter
        - Should follow dependency injection pattern
        """
        try:
            from src.application.use_cases.get_vehicle_use_case import GetVehicleUseCase
        except ImportError:
            pytest.skip("GetVehicleUseCase not implemented yet")

        # Act
        use_case = GetVehicleUseCase(vehicle_repository=mock_repository)

        # Assert
        assert use_case is not None
        assert hasattr(use_case, "execute"), "Use case should have execute method"

    def test_dto_is_immutable(self, mock_repository, sample_vehicle):
        """
        Test that returned DTO is immutable (frozen dataclass).

        EXPECTED TO FAIL: GetVehicleUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - VehicleDTO should be immutable
        - Attempting to modify should raise exception
        """
        try:
            from src.application.use_cases.get_vehicle_use_case import GetVehicleUseCase
        except ImportError:
            pytest.skip("GetVehicleUseCase not implemented yet")

        # Arrange
        mock_repository.get_by_id.return_value = sample_vehicle
        use_case = GetVehicleUseCase(vehicle_repository=mock_repository)

        # Act
        result = use_case.execute("V-001")

        # Assert - Try to modify DTO (should fail)
        with pytest.raises((AttributeError, Exception)):
            result.current_mileage = 999999

    def test_use_case_does_not_modify_domain_entity(self, mock_repository, sample_vehicle):
        """
        Test that use case doesn't modify the domain entity.

        EXPECTED TO FAIL: GetVehicleUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - Use case should only read from entity
        - Entity state should remain unchanged
        """
        try:
            from src.application.use_cases.get_vehicle_use_case import GetVehicleUseCase
        except ImportError:
            pytest.skip("GetVehicleUseCase not implemented yet")

        # Arrange
        original_mileage = sample_vehicle.current_mileage
        mock_repository.get_by_id.return_value = sample_vehicle
        use_case = GetVehicleUseCase(vehicle_repository=mock_repository)

        # Act
        use_case.execute("V-001")

        # Assert
        assert sample_vehicle.current_mileage == original_mileage, "Entity should not be modified"

    def test_use_case_maps_all_entity_properties_to_dto(self, mock_repository):
        """
        Test that all entity properties are mapped to DTO.

        EXPECTED TO FAIL: GetVehicleUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - All vehicle properties should be in DTO
        - No data should be lost in mapping
        """
        try:
            from src.application.use_cases.get_vehicle_use_case import GetVehicleUseCase
        except ImportError:
            pytest.skip("GetVehicleUseCase not implemented yet")

        # Arrange
        vehicle = Vehicle(
            id="V-123",
            plate="TST-999",  # Fixed: Valid plate format
            model="Test Model",
            current_mileage=12345,
        )
        mock_repository.get_by_id.return_value = vehicle
        use_case = GetVehicleUseCase(vehicle_repository=mock_repository)

        # Act
        result = use_case.execute("V-123")

        # Assert - All properties should be present
        assert hasattr(result, "id"), "DTO should have id"
        assert hasattr(result, "plate"), "DTO should have plate"
        assert hasattr(result, "model"), "DTO should have model"
        assert hasattr(result, "current_mileage"), "DTO should have current_mileage"

        assert result.id == "V-123"
        assert result.plate == "TST-999"
        assert result.model == "Test Model"
        assert result.current_mileage == 12345
