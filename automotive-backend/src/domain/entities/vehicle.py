"""Vehicle entity - Domain model."""

from src.domain.exceptions.invalid_mileage_exception import InvalidMileageException
from src.domain.ports.observer import Observer


class Vehicle:
    """Vehicle entity representing a fleet vehicle."""

    MAX_MILEAGE = 1_000_000
    MAX_MILEAGE_INCREMENT = 50_000
    MAINTENANCE_INTERVAL = 10_000

    def __init__(self, id: str, plate: str, model: str, current_mileage: int) -> None:
        """
        Initialize a Vehicle instance.

        Args:
            id: Unique identifier for the vehicle
            plate: License plate number
            model: Vehicle model name
            current_mileage: Current mileage in kilometers
        """
        self.id = id
        self.plate = plate
        self.model = model
        self.current_mileage = current_mileage
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        """Attach an observer to receive notifications."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Detach an observer from notifications."""
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify_observers(self) -> None:
        """Notify all observers about mileage update."""
        for observer in self._observers:
            observer.update(self.id, self.current_mileage)

    def _crosses_maintenance_threshold(self, old_mileage: int, new_mileage: int) -> bool:
        """
        Check if update crosses a maintenance threshold.

        Args:
            old_mileage: Previous mileage value
            new_mileage: New mileage value

        Returns:
            True if crosses a 10,000 km threshold, False otherwise
        """
        old_threshold = (old_mileage // self.MAINTENANCE_INTERVAL) * self.MAINTENANCE_INTERVAL
        new_threshold = (new_mileage // self.MAINTENANCE_INTERVAL) * self.MAINTENANCE_INTERVAL
        return new_threshold > old_threshold

    def update_mileage(self, new_mileage: int) -> None:
        """
        Update vehicle mileage.

        Args:
            new_mileage: New mileage value

        Raises:
            InvalidMileageException: If new mileage is not greater than current
        """
        if new_mileage <= self.current_mileage:
            raise InvalidMileageException(
                f"El kilometraje {new_mileage} debe ser mayor al actual {self.current_mileage}"
            )

        if new_mileage > self.MAX_MILEAGE:
            raise InvalidMileageException(
                f"El kilometraje {new_mileage} excede el límite máximo de {self.MAX_MILEAGE:,} km"
            )

        increment = new_mileage - self.current_mileage
        if increment > self.MAX_MILEAGE_INCREMENT:
            raise InvalidMileageException(
                f"El incremento de {increment:,} km excede el máximo permitido de "
                f"{self.MAX_MILEAGE_INCREMENT:,} km"
            )

        old_mileage = self.current_mileage
        self.current_mileage = new_mileage

        # Notify observers if maintenance threshold crossed
        if self._crosses_maintenance_threshold(old_mileage, new_mileage):
            self._notify_observers()
