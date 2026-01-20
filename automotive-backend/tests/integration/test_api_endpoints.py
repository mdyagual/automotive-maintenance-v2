"""Integration tests for FastAPI endpoints."""

from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from src.domain.entities.maintenance_alert import AlertType, MaintenanceAlert
from src.domain.entities.vehicle import Vehicle
from src.web.dependencies import get_alert_repository, get_vehicle_repository
from src.web.main import app


@pytest.fixture(autouse=True)
def reset_test_data():
    """Reset database to known state before each test."""
    from src.infrastructure.database.connection import SessionLocal
    from src.infrastructure.database.models import AlertModel, VehicleModel

    # Get session
    session = SessionLocal()

    # Clean all data
    session.query(AlertModel).delete()
    session.query(VehicleModel).delete()
    session.commit()

    # Create test vehicle V-123
    vehicle_repo = get_vehicle_repository()
    test_vehicle = Vehicle(
        id="V-123", plate="ABC-123", model="Toyota Corolla", current_mileage=5000
    )
    vehicle_repo.save(test_vehicle)

    yield

    # Cleanup after test - remove test data created during test
    session.query(AlertModel).delete()
    session.query(VehicleModel).delete()
    session.commit()
    session.close()


class TestVehicleEndpoints:
    """Integration tests for vehicle endpoints."""

    def test_update_vehicle_mileage_successfully(self) -> None:
        """
        Given: A vehicle exists with 5,000 km
        When: PUT /vehicles/{id}/mileage with 8,000 km
        Then: Should return 200 OK and update mileage
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.put(
            "/vehicles/V-123/mileage",
            json={"new_mileage": 8000}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "V-123"
        assert data["current_mileage"] == 8000

    def test_update_vehicle_mileage_with_invalid_value_returns_400(self) -> None:
        """
        Given: A vehicle exists with 5,000 km
        When: PUT /vehicles/{id}/mileage with 4,000 km (invalid)
        Then: Should return 400 Bad Request
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.put(
            "/vehicles/V-123/mileage",
            json={"new_mileage": 4000}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_update_vehicle_mileage_not_found_returns_404(self) -> None:
        """
        Given: A vehicle does not exist
        When: PUT /vehicles/{id}/mileage
        Then: Should return 404 Not Found
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.put(
            "/vehicles/V-999/mileage",
            json={"new_mileage": 10000}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_get_vehicle_by_id_successfully(self) -> None:
        """
        Given: A vehicle exists
        When: GET /vehicles/{id}
        Then: Should return 200 OK with vehicle data
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.get("/vehicles/V-123")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "V-123"
        assert "current_mileage" in data

    def test_get_alerts_for_vehicle(self) -> None:
        """
        Given: Alerts exist for a vehicle
        When: GET /vehicles/{id}/alerts
        Then: Should return list of alerts
        """
        # Arrange
        client = TestClient(app)

        # First trigger an alert by updating mileage
        client.put("/vehicles/V-123/mileage", json={"new_mileage": 10001})

        # Act
        response = client.get("/vehicles/V-123/alerts")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_create_new_vehicle_successfully(self) -> None:
        """
        Given: No vehicle with ID 'V-999' exists
        When: POST /vehicles with valid data
        Then: Should return 201 Created with vehicle data
        """
        # Arrange
        client = TestClient(app)
        new_vehicle_data = {
            "id": "V-999",
            "plate": "NEW-999",
            "model": "Mazda 3",
            "initial_mileage": 0,
        }

        # Act
        response = client.post("/vehicles", json=new_vehicle_data)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == "V-999"
        assert data["plate"] == "NEW-999"
        assert data["model"] == "Mazda 3"
        assert data["current_mileage"] == 0

    def test_create_vehicle_with_duplicate_id_returns_400(self) -> None:
        """
        Given: A vehicle with ID 'V-123' already exists
        When: POST /vehicles with same ID
        Then: Should return 400 Bad Request
        """
        # Arrange
        client = TestClient(app)
        duplicate_vehicle = {
            "id": "V-123",
            "plate": "DUP-123",
            "model": "Duplicate Car",
            "initial_mileage": 0,
        }

        # Act
        response = client.post("/vehicles", json=duplicate_vehicle)

        # Assert
        assert response.status_code == 400
        assert "Ya existe un vehículo con ID V-123" in response.json()["detail"]

    def test_get_all_vehicles_successfully(self) -> None:
        """
        Given: Multiple vehicles exist in the database
        When: GET /vehicles
        Then: Should return 200 OK with all vehicles and their alerts
        """
        # Arrange
        client = TestClient(app)
        vehicle_repo = get_vehicle_repository()

        # Create additional vehicles
        vehicle2 = Vehicle(
            id="V-456", plate="XYZ-456", model="Honda Civic", current_mileage=25000
        )
        vehicle3 = Vehicle(
            id="V-789", plate="DEF-789", model="Mazda 3", current_mileage=5000
        )
        vehicle_repo.save(vehicle2)
        vehicle_repo.save(vehicle3)

        # Act
        response = client.get("/vehicles")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert isinstance(data, list)

        # Verify structure of each vehicle
        for vehicle_data in data:
            assert "id" in vehicle_data
            assert "plate" in vehicle_data
            assert "model" in vehicle_data
            assert "current_mileage" in vehicle_data
            assert "alerts" in vehicle_data
            assert isinstance(vehicle_data["alerts"], list)

    def test_get_all_vehicles_returns_empty_list_when_no_vehicles(self) -> None:
        """
        Given: No vehicles in database (clean state)
        When: GET /vehicles
        Then: Should return 200 OK with empty list
        """
        # Arrange
        client = TestClient(app)
        from src.infrastructure.database.connection import SessionLocal
        from src.infrastructure.database.models import AlertModel, VehicleModel

        # Clean all vehicles (including V-123 from fixture)
        session = SessionLocal()
        session.query(AlertModel).delete()
        session.query(VehicleModel).delete()
        session.commit()
        session.close()

        # Act
        response = client.get("/vehicles")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data == []
        assert isinstance(data, list)

    def test_get_all_vehicles_includes_alerts_ordered_by_timestamp(self) -> None:
        """
        Given: Vehicles with multiple alerts exist
        When: GET /vehicles
        Then: Should return vehicles with alerts ordered by timestamp descending
        """
        # Arrange
        client = TestClient(app)
        alert_repo = get_alert_repository()

        # Create alerts for V-123 in different timestamps
        alert1 = MaintenanceAlert(
            id="alert-1",
            vehicle_id="V-123",
            alert_type=AlertType.BASIC_MAINTENANCE,
            mileage=10000,
            timestamp=datetime(2026, 1, 1, 10, 0, 0),
        )
        alert2 = MaintenanceAlert(
            id="alert-2",
            vehicle_id="V-123",
            alert_type=AlertType.BASIC_MAINTENANCE,
            mileage=20000,
            timestamp=datetime(2026, 1, 5, 10, 0, 0),
        )
        alert_repo.save(alert1)
        alert_repo.save(alert2)

        # Act
        response = client.get("/vehicles")

        # Assert
        assert response.status_code == 200
        data = response.json()
        vehicle_123 = next(v for v in data if v["id"] == "V-123")

        assert len(vehicle_123["alerts"]) == 2
        # Most recent first (timestamp desc)
        assert vehicle_123["alerts"][0]["id"] == "alert-2"
        assert vehicle_123["alerts"][1]["id"] == "alert-1"

    def test_delete_vehicle_successfully(self) -> None:
        """
        Given: A vehicle V-123 exists in the system
        When: DELETE /vehicles/V-123
        Then: Should return 204 No Content
        And: Vehicle should be deleted from database
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.delete("/vehicles/V-123")

        # Assert
        assert response.status_code == 204
        assert response.text == ""

        # Verify vehicle was deleted
        get_response = client.get("/vehicles/V-123")
        assert get_response.status_code == 404

    def test_delete_nonexistent_vehicle_returns_404(self) -> None:
        """
        Given: No vehicle with ID V-NONEXISTENT exists
        When: DELETE /vehicles/V-NONEXISTENT
        Then: Should return 404 Not Found with error message
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.delete("/vehicles/V-NONEXISTENT")

        # Assert
        assert response.status_code == 404
        assert "Vehículo con ID V-NONEXISTENT no encontrado" in response.json()["detail"]

    def test_delete_vehicle_cascades_alerts(self) -> None:
        """
        Given: A vehicle V-777 exists with multiple alerts
        When: DELETE /vehicles/V-777
        Then: Should return 204 No Content
        And: All associated alerts should be deleted (cascade)
        And: No orphan alerts should remain in database
        """
        # Arrange
        client = TestClient(app)
        vehicle_repo = get_vehicle_repository()
        alert_repo = get_alert_repository()

        # Create vehicle V-777
        vehicle = Vehicle(
            id="V-777", plate="XYZ-777", model="Honda Civic", current_mileage=30000
        )
        vehicle_repo.save(vehicle)

        # Create multiple alerts for V-777
        alert1 = MaintenanceAlert(
            id="alert-777-1",
            vehicle_id="V-777",
            alert_type=AlertType.BASIC_MAINTENANCE,
            mileage=10000,
            timestamp=datetime.now(),
        )
        alert2 = MaintenanceAlert(
            id="alert-777-2",
            vehicle_id="V-777",
            alert_type=AlertType.MAJOR_MAINTENANCE,
            mileage=50000,
            timestamp=datetime.now(),
        )
        alert3 = MaintenanceAlert(
            id="alert-777-3",
            vehicle_id="V-777",
            alert_type=AlertType.CRITICAL_THRESHOLD,
            mileage=100000,
            timestamp=datetime.now(),
        )
        alert_repo.save(alert1)
        alert_repo.save(alert2)
        alert_repo.save(alert3)

        # Verify alerts exist before deletion
        alerts_before = alert_repo.get_by_vehicle_id("V-777")
        assert len(alerts_before) == 3

        # Act
        response = client.delete("/vehicles/V-777")

        # Assert
        assert response.status_code == 204

        # Verify vehicle deleted
        get_response = client.get("/vehicles/V-777")
        assert get_response.status_code == 404

        # Verify alerts cascaded (deleted automatically)
        alerts_after = alert_repo.get_by_vehicle_id("V-777")
        assert len(alerts_after) == 0, "No orphan alerts should remain after vehicle deletion"
