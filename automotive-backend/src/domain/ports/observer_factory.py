"""Observer Factory Port - Domain layer abstraction."""

from abc import ABC, abstractmethod

from src.domain.ports.observer import Observer


class ObserverFactory(ABC):
    """Factory for creating observers (domain port)."""

    @abstractmethod
    def create_maintenance_observer(self, vehicle_id: str, initial_mileage: int) -> Observer:
        """
        Create a maintenance alert observer.

        Args:
            vehicle_id: ID of the vehicle to observe
            initial_mileage: Initial mileage of the vehicle

        Returns:
            Observer instance configured for maintenance alerts
        """
        pass
