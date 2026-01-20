"""Major Maintenance Strategy - every 50,000 km."""
from src.domain.entities.maintenance_alert import AlertType
from src.domain.strategies.maintenance_strategy import MaintenanceStrategy


class MajorMaintenanceStrategy(MaintenanceStrategy):
    """Strategy for major maintenance every 50,000 km."""

    INTERVAL = 50_000

    def should_generate_alert(self, old_mileage: int, new_mileage: int) -> bool:
        """
        Check if vehicle crosses a 50,000 km threshold.

        Args:
            old_mileage: Previous mileage value
            new_mileage: New mileage value

        Returns:
            True if crosses 50,000 km threshold, False otherwise
        """
        old_threshold = self._calculate_threshold(old_mileage)
        new_threshold = self._calculate_threshold(new_mileage)
        return new_threshold > old_threshold

    def get_alert_type(self) -> AlertType:
        """Return MAJOR_MAINTENANCE alert type."""
        return AlertType.MAJOR_MAINTENANCE
