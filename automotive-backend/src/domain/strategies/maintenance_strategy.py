"""Maintenance Strategy port - following DIP."""
from abc import ABC, abstractmethod

from src.domain.entities.maintenance_alert import AlertType


class MaintenanceStrategy(ABC):
    """Interface for maintenance strategies following Strategy Pattern."""

    INTERVAL: int  # Must be defined by subclasses

    def _calculate_threshold(self, mileage: int) -> int:
        """
        Calculate the maintenance threshold for given mileage.

        Args:
            mileage: Current mileage value

        Returns:
            The last crossed threshold (multiple of INTERVAL)
        """
        return (mileage // self.INTERVAL) * self.INTERVAL

    @abstractmethod
    def should_generate_alert(self, old_mileage: int, new_mileage: int) -> bool:
        """
        Determine if maintenance alert should be generated.

        Args:
            old_mileage: Previous mileage value
            new_mileage: New mileage value

        Returns:
            True if alert should be generated, False otherwise
        """
        pass

    @abstractmethod
    def get_alert_type(self) -> AlertType:
        """
        Get the type of alert this strategy generates.

        Returns:
            AlertType enum value
        """
        pass
