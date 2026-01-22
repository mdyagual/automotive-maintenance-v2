"""Vehicle entity - Domain model."""

import re
from datetime import datetime

from src.domain.entities.vehicle_status import VehicleStatus
from src.domain.exceptions.invalid_mileage_exception import InvalidMileageException
from src.domain.exceptions.invalid_model_exception import InvalidModelException
from src.domain.exceptions.invalid_plate_exception import InvalidPlateException
from src.domain.exceptions.invalid_vehicle_id_exception import InvalidVehicleIdException
from src.domain.ports.observer import Observer


class Vehicle:
    """Vehicle entity representing a fleet vehicle."""

    # Domain invariants - validation patterns
    VEHICLE_ID_PATTERN = r'^V-\d{3}$'  # RN-011: V-XXX format
    PLATE_PATTERN = r'^[A-Z]{3}-\d{3,4}$'  # RN-010: XXX-123 or XXX-1234
    MAX_MODEL_LENGTH = 100
    MAX_MILEAGE = 1_000_000
    MAX_MILEAGE_INCREMENT = 50_000
    MAINTENANCE_INTERVAL = 10_000

    def __init__(
        self,
        id: str,
        plate: str,
        model: str,
        current_mileage: int,
        status: VehicleStatus = VehicleStatus.ACTIVE,
        status_updated_at: datetime | None = None
    ) -> None:
        """
        Initialize a Vehicle instance with validation.

        Args:
            id: Unique identifier for the vehicle
            plate: License plate number
            model: Vehicle model name
            current_mileage: Current mileage in kilometers
            status: Operational status of the vehicle (default: ACTIVE)
            status_updated_at: Timestamp of last status update (default: now)

        Raises:
            InvalidVehicleIdException: If id format is invalid (RN-011)
            InvalidPlateException: If plate format is invalid (RN-010)
            InvalidModelException: If model is invalid
            InvalidMileageException: If mileage is invalid

        Business Rules:
        - RN-011: Vehicle ID must follow V-XXX format
        - RN-010: Plate must follow XXX-123 or XXX-1234 format
        - RN-002: Mileage cannot be negative
        - RN-003: Mileage cannot exceed 1,000,000 km
        """
        # Validate domain invariants in constructor (Always Valid principle)
        self._validate_vehicle_id(id)
        self._validate_plate(plate)
        self._validate_model(model)
        self._validate_initial_mileage(current_mileage)

        self.id = id
        self.plate = plate
        self.model = model
        self.current_mileage = current_mileage
        self.status = status
        self.status_updated_at = status_updated_at or datetime.now()
        self._observers: list[Observer] = []

    def _validate_vehicle_id(self, vehicle_id: str) -> None:
        """
        Validate vehicle ID format (RN-011).

        Args:
            vehicle_id: Vehicle identifier to validate

        Raises:
            InvalidVehicleIdException: If format is invalid
        """
        if not vehicle_id or not isinstance(vehicle_id, str):
            raise InvalidVehicleIdException(
                "El vehicle_id no puede estar vacío"
            )

        if not re.match(self.VEHICLE_ID_PATTERN, vehicle_id):
            raise InvalidVehicleIdException(
                f"Formato de vehicle_id inválido: '{vehicle_id}'. "
                f"Formato esperado: V-XXX (ejemplo: V-001, V-123)"
            )

    def _validate_plate(self, plate: str) -> None:
        """
        Validate plate format (RN-010).

        Args:
            plate: License plate to validate

        Raises:
            InvalidPlateException: If format is invalid
        """
        if not plate or not isinstance(plate, str):
            raise InvalidPlateException(
                "La placa no puede estar vacía"
            )

        if not re.match(self.PLATE_PATTERN, plate):
            raise InvalidPlateException(
                f"Formato de placa inválido: '{plate}'. "
                f"Formato esperado: XXX-123 o XXX-1234 (ejemplo: ABC-123, XYZ-9999)"
            )

    def _validate_model(self, model: str) -> None:
        """
        Validate model name.

        Args:
            model: Vehicle model name to validate

        Raises:
            InvalidModelException: If model is invalid
        """
        if not model or not isinstance(model, str):
            raise InvalidModelException("El modelo no puede estar vacío")

        if not model.strip():
            raise InvalidModelException("El modelo no puede estar vacío")

        if len(model) > self.MAX_MODEL_LENGTH:
            raise InvalidModelException(
                f"El modelo excede la longitud máxima de {self.MAX_MODEL_LENGTH} caracteres"
            )

    def _validate_initial_mileage(self, mileage: int) -> None:
        """
        Validate initial mileage (RN-002, RN-003).

        Args:
            mileage: Initial mileage value to validate

        Raises:
            InvalidMileageException: If mileage is invalid
        """
        if not isinstance(mileage, int):
            raise InvalidMileageException(
                f"El kilometraje debe ser un entero, recibido: {type(mileage).__name__}"
            )

        if mileage < 0:
            raise InvalidMileageException(
                f"El kilometraje inicial no puede ser negativo: {mileage}"
            )

        if mileage > self.MAX_MILEAGE:
            raise InvalidMileageException(
                f"El kilometraje inicial {mileage:,} km excede el máximo "
                f"permitido de {self.MAX_MILEAGE:,} km"
            )

    def attach(self, observer: Observer) -> None:
        """Attach an observer to receive notifications."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Detach an observer from notifications."""
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify_observers(self) -> None:
        """Notify all observers about mileage update."""
        for observer in self._observers:
            observer.update(self.id, self.current_mileage)

    def _crosses_maintenance_threshold(self, old_mileage: int, new_mileage: int) -> bool:
        """
        Check if update crosses a maintenance threshold.

        Args:
            old_mileage: Previous mileage value
            new_mileage: New mileage value

        Returns:
            True if crosses a 10,000 km threshold, False otherwise
        """
        old_threshold = (old_mileage // self.MAINTENANCE_INTERVAL) * self.MAINTENANCE_INTERVAL
        new_threshold = (new_mileage // self.MAINTENANCE_INTERVAL) * self.MAINTENANCE_INTERVAL
        return new_threshold > old_threshold

    def update_status(self, new_status: VehicleStatus) -> None:
        """
        Update vehicle operational status.

        Args:
            new_status: New status value (must be VehicleStatus enum)

        Raises:
            TypeError: If new_status is not a VehicleStatus enum

        Business Rules:
        - RN-025: Valid statuses are: active, inactive, in_maintenance, retired
        - RN-028: Status change must record update timestamp
        """
        # Validate that new_status is a VehicleStatus enum
        if not isinstance(new_status, VehicleStatus):
            raise TypeError(
                f"Status must be a VehicleStatus enum. "
                f"Valid statuses are: {', '.join([s.value for s in VehicleStatus])}"
            )

        self.status = new_status
        self.status_updated_at = datetime.now()

    def update_mileage(self, new_mileage: int) -> None:
        """
        Update vehicle mileage.

        Args:
            new_mileage: New mileage value

        Raises:
            InvalidMileageException: If new mileage is not greater than current
                                    or if vehicle is retired

        Business Rules:
        - RN-027: Cannot update mileage of retired vehicles
        """
        # Check if vehicle is retired (RN-027) - must be first check
        if self.status == VehicleStatus.RETIRED:
            raise InvalidMileageException(
                "No se puede actualizar kilometraje de vehículos retirados"
            )

        if new_mileage <= self.current_mileage:
            raise InvalidMileageException(
                f"El kilometraje {new_mileage} debe ser mayor al actual {self.current_mileage}"
            )

        if new_mileage > self.MAX_MILEAGE:
            raise InvalidMileageException(
                f"El kilometraje {new_mileage} excede el límite máximo de {self.MAX_MILEAGE:,} km"
            )

        increment = new_mileage - self.current_mileage
        if increment > self.MAX_MILEAGE_INCREMENT:
            raise InvalidMileageException(
                f"El incremento de {increment:,} km excede el máximo permitido de "
                f"{self.MAX_MILEAGE_INCREMENT:,} km"
            )

        self.current_mileage = new_mileage

        # Notify observers on every mileage update
        # The observer decides whether to generate alerts based on thresholds
        self._notify_observers()
