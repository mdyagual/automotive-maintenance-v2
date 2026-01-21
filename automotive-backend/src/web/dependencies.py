"""Dependency injection configuration."""

from src.domain.entities.vehicle import Vehicle
from src.domain.exceptions.vehicle_not_found_exception import (
    VehicleNotFoundException,
)
from src.domain.strategies.basic_maintenance_strategy import BasicMaintenanceStrategy
from src.domain.strategies.critical_threshold_strategy import CriticalThresholdStrategy
from src.domain.strategies.major_maintenance_strategy import MajorMaintenanceStrategy
from src.infrastructure.database.connection import SessionLocal, create_tables
from src.infrastructure.factories.observer_factory_impl import ObserverFactoryImpl
from src.infrastructure.repositories.sqlite_alert_repository import SqliteAlertRepository
from src.infrastructure.repositories.sqlite_vehicle_repository import SqliteVehicleRepository

# Create database tables on startup
create_tables()

# Create session
_db_session = SessionLocal()

# Singleton instances
_vehicle_repository = SqliteVehicleRepository(_db_session)
_alert_repository = SqliteAlertRepository(_db_session)

# Create observer factory with all strategies
_observer_factory = ObserverFactoryImpl(
    alert_repository=_alert_repository,
    strategies=[
        BasicMaintenanceStrategy(),
        MajorMaintenanceStrategy(),
        CriticalThresholdStrategy()
    ]
)


def get_vehicle_repository() -> SqliteVehicleRepository:
    """Get vehicle repository instance."""
    return _vehicle_repository


def get_alert_repository() -> SqliteAlertRepository:
    """Get alert repository instance."""
    return _alert_repository


def get_observer_factory() -> ObserverFactoryImpl:
    """Get observer factory instance."""
    return _observer_factory


def initialize_test_data() -> None:
    """Initialize test data for development."""
    # Check if test vehicle already exists
    try:
        _vehicle_repository.get_by_id("V-123")
        # Vehicle exists, skip initialization
        return
    except VehicleNotFoundException:
        # Vehicle doesn't exist, create it
        test_vehicle = Vehicle(
            id="V-123", plate="ABC-123", model="Toyota Corolla", current_mileage=5000
        )
        _vehicle_repository.save(test_vehicle)
