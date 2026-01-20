"""Critical Threshold Strategy - alert at 100,000 km (RN-007)."""
from src.domain.entities.maintenance_alert import AlertType
from src.domain.strategies.maintenance_strategy import MaintenanceStrategy


class CriticalThresholdStrategy(MaintenanceStrategy):
    """
    Strategy for critical threshold at 100,000 km.

    Unlike periodic maintenance strategies, this alert is triggered
    only once when the vehicle crosses the critical threshold.
    """

    CRITICAL_THRESHOLD = 100_000
    INTERVAL = CRITICAL_THRESHOLD  # Required by base class

    def should_generate_alert(self, old_mileage: int, new_mileage: int) -> bool:
        """
        Check if vehicle crosses the critical 100,000 km threshold.

        This alert is generated only once when crossing the threshold,
        not on subsequent mileage updates beyond 100,000 km.

        Args:
            old_mileage: Previous mileage value
            new_mileage: New mileage value

        Returns:
            True if crosses 100,000 km threshold for the first time, False otherwise
        """
        return old_mileage < self.CRITICAL_THRESHOLD <= new_mileage

    def get_alert_type(self) -> AlertType:
        """Return CRITICAL_THRESHOLD alert type."""
        return AlertType.CRITICAL_THRESHOLD
