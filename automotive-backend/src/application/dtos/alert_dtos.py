"""Data Transfer Objects for alerts."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AlertDTO:
    """Output DTO for alert data."""
    id: str
    vehicle_id: str
    alert_type: str  # String, not enum
    mileage: int
    timestamp: datetime
