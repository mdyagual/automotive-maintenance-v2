"""Tests for GetVehiclesByStatusUseCase - Application layer."""

from unittest.mock import Mock

import pytest

from src.domain.entities.vehicle import Vehicle
from src.domain.entities.vehicle_status import VehicleStatus


class TestGetVehiclesByStatusUseCase:
    """
    Tests for GetVehiclesByStatusUseCase (currently doesn't exist - tests will FAIL).

    These tests define the expected behavior for HU-005 Escenario 2:
    1. Use case should accept status parameter
    2. Use case should return list of VehicleDTO (not domain entities)
    3. Use case should delegate to repository.get_by_status()
    4. Use case should handle empty results
    5. Use case should filter correctly for all status values
    """

    @pytest.fixture
    def mock_repository(self):
        """Create a mock vehicle repository."""
        return Mock()

    @pytest.fixture
    def sample_active_vehicles(self):
        """Create sample vehicles with ACTIVE status."""
        return [
            Vehicle(
                id="V-001",
                plate="ABC-001",
                model="Toyota Corolla",
                current_mileage=50000,
                status=VehicleStatus.ACTIVE,
            ),
            Vehicle(
                id="V-002",
                plate="ABC-002",
                model="Honda Civic",
                current_mileage=60000,
                status=VehicleStatus.ACTIVE,
            ),
        ]

    @pytest.fixture
    def sample_mixed_vehicles(self):
        """Create sample vehicles with different statuses."""
        return [
            Vehicle(
                id="V-001",
                plate="ABC-001",
                model="Toyota Corolla",
                current_mileage=50000,
                status=VehicleStatus.ACTIVE,
            ),
            Vehicle(
                id="V-002",
                plate="ABC-002",
                model="Honda Civic",
                current_mileage=60000,
                status=VehicleStatus.ACTIVE,
            ),
            Vehicle(
                id="V-003",
                plate="ABC-003",
                model="Ford Focus",
                current_mileage=70000,
                status=VehicleStatus.IN_MAINTENANCE,
            ),
            Vehicle(
                id="V-004",
                plate="ABC-004",
                model="Mazda 3",
                current_mileage=80000,
                status=VehicleStatus.INACTIVE,
            ),
            Vehicle(
                id="V-005",
                plate="ABC-005",
                model="Chevrolet Cruze",
                current_mileage=150000,
                status=VehicleStatus.RETIRED,
            ),
        ]

    def test_get_vehicles_by_status_use_case_exists(self):
        """
        Test that GetVehiclesByStatusUseCase class exists.

        EXPECTED TO FAIL: GetVehiclesByStatusUseCase doesn't exist yet.
        """
        try:
            from src.application.use_cases.get_vehicles_by_status_use_case import (
                GetVehiclesByStatusUseCase,
            )

            assert GetVehiclesByStatusUseCase is not None
        except ImportError:
            pytest.fail("GetVehiclesByStatusUseCase not implemented yet")

    def test_execute_returns_list_of_vehicle_dtos_not_entities(self, mock_repository, sample_active_vehicles):
        """
        Test that execute() returns list of VehicleDTO, not domain entities.

        EXPECTED TO FAIL: GetVehiclesByStatusUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - Use case should return list of VehicleDTO
        - Domain entities should NOT be returned
        """
        try:
            from src.application.dtos.vehicle_dtos import VehicleDTO
            from src.application.use_cases.get_vehicles_by_status_use_case import (
                GetVehiclesByStatusUseCase,
            )
        except ImportError:
            pytest.skip("GetVehiclesByStatusUseCase or VehicleDTO not implemented yet")

        # Arrange
        mock_repository.get_by_status.return_value = sample_active_vehicles
        use_case = GetVehiclesByStatusUseCase(vehicle_repository=mock_repository)

        # Act
        result = use_case.execute(VehicleStatus.ACTIVE)

        # Assert
        assert isinstance(result, list), "Use case should return a list"
        assert len(result) == 2, "Should return 2 vehicles"

        for vehicle_dto in result:
            assert isinstance(vehicle_dto, VehicleDTO), "Each item should be VehicleDTO"
            assert not isinstance(vehicle_dto, Vehicle), "Should NOT return domain entities"

    def test_execute_calls_repository_get_by_status(self, mock_repository, sample_active_vehicles):
        """
        Test that execute() delegates to repository.get_by_status().

        EXPECTED TO FAIL: GetVehiclesByStatusUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - Use case should call repository.get_by_status(status)
        - Use case should pass the correct status parameter
        """
        try:
            from src.application.use_cases.get_vehicles_by_status_use_case import (
                GetVehiclesByStatusUseCase,
            )
        except ImportError:
            pytest.skip("GetVehiclesByStatusUseCase not implemented yet")

        # Arrange
        mock_repository.get_by_status.return_value = sample_active_vehicles
        use_case = GetVehiclesByStatusUseCase(vehicle_repository=mock_repository)

        # Act
        use_case.execute(VehicleStatus.ACTIVE)

        # Assert
        mock_repository.get_by_status.assert_called_once_with(VehicleStatus.ACTIVE)

    def test_execute_returns_empty_list_when_no_vehicles_match(self, mock_repository):
        """
        Test that execute() returns empty list when no vehicles have the status.

        EXPECTED TO FAIL: GetVehiclesByStatusUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - Should return empty list, not None
        - Should not raise exception
        """
        try:
            from src.application.use_cases.get_vehicles_by_status_use_case import (
                GetVehiclesByStatusUseCase,
            )
        except ImportError:
            pytest.skip("GetVehiclesByStatusUseCase not implemented yet")

        # Arrange
        mock_repository.get_by_status.return_value = []
        use_case = GetVehiclesByStatusUseCase(vehicle_repository=mock_repository)

        # Act
        result = use_case.execute(VehicleStatus.RETIRED)

        # Assert
        assert result == [], "Should return empty list"
        assert isinstance(result, list), "Should return list, not None"

    def test_execute_filters_active_vehicles_correctly(self, mock_repository, sample_active_vehicles):
        """
        Test filtering vehicles with ACTIVE status.

        EXPECTED TO FAIL: GetVehiclesByStatusUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - Should return only vehicles with ACTIVE status
        - Should return correct vehicle data in DTOs
        """
        try:
            from src.application.use_cases.get_vehicles_by_status_use_case import (
                GetVehiclesByStatusUseCase,
            )
        except ImportError:
            pytest.skip("GetVehiclesByStatusUseCase not implemented yet")

        # Arrange
        mock_repository.get_by_status.return_value = sample_active_vehicles
        use_case = GetVehiclesByStatusUseCase(vehicle_repository=mock_repository)

        # Act
        result = use_case.execute(VehicleStatus.ACTIVE)

        # Assert
        assert len(result) == 2, "Should return 2 active vehicles"
        assert result[0].id == "V-001"
        assert result[0].status == "active"
        assert result[1].id == "V-002"
        assert result[1].status == "active"

    def test_execute_with_different_status_values(self, mock_repository):
        """
        Test that execute() works correctly with all status values.

        EXPECTED TO FAIL: GetVehiclesByStatusUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - Should work with ACTIVE, INACTIVE, IN_MAINTENANCE, RETIRED
        - Should call repository with correct status each time
        """
        try:
            from src.application.use_cases.get_vehicles_by_status_use_case import (
                GetVehiclesByStatusUseCase,
            )
        except ImportError:
            pytest.skip("GetVehiclesByStatusUseCase not implemented yet")

        # Arrange
        mock_repository.get_by_status.return_value = []
        use_case = GetVehiclesByStatusUseCase(vehicle_repository=mock_repository)

        # Act & Assert - Test all status values
        use_case.execute(VehicleStatus.ACTIVE)
        mock_repository.get_by_status.assert_called_with(VehicleStatus.ACTIVE)

        use_case.execute(VehicleStatus.INACTIVE)
        mock_repository.get_by_status.assert_called_with(VehicleStatus.INACTIVE)

        use_case.execute(VehicleStatus.IN_MAINTENANCE)
        mock_repository.get_by_status.assert_called_with(VehicleStatus.IN_MAINTENANCE)

        use_case.execute(VehicleStatus.RETIRED)
        mock_repository.get_by_status.assert_called_with(VehicleStatus.RETIRED)

    def test_use_case_accepts_repository_in_constructor(self, mock_repository):
        """
        Test that GetVehiclesByStatusUseCase accepts repository in constructor.

        EXPECTED TO FAIL: GetVehiclesByStatusUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - Constructor should accept vehicle_repository parameter
        - Should follow dependency injection pattern
        """
        try:
            from src.application.use_cases.get_vehicles_by_status_use_case import (
                GetVehiclesByStatusUseCase,
            )
        except ImportError:
            pytest.skip("GetVehiclesByStatusUseCase not implemented yet")

        # Act
        use_case = GetVehiclesByStatusUseCase(vehicle_repository=mock_repository)

        # Assert
        assert use_case is not None
        assert hasattr(use_case, "execute"), "Use case should have execute method"

    def test_dto_contains_all_vehicle_fields_including_status(self, mock_repository, sample_active_vehicles):
        """
        Test that returned DTOs contain all vehicle fields including status.

        EXPECTED TO FAIL: GetVehiclesByStatusUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - DTOs should include: id, plate, model, current_mileage, status
        - Status should be string representation
        """
        try:
            from src.application.use_cases.get_vehicles_by_status_use_case import (
                GetVehiclesByStatusUseCase,
            )
        except ImportError:
            pytest.skip("GetVehiclesByStatusUseCase not implemented yet")

        # Arrange
        mock_repository.get_by_status.return_value = sample_active_vehicles
        use_case = GetVehiclesByStatusUseCase(vehicle_repository=mock_repository)

        # Act
        result = use_case.execute(VehicleStatus.ACTIVE)

        # Assert
        first_dto = result[0]
        assert hasattr(first_dto, "id"), "DTO should have id"
        assert hasattr(first_dto, "plate"), "DTO should have plate"
        assert hasattr(first_dto, "model"), "DTO should have model"
        assert hasattr(first_dto, "current_mileage"), "DTO should have current_mileage"
        assert hasattr(first_dto, "status"), "DTO should have status"
        assert first_dto.status == "active", "Status should be string representation"

    def test_use_case_does_not_modify_domain_entities(self, mock_repository, sample_active_vehicles):
        """
        Test that use case doesn't modify domain entities.

        EXPECTED TO FAIL: GetVehiclesByStatusUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - Use case should only read from entities
        - Entity state should remain unchanged
        """
        try:
            from src.application.use_cases.get_vehicles_by_status_use_case import (
                GetVehiclesByStatusUseCase,
            )
        except ImportError:
            pytest.skip("GetVehiclesByStatusUseCase not implemented yet")

        # Arrange
        original_count = len(sample_active_vehicles)
        original_ids = [v.id for v in sample_active_vehicles]
        original_statuses = [v.status for v in sample_active_vehicles]

        mock_repository.get_by_status.return_value = sample_active_vehicles
        use_case = GetVehiclesByStatusUseCase(vehicle_repository=mock_repository)

        # Act
        use_case.execute(VehicleStatus.ACTIVE)

        # Assert
        assert len(sample_active_vehicles) == original_count, "Vehicle list should not be modified"
        assert [v.id for v in sample_active_vehicles] == original_ids, "Vehicle IDs should not change"
        assert [v.status for v in sample_active_vehicles] == original_statuses, "Vehicle statuses should not change"

    def test_execute_with_gherkin_scenario_data(self, mock_repository):
        """
        Test the exact Gherkin scenario from HU-005 Escenario 2.

        Given: 5 vehicles in the system with different statuses
        When: I request vehicles with status='active'
        Then: System should return 2 vehicles
        And: Both vehicles should have status 'active'

        EXPECTED TO FAIL: GetVehiclesByStatusUseCase doesn't exist yet.
        """
        try:
            from src.application.use_cases.get_vehicles_by_status_use_case import (
                GetVehiclesByStatusUseCase,
            )
        except ImportError:
            pytest.skip("GetVehiclesByStatusUseCase not implemented yet")

        # Arrange - Create the exact scenario from Gherkin
        active_vehicles = [
            Vehicle(
                id="V-001",
                plate="ABC-001",
                model="Toyota Corolla",
                current_mileage=50000,
                status=VehicleStatus.ACTIVE,
            ),
            Vehicle(
                id="V-002",
                plate="ABC-002",
                model="Honda Civic",
                current_mileage=60000,
                status=VehicleStatus.ACTIVE,
            ),
        ]

        mock_repository.get_by_status.return_value = active_vehicles
        use_case = GetVehiclesByStatusUseCase(vehicle_repository=mock_repository)

        # Act
        result = use_case.execute(VehicleStatus.ACTIVE)

        # Assert
        assert len(result) == 2, "Sistema debe devolver 2 vehículos"
        assert all(v.status == "active" for v in result), "Ambos vehículos deben tener estado 'active'"
        assert result[0].id == "V-001"
        assert result[1].id == "V-002"
