"""Observer pattern port for automatic maintenance alerts."""
from abc import ABC, abstractmethod


class Observer(ABC):
    """Observer interface following DIP - depends on abstraction."""

    @abstractmethod
    def update(self, vehicle_id: str, mileage: int) -> None:
        """
        Notify observer about vehicle mileage update.

        Args:
            vehicle_id: Unique identifier of the vehicle
            mileage: New mileage value
        """
        pass
