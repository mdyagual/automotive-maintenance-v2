"""Use case for retrieving vehicles by plate number."""

from src.application.dtos.vehicle_dtos import VehicleDTO
from src.application.validators.vehicle_validator import VehicleValidator
from src.domain.exceptions.vehicle_not_found_exception import VehicleNotFoundException
from src.domain.ports.vehicle_repository import VehicleRepository


class GetVehicleByPlateUseCase:
    """Use case for retrieving vehicles by plate number (supports partial match)."""

    def __init__(self, vehicle_repository: VehicleRepository):
        """
        Initialize use case with repository.

        Args:
            vehicle_repository: Repository for vehicle persistence
        """
        self._vehicle_repository = vehicle_repository

    def execute(self, plate: str) -> VehicleDTO | list[VehicleDTO]:
        """
        Get vehicles by plate number (supports partial match).

        Args:
            plate: License plate number or partial plate (case-insensitive)

        Returns:
            - Single VehicleDTO if exactly one match found
            - List of VehicleDTO if multiple matches found
            - Raises exception if no matches found

        Raises:
            InvalidPlateException: If plate format is invalid (for exact matches)
            VehicleNotFoundException: If no vehicles found

        Business Rules:
        - RN-010: Plate must follow XXX-123 or XXX-1234 format (for exact matches)
        - RN-031: Search must be case-insensitive
        - RN-032: Search must support partial matches
        """
        # Validate plate is not empty or whitespace
        if not plate or not plate.strip():
            raise VehicleNotFoundException("La placa de búsqueda no puede estar vacía")

        # Normalize plate to uppercase for search (RN-031)
        normalized_plate = plate.strip().upper()

        # Validate plate format only if it looks like a complete plate
        # Partial searches (less than 7 chars) skip validation
        if len(normalized_plate) >= 7:
            validator = VehicleValidator()
            try:
                validator.validate_plate(normalized_plate)
            except Exception:
                # If validation fails, treat as partial search
                pass

        # Get vehicles from repository (case-insensitive, partial match)
        vehicles = self._vehicle_repository.get_by_plate(normalized_plate)

        # If no vehicles found, raise exception
        if not vehicles:
            raise VehicleNotFoundException(f"No se encontraron vehículos con placa que contenga '{plate}'")

        # Map entities to DTOs
        vehicle_dtos = [
            VehicleDTO(
                id=vehicle.id,
                plate=vehicle.plate,
                model=vehicle.model,
                current_mileage=vehicle.current_mileage,
                status=vehicle.status.value,  # Convert enum to string
            )
            for vehicle in vehicles
        ]

        # Return single DTO if only one match, otherwise return list
        if len(vehicle_dtos) == 1:
            return vehicle_dtos[0]

        return vehicle_dtos
