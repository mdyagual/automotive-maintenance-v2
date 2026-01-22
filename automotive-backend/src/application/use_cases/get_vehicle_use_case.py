"""Use case for retrieving a single vehicle by ID."""

from src.application.dtos.vehicle_dtos import VehicleDTO
from src.domain.ports.vehicle_repository import VehicleRepository


class GetVehicleUseCase:
    """Use case for retrieving a single vehicle by ID."""
    
    def __init__(self, vehicle_repository: VehicleRepository):
        """
        Initialize use case with repository.
        
        Args:
            vehicle_repository: Repository for vehicle persistence
        """
        self._vehicle_repository = vehicle_repository
    
    def execute(self, vehicle_id: str) -> VehicleDTO:
        """
        Get vehicle by ID.
        
        Args:
            vehicle_id: Unique identifier
            
        Returns:
            VehicleDTO with vehicle data
            
        Raises:
            VehicleNotFoundException: If vehicle not found
        """
        # Get vehicle from repository
        vehicle = self._vehicle_repository.get_by_id(vehicle_id)
        
        # Map entity to DTO
        return VehicleDTO(
            id=vehicle.id,
            plate=vehicle.plate,
            model=vehicle.model,
            current_mileage=vehicle.current_mileage
        )
