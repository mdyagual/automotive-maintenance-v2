"""Alert Repository port - following DIP."""
from abc import ABC, abstractmethod

from src.domain.entities.maintenance_alert import MaintenanceAlert


class AlertRepository(ABC):
    """Interface for alert repository following DIP."""

    @abstractmethod
    def save(self, alert: MaintenanceAlert) -> None:
        """
        Save alert to repository.

        Args:
            alert: MaintenanceAlert instance to save
        """
        pass

    @abstractmethod
    def get_by_vehicle_id(self, vehicle_id: str) -> list[MaintenanceAlert]:
        """
        Get all alerts for a specific vehicle.

        Args:
            vehicle_id: Unique identifier of the vehicle

        Returns:
            List of MaintenanceAlert instances for the vehicle
        """
        pass
