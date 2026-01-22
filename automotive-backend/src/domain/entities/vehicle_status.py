"""Vehicle status enum - Domain model."""

from enum import Enum


class VehicleStatus(str, Enum):
    """Enum representing the operational status of a vehicle."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    IN_MAINTENANCE = "in_maintenance"
    RETIRED = "retired"
