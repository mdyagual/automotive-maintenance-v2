"""Update Vehicle Mileage Use Case - Application layer."""

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



    def execute(self, vehicle_id: str, new_mileage: int) -> None:
        """
        Execute the use case to update vehicle mileage.

        Args:
            vehicle_id: Unique identifier of the vehicle
            new_mileage: New mileage value

        Raises:
            InvalidMileageException: If new mileage is invalid
            VehicleNotFoundException: If vehicle not found
        """
        # Obtener vehículo
        vehicle = self._vehicle_repository.get_by_id(vehicle_id)

        # Adjuntar observer real para alertas

        observer = MaintenanceAlertObserver(
            vehicle_id=vehicle_id,
            alert_repository=self._alert_repository,
            strategies=self._strategies,
            initial_mileage=vehicle.current_mileage
        )
        vehicle.attach(observer)

        # Actualizar kilometraje (la notificación y generación de alertas ocurre vía observer)
        vehicle.update_mileage(new_mileage)

        # Persistir vehículo actualizado
        self._vehicle_repository.save(vehicle)
