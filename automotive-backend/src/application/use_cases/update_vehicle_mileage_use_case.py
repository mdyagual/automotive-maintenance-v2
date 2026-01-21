"""Update Vehicle Mileage Use Case - Application layer."""

from src.application.dtos.vehicle_dtos import UpdateMileageCommand, VehicleDTO
from src.domain.ports.alert_repository import AlertRepository
from src.domain.ports.vehicle_repository import VehicleRepository
from src.domain.strategies.basic_maintenance_strategy import BasicMaintenanceStrategy
from src.domain.strategies.maintenance_strategy import MaintenanceStrategy
from src.infrastructure.observers.maintenance_alert_observer import MaintenanceAlertObserver


class UpdateVehicleMileageUseCase:
    """Use case for updating vehicle mileage following SRP."""

    def __init__(
        self,
        vehicle_repository: VehicleRepository,
        alert_repository: AlertRepository,
        strategies: list[MaintenanceStrategy] = None
    ) -> None:
        """
        Initialize use case with dependencies.

        Args:
            vehicle_repository: Repository for vehicle persistence
            alert_repository: Repository for alert persistence
            strategies: List of maintenance strategies (defaults to BasicMaintenanceStrategy)
        """
        self._vehicle_repository = vehicle_repository
        self._alert_repository = alert_repository
        self._strategies = strategies or [BasicMaintenanceStrategy()]

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
        # Obtener vehículo
        vehicle = self._vehicle_repository.get_by_id(command.vehicle_id)

        # Adjuntar observer real para alertas
        observer = MaintenanceAlertObserver(
            vehicle_id=command.vehicle_id,
            alert_repository=self._alert_repository,
            strategies=self._strategies,
            initial_mileage=vehicle.current_mileage
        )
        vehicle.attach(observer)

        # Actualizar kilometraje (la notificación y generación de alertas ocurre vía observer)
        vehicle.update_mileage(command.new_mileage)

        # Persistir vehículo actualizado
        self._vehicle_repository.save(vehicle)

        # Return DTO (not entity!)
        return VehicleDTO(
            id=vehicle.id,
            plate=vehicle.plate,
            model=vehicle.model,
            current_mileage=vehicle.current_mileage
        )
