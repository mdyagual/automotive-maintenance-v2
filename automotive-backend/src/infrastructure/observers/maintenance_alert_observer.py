"""Observer real para generación y persistencia de alertas de mantenimiento."""
from datetime import datetime

from src.domain.entities.maintenance_alert import MaintenanceAlert
from src.domain.ports.alert_repository import AlertRepository
from src.domain.ports.observer import Observer
from src.domain.strategies.maintenance_strategy import MaintenanceStrategy


class MaintenanceAlertObserver(Observer):
    """Observer que genera y persiste alertas de mantenimiento usando estrategias."""
    def __init__(self, vehicle_id: str, alert_repository: AlertRepository, strategies: list[MaintenanceStrategy], initial_mileage: int):
        self._vehicle_id = vehicle_id
        self._alert_repository = alert_repository
        self._strategies = strategies
        self._last_mileage = initial_mileage

    def update(self, vehicle_id: str, mileage: int) -> None:
        # Solo genera alertas si el vehicle_id coincide
        if vehicle_id != self._vehicle_id:
            return
        old_mileage = self._last_mileage
        for strategy in self._strategies:
            if strategy.should_generate_alert(old_mileage, mileage):
                alert_type = strategy.get_alert_type()
                alert_id = f"A-{vehicle_id}-{mileage}-{alert_type.value}"
                alert = MaintenanceAlert(
                    id=alert_id,
                    vehicle_id=vehicle_id,
                    alert_type=alert_type,
                    mileage=mileage,
                    timestamp=datetime.now()
                )
                self._alert_repository.save(alert)
        self._last_mileage = mileage
