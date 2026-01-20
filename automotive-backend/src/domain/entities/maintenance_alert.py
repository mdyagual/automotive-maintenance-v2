"""MaintenanceAlert entity for tracking vehicle maintenance alerts."""
from datetime import datetime
from enum import Enum


class AlertType(Enum):
    """Types of maintenance alerts."""

    BASIC_MAINTENANCE = "basic_maintenance"  # Every 10,000 km
    MAJOR_MAINTENANCE = "major_maintenance"  # Every 50,000 km
    CRITICAL_THRESHOLD = "critical_threshold"  # At 100,000 km


class MaintenanceAlert:
    """Alert generated when vehicle reaches maintenance threshold."""

    def __init__(
        self,
        id: str,
        vehicle_id: str,
        alert_type: AlertType,
        mileage: int,
        timestamp: datetime
    ) -> None:
        """
        Initialize a MaintenanceAlert instance.

        Args:
            id: Unique identifier for the alert
            vehicle_id: Identifier of the vehicle triggering the alert
            alert_type: Type of maintenance alert
            mileage: Mileage at which alert was triggered
            timestamp: When the alert was generated
        """
        self.id = id
        self.vehicle_id = vehicle_id
        self.alert_type = alert_type
        self.mileage = mileage
        self.timestamp = timestamp
