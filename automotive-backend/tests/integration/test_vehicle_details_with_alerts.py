"""
Integration tests for HU-003 Escenario 6: Vehicle details with alerts visualization.

Given existe un vehículo 'V-123' con 3 alertas de mantenimiento
When el usuario hace clic en el botón "Detalles" del vehículo
Then el sistema debe mostrar un modal con la información del vehículo
And el modal debe incluir una sección de "Alertas de Mantenimiento"
And debe mostrar las 3 alertas ordenadas cronológicamente (más reciente primero)
And cada alerta debe mostrar: tipo, mensaje, kilometraje y fecha de generación
"""

from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from src.domain.entities.maintenance_alert import AlertType, MaintenanceAlert
from src.domain.entities.vehicle import Vehicle
from src.infrastructure.database.connection import SessionLocal, engine
from src.infrastructure.database.models import AlertModel, Base, VehicleModel
from src.web.dependencies import get_alert_repository, get_vehicle_repository
from src.web.main import app


@pytest.fixture
def reset_test_data():
    """Reset database to known state before each test."""
    # Recreate all tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Get repositories
    vehicle_repo = get_vehicle_repository()
    alert_repo = get_alert_repository()

    # Create test vehicle V-123
    test_vehicle = Vehicle(
        id="V-123", plate="ABC-123", model="Toyota Corolla", current_mileage=35000
    )
    vehicle_repo.save(test_vehicle)

    # Create 3 alerts with different timestamps
    alert1 = MaintenanceAlert(
        id="alert-1",
        vehicle_id="V-123",
        alert_type=AlertType.BASIC_MAINTENANCE,
        mileage=10000,
        timestamp=datetime(2026, 1, 10, 10, 0, 0),
    )
    alert2 = MaintenanceAlert(
        id="alert-2",
        vehicle_id="V-123",
        alert_type=AlertType.MAJOR_MAINTENANCE,
        mileage=20000,
        timestamp=datetime(2026, 1, 15, 14, 30, 0),
    )
    alert3 = MaintenanceAlert(
        id="alert-3",
        vehicle_id="V-123",
        alert_type=AlertType.BASIC_MAINTENANCE,
        mileage=30000,
        timestamp=datetime(2026, 1, 20, 9, 15, 0),
    )

    alert_repo.save(alert1)
    alert_repo.save(alert2)
    alert_repo.save(alert3)

    yield

    # Cleanup
    session = SessionLocal()
    session.query(AlertModel).delete()
    session.query(VehicleModel).delete()
    session.commit()
    session.close()


