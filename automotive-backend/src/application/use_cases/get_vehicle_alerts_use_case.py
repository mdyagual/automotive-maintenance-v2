"""Use case for retrieving alerts for a specific vehicle."""

from src.application.dtos.alert_dtos import AlertDTO
from src.domain.ports.alert_repository import AlertRepository


class GetVehicleAlertsUseCase:
    """Use case for retrieving alerts for a specific vehicle."""

    def __init__(self, alert_repository: AlertRepository):
        """
        Initialize use case with repository.

        Args:
            alert_repository: Repository for alert persistence
        """
        self._alert_repository = alert_repository

    def execute(self, vehicle_id: str) -> list[AlertDTO]:
        """
        Get all alerts for a vehicle.

        Args:
            vehicle_id: Unique identifier of the vehicle

        Returns:
            List of AlertDTO objects for the vehicle
        """
        # Get all alerts from repository
        all_alerts = self._alert_repository.get_all()

        # Filter by vehicle_id (business logic in application layer)
        vehicle_alerts = [alert for alert in all_alerts if alert.vehicle_id == vehicle_id]

        # Map entities to DTOs
        return [
            AlertDTO(
                id=alert.id,
                vehicle_id=alert.vehicle_id,
                alert_type=alert.alert_type.name,  # Convert enum to string (use .name for uppercase)
                mileage=alert.mileage,
                timestamp=alert.timestamp,
            )
            for alert in vehicle_alerts
        ]
