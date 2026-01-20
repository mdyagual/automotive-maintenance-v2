"""Tests for SqliteAlertRepository - Infrastructure layer."""

from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.domain.entities.maintenance_alert import AlertType, MaintenanceAlert
from src.infrastructure.database.models import Base
from src.infrastructure.repositories.sqlite_alert_repository import (
    SqliteAlertRepository,
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
def repository(test_db):
    """Create repository instance with test database."""
    return SqliteAlertRepository(test_db)


class TestSqliteAlertRepository:
    """Test suite for SqliteAlertRepository."""

    def test_save_alert_to_database(self, repository, test_db):
        """
        Test saving an alert to SQLite database.

        Given a valid alert entity
        When save() is called
        Then the alert should be persisted in the database
        """
        # Arrange
        alert = MaintenanceAlert(
            id="V-123-10000-BASIC",
            vehicle_id="V-123",
            alert_type=AlertType.BASIC_MAINTENANCE,
            mileage=10000,
            timestamp=datetime(2026, 1, 7, 10, 0, 0),
        )

        # Act
        repository.save(alert)

        # Assert
        from src.infrastructure.database.models import AlertModel

        saved_alert = (
            test_db.query(AlertModel).filter_by(id="V-123-10000-BASIC").first()
        )
        assert saved_alert is not None
        assert saved_alert.id == "V-123-10000-BASIC"
        assert saved_alert.vehicle_id == "V-123"
        assert saved_alert.alert_type == AlertType.BASIC_MAINTENANCE
        assert saved_alert.mileage == 10000
        assert saved_alert.timestamp == datetime(2026, 1, 7, 10, 0, 0)

    def test_get_all_alerts_from_database(self, repository, test_db):
        """
        Test retrieving all alerts from SQLite database.

        Given multiple alerts saved in the database
        When get_all() is called
        Then all alert entities should be returned
        """
        # Arrange
        from src.infrastructure.database.models import AlertModel

        alert1 = AlertModel(
            id="V-123-10000-BASIC",
            vehicle_id="V-123",
            alert_type=AlertType.BASIC_MAINTENANCE,
            mileage=10000,
            timestamp=datetime(2026, 1, 7, 10, 0, 0),
        )
        alert2 = AlertModel(
            id="V-123-50000-MAJOR",
            vehicle_id="V-123",
            alert_type=AlertType.MAJOR_MAINTENANCE,
            mileage=50000,
            timestamp=datetime(2026, 1, 7, 11, 0, 0),
        )
        test_db.add(alert1)
        test_db.add(alert2)
        test_db.commit()

        # Act
        alerts = repository.get_all()

        # Assert
        assert len(alerts) == 2
        # Orden descendente: más reciente primero (11:00 antes que 10:00)
        assert alerts[0].id == "V-123-50000-MAJOR"
        assert alerts[0].alert_type == AlertType.MAJOR_MAINTENANCE
        assert alerts[1].id == "V-123-10000-BASIC"
        assert alerts[1].alert_type == AlertType.BASIC_MAINTENANCE
