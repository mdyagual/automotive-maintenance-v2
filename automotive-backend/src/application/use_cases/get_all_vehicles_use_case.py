"""Get All Vehicles Use Case - Application layer."""
from typing import TypedDict

from src.domain.entities.maintenance_alert import MaintenanceAlert
from src.domain.entities.vehicle import Vehicle
from src.domain.ports.alert_repository import AlertRepository
from src.domain.ports.vehicle_repository import VehicleRepository


class VehicleWithAlerts(TypedDict):
    """Type definition for vehicle with its alerts."""
    vehicle: Vehicle
    alerts: list[MaintenanceAlert]


class GetAllVehiclesUseCase:
    """Use case for retrieving all vehicles with their alerts following SRP."""

    def __init__(
        self,
        vehicle_repository: VehicleRepository,
        alert_repository: AlertRepository
    ) -> None:
        """
        Initialize use case with dependencies following DIP.

        Args:
            vehicle_repository: Repository for vehicle persistence
            alert_repository: Repository for alert persistence
        """
        self._vehicle_repository = vehicle_repository
        self._alert_repository = alert_repository

    def execute(self) -> list[VehicleWithAlerts]:
        """
        Execute the use case to get all vehicles with their alerts.

        Returns:
            List of VehicleWithAlerts containing vehicle and its alerts.
            Each item has:
            - "vehicle": Vehicle entity
            - "alerts": List of MaintenanceAlert entities (most recent first)
        """
        vehicles = self._vehicle_repository.get_all()

        result: list[VehicleWithAlerts] = []
        for vehicle in vehicles:
            alerts = self._alert_repository.get_by_vehicle_id(vehicle.id)
            result.append({
                "vehicle": vehicle,
                "alerts": alerts
            })

        return result
