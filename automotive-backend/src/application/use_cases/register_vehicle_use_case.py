"""Use case for registering a new vehicle in the system."""

from datetime import datetime

from src.application.dtos.vehicle_dtos import RegisterVehicleCommand, VehicleDTO
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

    def execute(self, command: RegisterVehicleCommand) -> VehicleDTO:
        """
        Register a new vehicle in the system.

        Args:
            command: RegisterVehicleCommand with vehicle data

        Returns:
            VehicleDTO with registered vehicle data

        Raises:
            DuplicateVehicleException: If vehicle with same ID already exists
        """
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
            current_mileage=command.initial_mileage
        )

        # Save to repository
        self._vehicle_repository.save(vehicle)

        # Extensión: Generar alertas omitidas si el kilometraje inicial cruza umbrales
        if self._alert_repository and self._strategies:
            for strategy in self._strategies:
                old_threshold = strategy._calculate_threshold(0)
                new_threshold = strategy._calculate_threshold(command.initial_mileage)
                interval = strategy.INTERVAL
                alert_type = strategy.get_alert_type()
                if new_threshold > old_threshold:
                    for threshold in range(
                        old_threshold + interval, new_threshold + 1, interval
                    ):
                        # Verificar si ya existe una alerta para ese vehículo, tipo y kilometraje
                        existentes = self._alert_repository.get_by_vehicle_id(command.vehicle_id)
                        ya_existe = any(
                            a.alert_type == alert_type and a.mileage == threshold
                            for a in existentes
                        )
                        if not ya_existe:
                            alert = MaintenanceAlert(
                                id=(
                                    f"A-{command.vehicle_id}-{threshold}-"
                                    f"{alert_type.value}"
                                ),
                                vehicle_id=command.vehicle_id,
                                alert_type=alert_type,
                                mileage=threshold,
                                timestamp=datetime.now(),
                            )
                            self._alert_repository.save(alert)

        # Return DTO (not entity!)
        return VehicleDTO(
            id=vehicle.id,
            plate=vehicle.plate,
            model=vehicle.model,
            current_mileage=vehicle.current_mileage
        )
