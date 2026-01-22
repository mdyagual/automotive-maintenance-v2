"""Update Vehicle Mileage Use Case - Application layer."""

from src.application.dtos.vehicle_dtos import UpdateMileageCommand, VehicleDTO
from src.domain.ports.observer_factory import ObserverFactory
from src.domain.ports.vehicle_repository import VehicleRepository


class UpdateVehicleMileageUseCase:
    """Use case for updating vehicle mileage following SRP."""

    def __init__(
        self,
        vehicle_repository: VehicleRepository,
        observer_factory: ObserverFactory
    ) -> None:
        """
        Initialize use case with dependencies.

        Args:
            vehicle_repository: Repository for vehicle persistence
            observer_factory: Factory for creating observers (domain abstraction)
        """
        self._vehicle_repository = vehicle_repository
        self._observer_factory = observer_factory

    def execute(self, command: UpdateMileageCommand) -> VehicleDTO:
        """
        Execute the use case to update vehicle mileage.

        Args:
            command: UpdateMileageCommand with vehicle_id and new_mileage

        Returns:
            VehicleDTO with updated vehicle data

        Raises:
            InvalidMileageException: If new mileage is invalid
            VehicleNotFoundException: If vehicle not found
        """
        # Get vehicle
        vehicle = self._vehicle_repository.get_by_id(command.vehicle_id)

        # ✅ Use factory (domain abstraction) to create observer
        observer = self._observer_factory.create_maintenance_observer(
            vehicle_id=command.vehicle_id,
            initial_mileage=vehicle.current_mileage
        )
        vehicle.attach(observer)

        # Update mileage (notification and alert generation occurs via observer)
        vehicle.update_mileage(command.new_mileage)

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
