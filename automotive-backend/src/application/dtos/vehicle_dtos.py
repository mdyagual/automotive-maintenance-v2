"""Vehicle DTOs for application layer."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class RegisterVehicleCommand:
    """Input DTO for registering a vehicle."""
    vehicle_id: str
    plate: str
    model: str
    initial_mileage: int


@dataclass(frozen=True)
class UpdateMileageCommand:
    """Input DTO for updating vehicle mileage."""
    vehicle_id: str
    new_mileage: int


@dataclass(frozen=True)
class DeleteVehicleCommand:
    """Input DTO for deleting a vehicle."""
    vehicle_id: str


@dataclass(frozen=True)
class VehicleDTO:
    """Output DTO for vehicle data."""
    id: str
    plate: str
    model: str
    current_mileage: int
    status: str


@dataclass(frozen=True)
class AlertDTO:
    """Output DTO for maintenance alert data."""
    id: str
    vehicle_id: str
    alert_type: str
    mileage: int
    timestamp: datetime


@dataclass(frozen=True)
class VehicleWithAlertsDTO:
    """Output DTO for vehicle with its alerts."""
    vehicle: VehicleDTO
    alerts: list[AlertDTO]


@dataclass(frozen=True)
class DeleteVehicleResultDTO:
    """Output DTO for delete vehicle operation result."""
    deleted_vehicle_id: str
    success: bool
    timestamp: datetime
