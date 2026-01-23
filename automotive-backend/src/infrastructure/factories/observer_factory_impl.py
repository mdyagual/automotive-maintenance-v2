"""Observer Factory Implementation - Infrastructure layer."""

from src.domain.ports.alert_repository import AlertRepository
from src.domain.ports.observer import Observer
from src.domain.ports.observer_factory import ObserverFactory
from src.domain.strategies.maintenance_strategy import MaintenanceStrategy
from src.infrastructure.observers.maintenance_alert_observer import (
    MaintenanceAlertObserver,
)


class ObserverFactoryImpl(ObserverFactory):
    """Infrastructure implementation of observer factory."""

    def __init__(self, alert_repository: AlertRepository, strategies: list[MaintenanceStrategy]) -> None:
        """
        Initialize factory with dependencies.

        Args:
            alert_repository: Repository for persisting alerts
            strategies: List of maintenance strategies
        """
        self._alert_repository = alert_repository
        self._strategies = strategies

    def create_maintenance_observer(self, vehicle_id: str, initial_mileage: int) -> Observer:
        """
        Create a maintenance alert observer.

        Args:
            vehicle_id: ID of the vehicle to observe
            initial_mileage: Initial mileage of the vehicle

        Returns:
            MaintenanceAlertObserver instance
        """
        return MaintenanceAlertObserver(
            vehicle_id=vehicle_id,
            alert_repository=self._alert_repository,
            strategies=self._strategies,
            initial_mileage=initial_mileage,
        )
