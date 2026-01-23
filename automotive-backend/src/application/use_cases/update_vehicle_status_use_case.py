"""Update Vehicle Status Use Case - Application layer."""

from src.application.dtos.vehicle_dtos import UpdateStatusCommand, VehicleDTO
from src.application.validators.vehicle_validator import VehicleValidator
from src.domain.entities.vehicle_status import VehicleStatus
from src.domain.exceptions.invalid_status_exception import InvalidStatusException
from src.domain.ports.vehicle_repository import VehicleRepository


class UpdateVehicleStatusUseCase:
    """Use case for updating vehicle operational status following SRP."""

    def __init__(self, vehicle_repository: VehicleRepository) -> None:
        """
        Initialize use case with dependencies.

        Args:
            vehicle_repository: Repository for vehicle persistence
        """
        self._vehicle_repository = vehicle_repository

    def execute(self, command: UpdateStatusCommand) -> VehicleDTO:
        """
        Execute the use case to update vehicle status.

        Args:
            command: UpdateStatusCommand with vehicle_id and new_status

        Returns:
            VehicleDTO with updated vehicle data

        Raises:
            InvalidVehicleIdException: If vehicle_id format is invalid
            InvalidStatusException: If status value is invalid
            VehicleNotFoundException: If vehicle not found

        Business Rules:
        - RN-025: Valid statuses are: active, inactive, in_maintenance, retired
        - RN-028: Status change must record update timestamp
        """
        # Validate vehicle_id format at application boundary
        validator = VehicleValidator()
        validator.validate_vehicle_id(command.vehicle_id)

        # Validate and convert status string to enum
        try:
            status_enum = VehicleStatus(command.new_status.lower())
        except ValueError:
            valid_statuses = [s.value for s in VehicleStatus]
            raise InvalidStatusException(
                f"Estado inválido '{command.new_status}'. Estados válidos: {', '.join(valid_statuses)}"
            )

        # Get vehicle
        vehicle = self._vehicle_repository.get_by_id(command.vehicle_id)

        # Update status (domain method handles validation and timestamp)
        vehicle.update_status(status_enum)

        # Persist updated vehicle
        self._vehicle_repository.save(vehicle)

        # Return DTO (not entity!)
        return VehicleDTO(
            id=vehicle.id,
            plate=vehicle.plate,
            model=vehicle.model,
            current_mileage=vehicle.current_mileage,
            status=vehicle.status.value,  # Convert enum to string
        )
