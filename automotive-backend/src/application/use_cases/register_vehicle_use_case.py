"""Use case for registering a new vehicle in the system."""

from src.application.dtos.vehicle_dtos import RegisterVehicleCommand, VehicleDTO
from src.application.validators.vehicle_validator import VehicleValidator
from src.domain.entities.vehicle import Vehicle
from src.domain.exceptions.duplicate_vehicle_exception import (
    DuplicateVehicleException,
)
from src.domain.exceptions.vehicle_not_found_exception import (
    VehicleNotFoundException,
)
from src.domain.ports.observer_factory import ObserverFactory
from src.domain.ports.vehicle_repository import VehicleRepository


class RegisterVehicleUseCase:
    """Use case for registering a new vehicle."""

    def __init__(
        self,
        vehicle_repository: VehicleRepository,
        observer_factory: ObserverFactory = None,
    ):
        """
        Initialize use case with repository and observer factory.

        Args:
            vehicle_repository: Repository for vehicle persistence
            observer_factory: Factory for creating observers (optional)
        """
        self._vehicle_repository = vehicle_repository
        self._observer_factory = observer_factory

    def execute(self, command: RegisterVehicleCommand) -> VehicleDTO:
        """
        Register a new vehicle in the system.

        Args:
            command: RegisterVehicleCommand with vehicle data

        Returns:
            VehicleDTO with registered vehicle data

        Raises:
            DuplicateVehicleException: If vehicle with same ID already exists
            ValueError: If input data is invalid
        """
        # ✅ Validate input data at application boundary
        validator = VehicleValidator()
        validator.validate_vehicle_data(
            vehicle_id=command.vehicle_id,
            plate=command.plate,
            model=command.model,
            initial_mileage=command.initial_mileage
        )
        
        # Validate vehicle ID doesn't exist
        try:
            self._vehicle_repository.get_by_id(command.vehicle_id)
            raise DuplicateVehicleException(f"Ya existe un vehículo con ID {command.vehicle_id}")
        except VehicleNotFoundException:
            # Vehicle doesn't exist (expected), continue
            pass

        # Create new vehicle entity
        vehicle = Vehicle(
            id=command.vehicle_id,
            plate=command.plate,
            model=command.model,
            current_mileage=0  # Start at 0 to trigger all missed alerts
        )

        # ✅ Use Observer pattern to generate missed alerts
        if self._observer_factory and command.initial_mileage > 0:
            # Create observer starting from 0 to catch all thresholds
            observer = self._observer_factory.create_maintenance_observer(
                vehicle_id=command.vehicle_id,
                initial_mileage=0
            )
            vehicle.attach(observer)
            
            # Update to initial mileage - this triggers alert generation via observer
            vehicle.update_mileage(command.initial_mileage)

        # Save to repository
        self._vehicle_repository.save(vehicle)

        # Return DTO (not entity!)
        return VehicleDTO(
            id=vehicle.id,
            plate=vehicle.plate,
            model=vehicle.model,
            current_mileage=vehicle.current_mileage
        )
