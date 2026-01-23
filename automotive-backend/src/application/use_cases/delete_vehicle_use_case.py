"""Use case for deleting a vehicle from the system."""

from datetime import datetime

from src.application.dtos.vehicle_dtos import DeleteVehicleCommand, DeleteVehicleResultDTO
from src.application.validators.vehicle_validator import VehicleValidator
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

    def execute(self, command: DeleteVehicleCommand) -> DeleteVehicleResultDTO:
        """
        Delete a vehicle from the system.

        The deletion will cascade to all associated alerts automatically
        due to the database cascade configuration.

        Args:
            command: DeleteVehicleCommand with vehicle_id

        Returns:
            DeleteVehicleResultDTO with operation confirmation

        Raises:
            InvalidVehicleIdException: If vehicle_id format is invalid
            VehicleNotFoundException: If vehicle with given ID doesn't exist
        """
        # ✅ Validate vehicle_id format at application boundary
        validator = VehicleValidator()
        validator.validate_vehicle_id(command.vehicle_id)

        # Delete the vehicle (will raise VehicleNotFoundException if not found)
        self._vehicle_repository.delete(command.vehicle_id)

        # Return confirmation DTO
        return DeleteVehicleResultDTO(deleted_vehicle_id=command.vehicle_id, success=True, timestamp=datetime.now())
