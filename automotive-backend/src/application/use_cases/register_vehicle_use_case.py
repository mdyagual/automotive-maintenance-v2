"""Use case for registering a new vehicle in the system."""

from datetime import datetime

from src.domain.entities.maintenance_alert import MaintenanceAlert
from src.domain.entities.vehicle import Vehicle
from src.domain.exceptions.duplicate_vehicle_exception import (
    DuplicateVehicleException,
)
from src.domain.exceptions.vehicle_not_found_exception import (
    VehicleNotFoundException,
)
from src.domain.ports.vehicle_repository import VehicleRepository


class RegisterVehicleUseCase:
    """Use case for registering a new vehicle."""

    def __init__(
        self,
        vehicle_repository: VehicleRepository,
        alert_repository=None,
        strategies=None,
    ):
        """Initialize use case with repository and alert dependencies."""
        self._vehicle_repository = vehicle_repository
        self._alert_repository = alert_repository
        self._strategies = strategies or []

    def execute(
        self, vehicle_id: str, plate: str, model: str, initial_mileage: int
    ) -> Vehicle:
        """
        Register a new vehicle in the system.

        Args:
            vehicle_id: Unique identifier for the vehicle
            plate: License plate number
            model: Vehicle model name
            initial_mileage: Starting mileage value

        Returns:
            The registered vehicle entity

        Raises:
            DuplicateVehicleException: If vehicle with same ID already exists
        """
        # Validate vehicle ID doesn't exist
        try:
            self._vehicle_repository.get_by_id(vehicle_id)
            raise DuplicateVehicleException(f"Ya existe un vehículo con ID {vehicle_id}")
        except VehicleNotFoundException:
            # Vehicle doesn't exist (expected), continue
            pass

        # Create new vehicle entity
        vehicle = Vehicle(
            id=vehicle_id, plate=plate, model=model, current_mileage=initial_mileage
        )

        # Save to repository
        self._vehicle_repository.save(vehicle)

        # Extensión: Generar alertas omitidas si el kilometraje inicial cruza umbrales
        if self._alert_repository and self._strategies:
            for strategy in self._strategies:
                old_threshold = strategy._calculate_threshold(0)
                new_threshold = strategy._calculate_threshold(initial_mileage)
                interval = strategy.INTERVAL
                alert_type = strategy.get_alert_type()
                if new_threshold > old_threshold:
                    for threshold in range(
                        old_threshold + interval, new_threshold + 1, interval
                    ):
                        # Verificar si ya existe una alerta para ese vehículo, tipo y kilometraje
                        existentes = self._alert_repository.get_by_vehicle_id(vehicle_id)
                        ya_existe = any(
                            a.alert_type == alert_type and a.mileage == threshold
                            for a in existentes
                        )
                        if not ya_existe:
                            alert = MaintenanceAlert(
                                id=(
                                    f"A-{vehicle_id}-{threshold}-"
                                    f"{alert_type.value}"
                                ),
                                vehicle_id=vehicle_id,
                                alert_type=alert_type,
                                mileage=threshold,
                                timestamp=datetime.now(),
                            )
                            self._alert_repository.save(alert)

        return vehicle
