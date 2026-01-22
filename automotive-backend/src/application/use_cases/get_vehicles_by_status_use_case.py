"""Use case for getting vehicles filtered by status - Application layer."""

from src.application.dtos.vehicle_dtos import VehicleDTO
from src.domain.entities.vehicle_status import VehicleStatus
from src.domain.ports.vehicle_repository import VehicleRepository


class GetVehiclesByStatusUseCase:
    """
    Use case for retrieving vehicles filtered by operational status.

    Implements HU-005 Escenario 2: Filter vehicles by status.

    This use case:
    1. Accepts a VehicleStatus enum parameter
    2. Delegates filtering to the repository
    3. Converts domain entities to DTOs
    4. Returns list of VehicleDTO (not domain entities)

    Clean Architecture compliance:
    - Depends on domain abstractions (VehicleRepository port)
    - Returns DTOs, not domain entities
    - No infrastructure concerns
    - Pure orchestration logic
    """

    def __init__(self, vehicle_repository: VehicleRepository) -> None:
        """
        Initialize use case with repository dependency.

        Args:
            vehicle_repository: Repository for vehicle persistence
        """
        self._vehicle_repository = vehicle_repository

    def execute(self, status: VehicleStatus) -> list[VehicleDTO]:
        """
        Execute the use case to get vehicles by status.

        Args:
            status: Vehicle status to filter by (VehicleStatus enum)

        Returns:
            List of VehicleDTO with the specified status
            Empty list if no vehicles match

        Business Rules:
        - RN-029: Vehicles can be filtered by status in queries
        - RN-025: Valid statuses are: active, inactive, in_maintenance, retired
        """
        # Delegate filtering to repository
        vehicles = self._vehicle_repository.get_by_status(status)

        # Convert domain entities to DTOs
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

        return vehicle_dtos
