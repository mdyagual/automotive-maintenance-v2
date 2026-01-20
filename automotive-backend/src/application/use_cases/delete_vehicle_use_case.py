"""Use case for deleting a vehicle from the system."""

from src.domain.ports.vehicle_repository import VehicleRepository


class DeleteVehicleUseCase:
    """Use case for deleting a vehicle and its associated alerts."""

    def __init__(self, vehicle_repository: VehicleRepository):
        """
        Initialize use case with repository dependency.

        Args:
            vehicle_repository: Repository for vehicle persistence
        """
        self._vehicle_repository = vehicle_repository

    def execute(self, vehicle_id: str) -> None:
        """
        Delete a vehicle from the system.

        The deletion will cascade to all associated alerts automatically
        due to the database cascade configuration.

        Args:
            vehicle_id: Unique identifier of the vehicle to delete

        Raises:
            VehicleNotFoundException: If vehicle with given ID doesn't exist
        """
        self._vehicle_repository.delete(vehicle_id)