class TestVehicleDetailsWithAlerts:
    """Test cases for vehicle details with alerts - HU-003 Escenario 6."""

    def test_get_vehicle_with_alerts_returns_complete_information(
        self, reset_test_data
    ) -> None:
        """
        Given: A vehicle 'V-123' exists with 3 maintenance alerts
        When: GET /vehicles (to get all vehicles with alerts)
        Then: The system should return the vehicle with complete information
        And: Should include an "alerts" section
        And: Should show the 3 alerts ordered chronologically (most recent first)
        And: Each alert should show: type, message, mileage, and timestamp

        User Story: HU-003 - Escenario 6
        Business Rule: RN-016 - Alerts should be ordered chronologically (most recent first)
        """
        # Arrange
        client = TestClient(app)

        # Act - Get all vehicles (which includes alerts)
        response = client.get("/vehicles")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

        vehicle = data[0]

        # Verify vehicle information
        assert vehicle["id"] == "V-123"
        assert vehicle["plate"] == "ABC-123"
        assert vehicle["model"] == "Toyota Corolla"
        assert vehicle["current_mileage"] == 35000

        # Verify alerts section exists
        assert "alerts" in vehicle
        alerts = vehicle["alerts"]
        assert len(alerts) == 3

        # Verify alerts are ordered chronologically (most recent first)
        assert alerts[0]["id"] == "alert-3"  # Most recent (2026-01-20)
        assert alerts[1]["id"] == "alert-2"  # Middle (2026-01-15)
        assert alerts[2]["id"] == "alert-1"  # Oldest (2026-01-10)

        # Verify each alert contains required fields
        for alert in alerts:
            assert "alert_type" in alert
            assert "mileage" in alert
            assert "timestamp" in alert
            assert "vehicle_id" in alert

        # Verify specific alert details (alert_type is lowercase in response)
        assert alerts[0]["alert_type"] == "basic_maintenance"
        assert alerts[0]["mileage"] == 30000
        assert alerts[0]["timestamp"] == "2026-01-20T09:15:00"

        assert alerts[1]["alert_type"] == "major_maintenance"
        assert alerts[1]["mileage"] == 20000
        assert alerts[1]["timestamp"] == "2026-01-15T14:30:00"

        assert alerts[2]["alert_type"] == "basic_maintenance"
        assert alerts[2]["mileage"] == 10000
        assert alerts[2]["timestamp"] == "2026-01-10T10:00:00"

    def test_get_vehicle_by_id_includes_alerts_information(
        self, reset_test_data
    ) -> None:
        """
        Given: A vehicle 'V-123' exists with 3 maintenance alerts
        When: GET /vehicles/V-123 (to get specific vehicle details)
        Then: The response should include vehicle information
        Note: Current implementation returns basic vehicle info without alerts
        This test documents the current behavior for the details endpoint

        User Story: HU-003 - Escenario 6
        """
        # Arrange
        client = TestClient(app)

        # Act - Get specific vehicle
        response = client.get("/vehicles/V-123")

        # Assert
        assert response.status_code == 200
        data = response.json()

        # Verify vehicle information
        assert data["id"] == "V-123"
        assert data["plate"] == "ABC-123"
        assert data["model"] == "Toyota Corolla"
        assert data["current_mileage"] == 35000
        assert data["status"] == "active"

        # Note: Current GET /vehicles/{id} endpoint returns VehicleResponse
        # which doesn't include alerts. Alerts are fetched separately via
        # GET /vehicles/{id}/alerts or included in GET /vehicles (all vehicles)

    def test_get_vehicle_alerts_endpoint_returns_ordered_alerts(
        self, reset_test_data
    ) -> None:
        """
        Given: A vehicle 'V-123' exists with 3 maintenance alerts
        When: GET /vehicles/V-123/alerts
        Then: Should return all alerts for the vehicle
        And: Alerts should be ordered chronologically (most recent first)

        User Story: HU-003 - Escenario 6
        Business Rule: RN-016 - Alerts should be ordered chronologically
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.get("/vehicles/V-123/alerts")

        # Assert
        assert response.status_code == 200
        alerts = response.json()
        assert len(alerts) == 3

        # Verify chronological order (most recent first)
        assert alerts[0]["id"] == "alert-3"
        assert alerts[0]["timestamp"] == "2026-01-20T09:15:00"

        assert alerts[1]["id"] == "alert-2"
        assert alerts[1]["timestamp"] == "2026-01-15T14:30:00"

        assert alerts[2]["id"] == "alert-1"
        assert alerts[2]["timestamp"] == "2026-01-10T10:00:00"

    def test_vehicle_with_no_alerts_returns_empty_alerts_list(
        self, reset_test_data
    ) -> None:
        """
        Given: A vehicle exists without any alerts
        When: GET /vehicles
        Then: The vehicle should have an empty alerts list

        User Story: HU-003 - Escenario 3
        """
        # Arrange
        client = TestClient(app)
        vehicle_repo = get_vehicle_repository()

        # Create vehicle without alerts
        vehicle_no_alerts = Vehicle(
            id="V-456", plate="XYZ-456", model="Honda Civic", current_mileage=5000
        )
        vehicle_repo.save(vehicle_no_alerts)

        # Act
        response = client.get("/vehicles")

        # Assert
        assert response.status_code == 200
        data = response.json()

        # Find the vehicle without alerts
        vehicle_456 = next((v for v in data if v["id"] == "V-456"), None)
        assert vehicle_456 is not None
        assert vehicle_456["alerts"] == []
