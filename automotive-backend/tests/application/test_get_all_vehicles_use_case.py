"""Tests for GetAllVehiclesUseCase - Application layer."""
from datetime import datetime

import pytest

from src.application.use_cases.get_all_vehicles_use_case import GetAllVehiclesUseCase
from src.domain.entities.maintenance_alert import AlertType, MaintenanceAlert
from src.domain.entities.vehicle import Vehicle
from src.infrastructure.database.connection import SessionLocal, create_tables
from src.infrastructure.database.models import AlertModel, VehicleModel
from src.infrastructure.repositories.sqlite_alert_repository import SqliteAlertRepository
from src.infrastructure.repositories.sqlite_vehicle_repository import SqliteVehicleRepository


class TestGetAllVehiclesUseCase:
    """Test suite for GetAllVehiclesUseCase."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test database before each test."""
        create_tables()
        db = SessionLocal()

        # Clean database
        db.query(AlertModel).delete()
        db.query(VehicleModel).delete()
        db.commit()

        self.db = db
        self.vehicle_repository = SqliteVehicleRepository(db)
        self.alert_repository = SqliteAlertRepository(db)
        self.use_case = GetAllVehiclesUseCase(
            vehicle_repository=self.vehicle_repository,
            alert_repository=self.alert_repository
        )

        yield

        # Cleanup
        db.query(AlertModel).delete()
        db.query(VehicleModel).delete()
        db.commit()
        db.close()

    def test_get_all_vehicles_with_alerts_successfully(self):
        """
        Test getting all vehicles with their alerts.

        Given: Multiple vehicles with alerts in the database
        When: execute() is called
        Then: Returns all vehicles with their alerts ordered by timestamp descending
        """
        # Arrange
        vehicle1 = Vehicle(id="V-100", plate="ABC-100", model="Toyota", current_mileage=15000)
        vehicle2 = Vehicle(id="V-200", plate="XYZ-200", model="Honda", current_mileage=25000)
        vehicle3 = Vehicle(id="V-300", plate="DEF-300", model="Mazda", current_mileage=5000)

        self.vehicle_repository.save(vehicle1)
        self.vehicle_repository.save(vehicle2)
        self.vehicle_repository.save(vehicle3)

        # Add alerts for vehicle1
        alert1 = MaintenanceAlert(
            id="alert-1",
            vehicle_id="V-100",
            alert_type=AlertType.BASIC_MAINTENANCE,
            mileage=10000,
            timestamp=datetime(2026, 1, 1, 10, 0, 0)
        )
        alert2 = MaintenanceAlert(
            id="alert-2",
            vehicle_id="V-100",
            alert_type=AlertType.BASIC_MAINTENANCE,
            mileage=20000,
            timestamp=datetime(2026, 1, 5, 10, 0, 0)
        )
        self.alert_repository.save(alert1)
        self.alert_repository.save(alert2)

        # Add alert for vehicle2
        alert3 = MaintenanceAlert(
            id="alert-3",
            vehicle_id="V-200",
            alert_type=AlertType.MAJOR_MAINTENANCE,
            mileage=50000,
            timestamp=datetime(2026, 1, 3, 10, 0, 0)
        )
        self.alert_repository.save(alert3)

        # Act
        result = self.use_case.execute()

        # Assert
        assert len(result) == 3

        # Verify vehicle1 with 2 alerts (most recent first)
        vehicle1_result = next(v for v in result if v["vehicle"].id == "V-100")
        assert vehicle1_result["vehicle"].plate == "ABC-100"
        assert vehicle1_result["vehicle"].current_mileage == 15000
        assert len(vehicle1_result["alerts"]) == 2
        assert vehicle1_result["alerts"][0].id == "alert-2"  # Most recent first
        assert vehicle1_result["alerts"][1].id == "alert-1"

        # Verify vehicle2 with 1 alert
        vehicle2_result = next(v for v in result if v["vehicle"].id == "V-200")
        assert vehicle2_result["vehicle"].plate == "XYZ-200"
        assert len(vehicle2_result["alerts"]) == 1
        assert vehicle2_result["alerts"][0].id == "alert-3"

        # Verify vehicle3 with no alerts
        vehicle3_result = next(v for v in result if v["vehicle"].id == "V-300")
        assert vehicle3_result["vehicle"].plate == "DEF-300"
        assert len(vehicle3_result["alerts"]) == 0

    def test_get_all_vehicles_returns_empty_list_when_no_vehicles(self):
        """
        Test getting all vehicles when database is empty.

        Given: No vehicles in the database
        When: execute() is called
        Then: Returns empty list
        """
        # Act
        result = self.use_case.execute()

        # Assert
        assert result == []
        assert isinstance(result, list)
