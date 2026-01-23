"""Shared fixtures for application layer tests."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.domain.strategies.basic_maintenance_strategy import BasicMaintenanceStrategy
from src.infrastructure.database.models import Base
from src.infrastructure.factories.observer_factory_impl import ObserverFactoryImpl
from src.infrastructure.repositories.sqlite_alert_repository import (
    SqliteAlertRepository,
)
from src.infrastructure.repositories.sqlite_vehicle_repository import (
    SqliteVehicleRepository,
)


@pytest.fixture
def test_db():
    """Create clean persistent SQLite database for each test."""
    engine = create_engine("sqlite:///test_maintenance.db")
    Base.metadata.create_all(engine)
    session_local = sessionmaker(bind=engine)
    session = session_local()

    yield session

    # Cleanup after test
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def vehicle_repository(test_db):
    """Create vehicle repository instance with test database."""
    return SqliteVehicleRepository(test_db)


@pytest.fixture
def alert_repository(test_db):
    """Create alert repository instance with test database."""
    return SqliteAlertRepository(test_db)


@pytest.fixture
def observer_factory(alert_repository):
    """Create observer factory instance with test dependencies."""
    strategies = [BasicMaintenanceStrategy()]
    return ObserverFactoryImpl(alert_repository=alert_repository, strategies=strategies)
