"""Get All Vehicles Use Case - Application layer."""

from src.application.dtos.vehicle_dtos import AlertDTO, VehicleDTO, VehicleWithAlertsDTO
from src.domain.ports.alert_repository import AlertRepository
from src.domain.ports.vehicle_repository import VehicleRepository


class GetAllVehiclesUseCase:
    """Use case for retrieving all vehicles with their alerts following SRP."""

    def __init__(self, vehicle_repository: VehicleRepository, alert_repository: AlertRepository) -> None:
        """
        Initialize use case with dependencies following DIP.

        Args:
            vehicle_repository: Repository for vehicle persistence
            alert_repository: Repository for alert persistence
        """
        self._vehicle_repository = vehicle_repository
        self._alert_repository = alert_repository

    def execute(self) -> list[VehicleWithAlertsDTO]:
        """
        Execute the use case to get all vehicles with their alerts.

        Returns:
            List of VehicleWithAlertsDTO containing vehicle and its alerts.
            Each item has:
            - vehicle: VehicleDTO with vehicle data
            - alerts: List of AlertDTO (most recent first)
        """
        vehicles = self._vehicle_repository.get_all()

        result: list[VehicleWithAlertsDTO] = []
        for vehicle in vehicles:
            alerts = self._alert_repository.get_by_vehicle_id(vehicle.id)

            # Map domain entities to DTOs
            vehicle_dto = VehicleDTO(
                id=vehicle.id,
                plate=vehicle.plate,
                model=vehicle.model,
                current_mileage=vehicle.current_mileage,
                status=vehicle.status.value,  # Convert enum to string
            )

            alert_dtos = [AlertDTO(id=alert.id, vehicle_id=alert.vehicle_id, alert_type=alert.alert_type.value, mileage=alert.mileage, timestamp=alert.timestamp) for alert in alerts]

            result.append(VehicleWithAlertsDTO(vehicle=vehicle_dto, alerts=alert_dtos))

        return result
