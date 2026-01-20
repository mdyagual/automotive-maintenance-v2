"""Tests for MaintenanceAlert entity following TDD approach."""
from datetime import datetime

from src.domain.entities.maintenance_alert import AlertType, MaintenanceAlert


class TestMaintenanceAlertCreation:
    """Test cases for MaintenanceAlert creation."""

    def test_create_basic_maintenance_alert(self) -> None:
        """
        Given: Valid maintenance alert data
        When: Creating a MaintenanceAlert for basic maintenance
        Then: Alert should be created with correct attributes
        """
        # Arrange
        alert_id = "A-001"
        vehicle_id = "V-123"
        alert_type = AlertType.BASIC_MAINTENANCE
        mileage = 10000
        timestamp = datetime(2026, 1, 6, 10, 0, 0)

        # Act
        alert = MaintenanceAlert(
            id=alert_id,
            vehicle_id=vehicle_id,
            alert_type=alert_type,
            mileage=mileage,
            timestamp=timestamp
        )

        # Assert
        assert alert.id == alert_id
        assert alert.vehicle_id == vehicle_id
        assert alert.alert_type == AlertType.BASIC_MAINTENANCE
        assert alert.mileage == mileage
        assert alert.timestamp == timestamp
