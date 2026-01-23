"""Dependency injection configuration using FastAPI Depends for per-request sessions."""

from collections.abc import Generator

from fastapi import Depends
from fastapi.params import Depends as DependsClass
from sqlalchemy.orm import Session

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


def get_db_session() -> Generator[Session, None, None]:
    """
    Create a new database session per request.

    This function uses FastAPI's dependency injection to provide
    a request-scoped database session with automatic cleanup.

    Yields:
        Session: SQLAlchemy session for database operations

    Benefits:
        - New session per request (transaction isolation)
        - Automatic session cleanup (no memory leaks)
        - Thread-safe (each request has its own session)
        - Testable (can inject mock sessions)
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_vehicle_repository(db: Session = Depends(get_db_session)) -> SqliteVehicleRepository:
    """
    Create vehicle repository with request-scoped session.

    Args:
        db: Database session injected by FastAPI (or None for direct calls)

    Returns:
        SqliteVehicleRepository: Repository instance with its own session

    Note:
        This function works in two contexts:
        1. FastAPI context: db is injected via Depends()
        2. Direct call (tests): db is Depends object, so we manually consume the generator
    """
    # Handle direct calls (when db is a Depends object, not a Session)
    if isinstance(db, DependsClass):
        # Manually consume the generator for direct calls
        session_gen = get_db_session()
        db = next(session_gen)

    return SqliteVehicleRepository(db)


def get_alert_repository(db: Session = Depends(get_db_session)) -> SqliteAlertRepository:
    """
    Create alert repository with request-scoped session.

    Args:
        db: Database session injected by FastAPI (or None for direct calls)

    Returns:
        SqliteAlertRepository: Repository instance with its own session

    Note:
        This function works in two contexts:
        1. FastAPI context: db is injected via Depends()
        2. Direct call (tests): db is Depends object, so we manually consume the generator
    """
    # Handle direct calls (when db is a Depends object, not a Session)
    if isinstance(db, DependsClass):
        # Manually consume the generator for direct calls
        session_gen = get_db_session()
        db = next(session_gen)

    return SqliteAlertRepository(db)


def get_observer_factory(alert_repo: SqliteAlertRepository = Depends(get_alert_repository)) -> ObserverFactoryImpl:
    """
    Create observer factory with dependencies.

    Args:
        alert_repo: Alert repository injected by FastAPI (or None for direct calls)

    Returns:
        ObserverFactoryImpl: Factory instance with all maintenance strategies

    Note:
        This function works in two contexts:
        1. FastAPI context: alert_repo is injected via Depends()
        2. Direct call (tests): alert_repo is Depends object, so we call get_alert_repository()
    """
    # Handle direct calls (when alert_repo is a Depends object, not a repository)
    if isinstance(alert_repo, DependsClass):
        # Manually call get_alert_repository for direct calls
        alert_repo = get_alert_repository()

    strategies = [BasicMaintenanceStrategy(), MajorMaintenanceStrategy(), CriticalThresholdStrategy()]
    return ObserverFactoryImpl(alert_repo, strategies)


def initialize_test_data(vehicle_repo: SqliteVehicleRepository = Depends(get_vehicle_repository)) -> None:
    """
    Initialize test data for development.

    Args:
        vehicle_repo: Vehicle repository injected by FastAPI
    """
    # Check if test vehicle already exists
    try:
        vehicle_repo.get_by_id("V-123")
        # Vehicle exists, skip initialization
        return
    except VehicleNotFoundException:
        # Vehicle doesn't exist, create it
        test_vehicle = Vehicle(id="V-123", plate="ABC-123", model="Toyota Corolla", current_mileage=5000)
        vehicle_repo.save(test_vehicle)
