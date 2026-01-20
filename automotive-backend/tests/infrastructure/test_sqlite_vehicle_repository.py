"""Tests for SqliteVehicleRepository - Infrastructure layer."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.domain.entities.vehicle import Vehicle
from src.domain.exceptions.vehicle_not_found_exception import (
    VehicleNotFoundException,
)
from src.infrastructure.database.models import Base
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
def repository(test_db):
    """Create repository instance with test database."""
    return SqliteVehicleRepository(test_db)


class TestSqliteVehicleRepository:
    """Test suite for SqliteVehicleRepository."""

    def test_save_vehicle_to_database(self, repository, test_db):
        """
        Test saving a vehicle to SQLite database.

        Given a valid vehicle entity
        When save() is called
        Then the vehicle should be persisted in the database
        """
        # Arrange
        vehicle = Vehicle(
            id="V-123", plate="ABC-123", model="Toyota Corolla", current_mileage=5000
        )

        # Act
        repository.save(vehicle)

        # Assert
        from src.infrastructure.database.models import VehicleModel

        saved_vehicle = test_db.query(VehicleModel).filter_by(id="V-123").first()
        assert saved_vehicle is not None
        assert saved_vehicle.id == "V-123"
        assert saved_vehicle.plate == "ABC-123"
        assert saved_vehicle.model == "Toyota Corolla"
        assert saved_vehicle.current_mileage == 5000

    def test_get_vehicle_by_id_from_database(self, repository, test_db):
        """
        Test retrieving a vehicle by ID from SQLite database.

        Given a vehicle saved in the database
        When get_by_id() is called with the vehicle ID
        Then the vehicle entity should be returned with correct data
        """
        # Arrange
        from src.infrastructure.database.models import VehicleModel

        vehicle_model = VehicleModel(
            id="V-456", plate="XYZ-789", model="Honda Civic", current_mileage=15000
        )
        test_db.add(vehicle_model)
        test_db.commit()

        # Act
        vehicle = repository.get_by_id("V-456")

        # Assert
        assert vehicle is not None
        assert vehicle.id == "V-456"
        assert vehicle.plate == "XYZ-789"
        assert vehicle.model == "Honda Civic"
        assert vehicle.current_mileage == 15000

    def test_get_nonexistent_vehicle_raises_error(self, repository):
        """
        Test that getting a nonexistent vehicle raises VehicleNotFoundException.

        Given an empty database
        When get_by_id() is called with a nonexistent vehicle ID
        Then VehicleNotFoundException should be raised with appropriate message
        """
        # Act & Assert
        with pytest.raises(VehicleNotFoundException) as exc_info:
            repository.get_by_id("V-999")

        assert "Vehículo con ID V-999 no encontrado" in str(exc_info.value)
