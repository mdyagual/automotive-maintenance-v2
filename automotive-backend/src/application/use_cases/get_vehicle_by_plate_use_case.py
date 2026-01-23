"""Use case for retrieving a vehicle by plate number."""

from src.application.dtos.vehicle_dtos import VehicleDTO
from src.application.validators.vehicle_validator import VehicleValidator
from src.domain.ports.vehicle_repository import VehicleRepository


class GetVehicleByPlateUseCase:
    """Use case for retrieving a vehicle by its plate number."""

    def __init__(self, vehicle_repository: VehicleRepository):
        """
        Initialize use case with repository.

        Args:
            vehicle_repository: Repository for vehicle persistence
        """
        self._vehicle_repository = vehicle_repository

    def execute(self, plate: str) -> VehicleDTO:
        """
        Get vehicle by plate number.

        Args:
            plate: License plate number (case-insensitive)

        Returns:
            VehicleDTO with vehicle data

        Raises:
            InvalidPlateException: If plate format is invalid
            VehicleNotFoundException: If vehicle not found

        Business Rules:
        - RN-010: Plate must follow XXX-123 or XXX-1234 format
        - RN-031: Search must be case-insensitive
        """
        # Normalize plate to uppercase for validation and search (RN-031)
        normalized_plate = plate.upper() if plate else plate

        # Validate plate format at application boundary
        validator = VehicleValidator()
        validator.validate_plate(normalized_plate)

        # Get vehicle from repository (case-insensitive search)
        vehicle = self._vehicle_repository.get_by_plate(normalized_plate)

        # Map entity to DTO
        return VehicleDTO(
            id=vehicle.id,
            plate=vehicle.plate,
            model=vehicle.model,
            current_mileage=vehicle.current_mileage,
            status=vehicle.status.value,  # Convert enum to string
        )
