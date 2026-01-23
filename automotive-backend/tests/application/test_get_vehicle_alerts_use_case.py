"""
Unit tests for GetVehicleAlertsUseCase.

These tests will FAIL until GetVehicleAlertsUseCase is implemented.
They define the expected behavior of the missing use case.
"""

from datetime import datetime
from unittest.mock import Mock

import pytest

from src.domain.entities.maintenance_alert import AlertType, MaintenanceAlert


class TestGetVehicleAlertsUseCase:
    """
    Tests for GetVehicleAlertsUseCase (currently doesn't exist - tests will FAIL).

    These tests define the expected behavior:
    1. Use case should accept vehicle_id as parameter
    2. Use case should return list[AlertDTO] (not domain entities)
    3. Use case should filter alerts by vehicle_id (business logic)
    4. Use case should delegate to repository
    """

    @pytest.fixture
    def mock_repository(self):
        """Create a mock alert repository."""
        return Mock()

    @pytest.fixture
    def sample_alerts(self):
        """Create sample alert entities for multiple vehicles."""
        return [
            MaintenanceAlert(id="A-V-001-10000-BASIC", vehicle_id="V-001", alert_type=AlertType.BASIC_MAINTENANCE, mileage=10000, timestamp=datetime(2024, 1, 1, 10, 0, 0)),
            MaintenanceAlert(
                id="A-V-002-10000-BASIC",
                vehicle_id="V-002",  # Different vehicle
                alert_type=AlertType.BASIC_MAINTENANCE,
                mileage=10000,
                timestamp=datetime(2024, 1, 2, 10, 0, 0),
            ),
            MaintenanceAlert(id="A-V-001-30000-MAJOR", vehicle_id="V-001", alert_type=AlertType.MAJOR_MAINTENANCE, mileage=30000, timestamp=datetime(2024, 6, 1, 10, 0, 0)),
            MaintenanceAlert(id="A-V-001-50000-CRITICAL", vehicle_id="V-001", alert_type=AlertType.CRITICAL_THRESHOLD, mileage=50000, timestamp=datetime(2024, 12, 1, 10, 0, 0)),
        ]

    def test_get_vehicle_alerts_use_case_exists(self):
        """
        Test that GetVehicleAlertsUseCase class exists.

        EXPECTED TO FAIL: GetVehicleAlertsUseCase doesn't exist yet.
        """
        try:
            from src.application.use_cases.get_vehicle_alerts_use_case import GetVehicleAlertsUseCase

            assert GetVehicleAlertsUseCase is not None
        except ImportError:
            pytest.fail("GetVehicleAlertsUseCase does not exist. Please create it at src/application/use_cases/get_vehicle_alerts_use_case.py")

    def test_execute_returns_list_of_alert_dtos(self, mock_repository, sample_alerts):
        """
        Test that execute() returns list[AlertDTO], not domain entities.

        EXPECTED TO FAIL: GetVehicleAlertsUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - Use case should return list of AlertDTO
        - Domain entities should NOT be returned
        """
        try:
            from src.application.dtos.alert_dtos import AlertDTO
            from src.application.use_cases.get_vehicle_alerts_use_case import GetVehicleAlertsUseCase
        except ImportError:
            pytest.skip("GetVehicleAlertsUseCase or AlertDTO not implemented yet")

        # Arrange
        mock_repository.get_all.return_value = sample_alerts
        use_case = GetVehicleAlertsUseCase(alert_repository=mock_repository)

        # Act
        result = use_case.execute("V-001")

        # Assert
        assert isinstance(result, list), "Use case should return a list"
        assert len(result) > 0, "Should return alerts for V-001"

        for alert_dto in result:
            assert isinstance(alert_dto, AlertDTO), "Each item should be AlertDTO"
            assert not isinstance(alert_dto, MaintenanceAlert), "Should NOT return domain entities"

    def test_execute_filters_alerts_by_vehicle_id(self, mock_repository, sample_alerts):
        """
        Test that execute() filters alerts by vehicle_id (business logic).

        EXPECTED TO FAIL: GetVehicleAlertsUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - Use case should filter alerts for the specified vehicle
        - Should only return alerts matching vehicle_id
        - Filtering is business logic that belongs in application layer
        """
        try:
            from src.application.use_cases.get_vehicle_alerts_use_case import GetVehicleAlertsUseCase
        except ImportError:
            pytest.skip("GetVehicleAlertsUseCase not implemented yet")

        # Arrange
        mock_repository.get_all.return_value = sample_alerts
        use_case = GetVehicleAlertsUseCase(alert_repository=mock_repository)

        # Act
        result = use_case.execute("V-001")

        # Assert
        assert len(result) == 3, "Should return 3 alerts for V-001"

        # All returned alerts should be for V-001
        for alert_dto in result:
            assert alert_dto.vehicle_id == "V-001", "All alerts should be for V-001"

    def test_execute_returns_empty_list_when_no_alerts(self, mock_repository):
        """
        Test that execute() returns empty list when vehicle has no alerts.

        EXPECTED TO FAIL: GetVehicleAlertsUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - Should return empty list, not None
        - Should not raise exception
        """
        try:
            from src.application.use_cases.get_vehicle_alerts_use_case import GetVehicleAlertsUseCase
        except ImportError:
            pytest.skip("GetVehicleAlertsUseCase not implemented yet")

        # Arrange
        mock_repository.get_all.return_value = []
        use_case = GetVehicleAlertsUseCase(alert_repository=mock_repository)

        # Act
        result = use_case.execute("V-999")

        # Assert
        assert result == [], "Should return empty list"
        assert isinstance(result, list), "Should return list, not None"

    def test_execute_calls_repository_get_all(self, mock_repository, sample_alerts):
        """
        Test that execute() delegates to repository.get_all().

        EXPECTED TO FAIL: GetVehicleAlertsUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - Use case should call repository.get_all()
        - Should call it exactly once
        """
        try:
            from src.application.use_cases.get_vehicle_alerts_use_case import GetVehicleAlertsUseCase
        except ImportError:
            pytest.skip("GetVehicleAlertsUseCase not implemented yet")

        # Arrange
        mock_repository.get_all.return_value = sample_alerts
        use_case = GetVehicleAlertsUseCase(alert_repository=mock_repository)

        # Act
        use_case.execute("V-001")

        # Assert
        mock_repository.get_all.assert_called_once()

    def test_execute_with_different_vehicle_ids(self, mock_repository, sample_alerts):
        """
        Test that execute() correctly filters for different vehicle IDs.

        EXPECTED TO FAIL: GetVehicleAlertsUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - Should return correct alerts for each vehicle
        - Filtering should work for any vehicle_id
        """
        try:
            from src.application.use_cases.get_vehicle_alerts_use_case import GetVehicleAlertsUseCase
        except ImportError:
            pytest.skip("GetVehicleAlertsUseCase not implemented yet")

        # Arrange
        mock_repository.get_all.return_value = sample_alerts
        use_case = GetVehicleAlertsUseCase(alert_repository=mock_repository)

        # Act
        result_v001 = use_case.execute("V-001")
        result_v002 = use_case.execute("V-002")

        # Assert
        assert len(result_v001) == 3, "V-001 should have 3 alerts"
        assert len(result_v002) == 1, "V-002 should have 1 alert"

        assert all(a.vehicle_id == "V-001" for a in result_v001)
        assert all(a.vehicle_id == "V-002" for a in result_v002)

    def test_use_case_accepts_repository_in_constructor(self, mock_repository):
        """
        Test that GetVehicleAlertsUseCase accepts repository in constructor.

        EXPECTED TO FAIL: GetVehicleAlertsUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - Constructor should accept alert_repository parameter
        - Should follow dependency injection pattern
        """
        try:
            from src.application.use_cases.get_vehicle_alerts_use_case import GetVehicleAlertsUseCase
        except ImportError:
            pytest.skip("GetVehicleAlertsUseCase not implemented yet")

        # Act
        use_case = GetVehicleAlertsUseCase(alert_repository=mock_repository)

        # Assert
        assert use_case is not None
        assert hasattr(use_case, "execute"), "Use case should have execute method"

    def test_alert_dto_is_immutable(self, mock_repository, sample_alerts):
        """
        Test that returned AlertDTOs are immutable (frozen dataclass).

        EXPECTED TO FAIL: GetVehicleAlertsUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - AlertDTO should be immutable
        - Attempting to modify should raise exception
        """
        try:
            from src.application.use_cases.get_vehicle_alerts_use_case import GetVehicleAlertsUseCase
        except ImportError:
            pytest.skip("GetVehicleAlertsUseCase not implemented yet")

        # Arrange
        mock_repository.get_all.return_value = sample_alerts
        use_case = GetVehicleAlertsUseCase(alert_repository=mock_repository)

        # Act
        result = use_case.execute("V-001")

        # Assert - Try to modify DTO (should fail)
        with pytest.raises((AttributeError, Exception)):
            result[0].mileage = 999999

    def test_use_case_maps_all_alert_properties_to_dto(self, mock_repository):
        """
        Test that all alert properties are mapped to DTO.

        EXPECTED TO FAIL: GetVehicleAlertsUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - All alert properties should be in DTO
        - No data should be lost in mapping
        """
        try:
            from src.application.use_cases.get_vehicle_alerts_use_case import GetVehicleAlertsUseCase
        except ImportError:
            pytest.skip("GetVehicleAlertsUseCase not implemented yet")

        # Arrange
        alert = MaintenanceAlert(id="A-TEST-123", vehicle_id="V-TEST", alert_type=AlertType.BASIC_MAINTENANCE, mileage=15000, timestamp=datetime(2024, 3, 15, 14, 30, 0))
        mock_repository.get_all.return_value = [alert]
        use_case = GetVehicleAlertsUseCase(alert_repository=mock_repository)

        # Act
        result = use_case.execute("V-TEST")

        # Assert - All properties should be present
        assert len(result) == 1
        alert_dto = result[0]

        assert hasattr(alert_dto, "id"), "DTO should have id"
        assert hasattr(alert_dto, "vehicle_id"), "DTO should have vehicle_id"
        assert hasattr(alert_dto, "alert_type"), "DTO should have alert_type"
        assert hasattr(alert_dto, "mileage"), "DTO should have mileage"
        assert hasattr(alert_dto, "timestamp"), "DTO should have timestamp"

        assert alert_dto.id == "A-TEST-123"
        assert alert_dto.vehicle_id == "V-TEST"
        assert alert_dto.alert_type == "BASIC_MAINTENANCE"
        assert alert_dto.mileage == 15000
        assert alert_dto.timestamp == datetime(2024, 3, 15, 14, 30, 0)

    def test_alert_type_is_converted_to_string_in_dto(self, mock_repository):
        """
        Test that AlertType enum is converted to string in DTO.

        EXPECTED TO FAIL: GetVehicleAlertsUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - alert_type should be string in DTO, not enum
        - Should use enum.value for conversion
        """
        try:
            from src.application.use_cases.get_vehicle_alerts_use_case import GetVehicleAlertsUseCase
        except ImportError:
            pytest.skip("GetVehicleAlertsUseCase not implemented yet")

        # Arrange
        alerts = [
            MaintenanceAlert(id="A-1", vehicle_id="V-001", alert_type=AlertType.BASIC_MAINTENANCE, mileage=10000, timestamp=datetime(2024, 1, 1)),
            MaintenanceAlert(id="A-2", vehicle_id="V-001", alert_type=AlertType.MAJOR_MAINTENANCE, mileage=30000, timestamp=datetime(2024, 6, 1)),
            MaintenanceAlert(id="A-3", vehicle_id="V-001", alert_type=AlertType.CRITICAL_THRESHOLD, mileage=50000, timestamp=datetime(2024, 12, 1)),
        ]
        mock_repository.get_all.return_value = alerts
        use_case = GetVehicleAlertsUseCase(alert_repository=mock_repository)

        # Act
        result = use_case.execute("V-001")

        # Assert
        assert result[0].alert_type == "BASIC_MAINTENANCE"
        assert result[1].alert_type == "MAJOR_MAINTENANCE"
        assert result[2].alert_type == "CRITICAL_THRESHOLD"

        # Should be strings, not enums
        assert isinstance(result[0].alert_type, str)
        assert isinstance(result[1].alert_type, str)
        assert isinstance(result[2].alert_type, str)

    def test_use_case_does_not_modify_domain_entities(self, mock_repository, sample_alerts):
        """
        Test that use case doesn't modify domain entities.

        EXPECTED TO FAIL: GetVehicleAlertsUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - Use case should only read from entities
        - Entity state should remain unchanged
        """
        try:
            from src.application.use_cases.get_vehicle_alerts_use_case import GetVehicleAlertsUseCase
        except ImportError:
            pytest.skip("GetVehicleAlertsUseCase not implemented yet")

        # Arrange
        original_count = len(sample_alerts)
        original_ids = [alert.id for alert in sample_alerts]

        mock_repository.get_all.return_value = sample_alerts
        use_case = GetVehicleAlertsUseCase(alert_repository=mock_repository)

        # Act
        use_case.execute("V-001")

        # Assert
        assert len(sample_alerts) == original_count, "Alert list should not be modified"
        assert [alert.id for alert in sample_alerts] == original_ids, "Alert IDs should not change"

    def test_execute_returns_alerts_in_original_order(self, mock_repository):
        """
        Test that execute() preserves the order of alerts from repository.

        EXPECTED TO FAIL: GetVehicleAlertsUseCase doesn't exist yet.

        CORRECT BEHAVIOR:
        - Should maintain the order from repository
        - Should not sort or reorder alerts
        """
        try:
            from src.application.use_cases.get_vehicle_alerts_use_case import GetVehicleAlertsUseCase
        except ImportError:
            pytest.skip("GetVehicleAlertsUseCase not implemented yet")

        # Arrange - Alerts in specific order
        alerts = [
            MaintenanceAlert(id="A-3", vehicle_id="V-001", alert_type=AlertType.CRITICAL_THRESHOLD, mileage=50000, timestamp=datetime(2024, 12, 1)),
            MaintenanceAlert(id="A-1", vehicle_id="V-001", alert_type=AlertType.BASIC_MAINTENANCE, mileage=10000, timestamp=datetime(2024, 1, 1)),
            MaintenanceAlert(id="A-2", vehicle_id="V-001", alert_type=AlertType.MAJOR_MAINTENANCE, mileage=30000, timestamp=datetime(2024, 6, 1)),
        ]
        mock_repository.get_all.return_value = alerts
        use_case = GetVehicleAlertsUseCase(alert_repository=mock_repository)

        # Act
        result = use_case.execute("V-001")

        # Assert - Order should be preserved
        assert result[0].id == "A-3"
        assert result[1].id == "A-1"
        assert result[2].id == "A-2"
