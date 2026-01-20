"""Vehicle Repository port - following DIP."""
from abc import ABC, abstractmethod

from src.domain.entities.vehicle import Vehicle


class VehicleRepository(ABC):
    """Interface for vehicle repository following DIP."""

    @abstractmethod
    def get_by_id(self, vehicle_id: str) -> Vehicle:
        """
        Get vehicle by ID.

        Args:
            vehicle_id: Unique identifier of the vehicle

        Returns:
            Vehicle instance

        Raises:
            VehicleNotFoundException: If vehicle not found
        """
        pass

    @abstractmethod
    def save(self, vehicle: Vehicle) -> None:
        """
        Save vehicle to repository.

        Args:
            vehicle: Vehicle instance to save
        """
        pass

    @abstractmethod
    def get_all(self) -> list[Vehicle]:
        """
        Get all vehicles from repository.

        Returns:
            List of all Vehicle instances
        """
        pass

    @abstractmethod
    def delete(self, vehicle_id: str) -> None:
        """
        Delete vehicle from repository by ID.

        Args:
            vehicle_id: Unique identifier of the vehicle to delete

        Raises:
            VehicleNotFoundException: If vehicle not found
        """
        pass
