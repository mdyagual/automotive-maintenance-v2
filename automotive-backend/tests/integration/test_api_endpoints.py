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
    from src.infrastructure.database.connection import SessionLocal, engine
    from src.infrastructure.database.models import AlertModel, Base, VehicleModel

    # Recreate all tables to ensure schema is up to date
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Get session
    session = SessionLocal()

    # Create test vehicle V-123
    vehicle_repo = get_vehicle_repository()
    test_vehicle = Vehicle(id="V-123", plate="ABC-123", model="Toyota Corolla", current_mileage=5000)
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
        response = client.put("/vehicles/V-123/mileage", json={"new_mileage": 8000})

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
        response = client.put("/vehicles/V-123/mileage", json={"new_mileage": 4000})

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
        response = client.put("/vehicles/V-999/mileage", json={"new_mileage": 10000})

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
        vehicle2 = Vehicle(id="V-456", plate="XYZ-456", model="Honda Civic", current_mileage=25000)
        vehicle3 = Vehicle(id="V-789", plate="DEF-789", model="Mazda 3", current_mileage=5000)
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
        response = client.delete("/vehicles/V-999")

        # Assert
        assert response.status_code == 404
        assert "Vehículo con ID V-999 no encontrado" in response.json()["detail"]

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
        vehicle = Vehicle(id="V-777", plate="XYZ-777", model="Honda Civic", current_mileage=30000)
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

    def test_get_vehicle_includes_status_field(self) -> None:
        """
        Test that GET /vehicles/{id} includes status field.

        Given: A vehicle V-123 exists in the system
        When: GET /vehicles/V-123
        Then: Response must include status field for HU-005
        And: Status should be 'active' by default

        User Story: HU-005 - Escenario 1
        Business Rule: RN-026 - Default status is 'active'
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.get("/vehicles/V-123")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "status" in data, "Response must include status field for HU-005"
        assert data["status"] == "active"

    def test_create_vehicle_returns_status_field(self) -> None:
        """
        Test that POST /vehicles returns status field.

        Given: I'm registering a new vehicle
        When: POST /vehicles with valid data
        Then: Response must include status field
        And: Status should be 'active' by default

        User Story: HU-005 - Escenario 4
        Business Rule: RN-026 - Default status is 'active'
        """
        # Arrange
        client = TestClient(app)
        new_vehicle_data = {
            "id": "V-888",
            "plate": "NEW-888",
            "model": "Test Vehicle",
            "initial_mileage": 0,
        }

        # Act
        response = client.post("/vehicles", json=new_vehicle_data)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert "status" in data, "Response must include status field for HU-005"
        assert data["status"] == "active"

    def test_update_mileage_returns_status_field(self) -> None:
        """
        Test that PUT /vehicles/{id}/mileage returns status field.

        Given: A vehicle V-123 exists
        When: PUT /vehicles/V-123/mileage with new mileage
        Then: Response must include status field

        User Story: HU-005 - Escenario 1
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.put("/vehicles/V-123/mileage", json={"new_mileage": 8000})

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "status" in data, "Response must include status field for HU-005"
        assert data["status"] == "active"

    def test_get_all_vehicles_includes_status_field(self) -> None:
        """
        Test that GET /vehicles includes status field for all vehicles.

        Given: Multiple vehicles exist in the system
        When: GET /vehicles
        Then: Each vehicle must include status field

        User Story: HU-005 - Escenario 2
        Business Rule: RN-029 - Vehicles can be filtered by status
        """
        # Arrange
        client = TestClient(app)
        vehicle_repo = get_vehicle_repository()

        # Create additional vehicles
        vehicle2 = Vehicle(id="V-456", plate="XYZ-456", model="Honda Civic", current_mileage=25000)
        vehicle_repo.save(vehicle2)

        # Act
        response = client.get("/vehicles")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2

        # Verify all vehicles have status field
        for vehicle_data in data:
            assert "status" in vehicle_data, f"Vehicle {vehicle_data['id']} must include status field for HU-005"
            assert vehicle_data["status"] in ["active", "inactive", "in_maintenance", "retired"], f"Status must be a valid value, got: {vehicle_data['status']}"

    def test_search_vehicle_by_exact_plate_returns_one_vehicle(self) -> None:
        """
        Test searching vehicle by exact plate match.

        Given: Vehicles exist in the system with plates ABC-123, XYZ-456, ABC-789
        When: GET /vehicles/search?plate=ABC-123
        Then: The system should return 1 vehicle
        And: The vehicle should have plate "ABC-123"
        And: The vehicle should include alerts (RN-034)

        User Story: HU-006 - Escenario 1
        Business Rule: RN-031 - Search must be case-insensitive
        Business Rule: RN-034 - Search results must include alerts
        """
        # Arrange
        client = TestClient(app)
        vehicle_repo = get_vehicle_repository()

        # Create additional test vehicles
        vehicle2 = Vehicle(id="V-002", plate="XYZ-456", model="Honda Civic", current_mileage=10000)
        vehicle3 = Vehicle(id="V-003", plate="ABC-789", model="Mazda 3", current_mileage=15000)
        vehicle_repo.save(vehicle2)
        vehicle_repo.save(vehicle3)

        # Act
        response = client.get("/vehicles/search?plate=ABC-123")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "V-123"
        assert data["plate"] == "ABC-123"
        assert data["model"] == "Toyota Corolla"
        assert data["current_mileage"] == 5000
        # Verify alerts are included (RN-034)
        assert "alerts" in data
        assert isinstance(data["alerts"], list)

    def test_search_vehicle_by_plate_case_insensitive(self) -> None:
        """
        Test that search is case-insensitive.

        Given: A vehicle exists with plate "ABC-123"
        When: GET /vehicles/search?plate=abc-123 (lowercase)
        Then: The system should return the vehicle with plate "ABC-123"
        And: The vehicle should include alerts (RN-034)

        User Story: HU-006 - Escenario 4
        Business Rule: RN-031 - Search must be case-insensitive
        Business Rule: RN-034 - Search results must include alerts
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.get("/vehicles/search?plate=abc-123")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["plate"] == "ABC-123"
        assert data["id"] == "V-123"
        # Verify alerts are included (RN-034)
        assert "alerts" in data
        assert isinstance(data["alerts"], list)

    def test_search_vehicle_by_nonexistent_plate_returns_404(self) -> None:
        """
        Test searching for a vehicle with a plate that doesn't exist.

        Given: Vehicles exist in the system
        When: GET /vehicles/search?plate=ZZZ-999
        Then: The system should return 404 Not Found

        User Story: HU-006 - Escenario 3
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.get("/vehicles/search?plate=ZZZ-999")

        # Assert
        assert response.status_code == 404
        assert "ZZZ-999" in response.json()["detail"]

    def test_search_vehicle_with_invalid_plate_format_returns_400(self) -> None:
        """
        Test that searching with invalid complete plate format returns 404 (no results).

        Given: I'm searching for a vehicle
        When: GET /vehicles/search?plate=INVALID
        Then: The system should return 404 Not Found (no vehicles match)

        Note: Partial searches are now allowed, so this returns 404 instead of 400
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.get("/vehicles/search?plate=INVALID")

        # Assert - Should return 404 since no vehicles match "INVALID"
        assert response.status_code == 404

    def test_search_vehicle_by_partial_plate_returns_multiple_vehicles(self) -> None:
        """
        Test searching vehicles by partial plate match.

        Given: Vehicles exist with plates ABC-123, XYZ-456, ABC-789
        When: GET /vehicles/search?plate=ABC
        Then: The system should return 2 vehicles
        And: Both vehicles should have plates containing "ABC"
        And: Each vehicle should include alerts (RN-034)

        User Story: HU-006 - Escenario 2
        Business Rule: RN-032 - Search must support partial matches
        Business Rule: RN-034 - Search results must include alerts
        """
        # Arrange
        client = TestClient(app)
        vehicle_repo = get_vehicle_repository()

        # Create additional test vehicles
        vehicle2 = Vehicle(id="V-002", plate="XYZ-456", model="Honda Civic", current_mileage=10000)
        vehicle3 = Vehicle(id="V-003", plate="ABC-789", model="Mazda 3", current_mileage=15000)
        vehicle_repo.save(vehicle2)
        vehicle_repo.save(vehicle3)

        # Act
        response = client.get("/vehicles/search?plate=ABC")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2

        # Verify both vehicles have plates containing "ABC"
        plates = [v["plate"] for v in data]
        assert "ABC-123" in plates
        assert "ABC-789" in plates

        # Verify each vehicle includes alerts (RN-034)
        for vehicle in data:
            assert "alerts" in vehicle
            assert isinstance(vehicle["alerts"], list)

        # Verify structure
        for vehicle in data:
            assert "ABC" in vehicle["plate"]
            assert "id" in vehicle
            assert "model" in vehicle
            assert "current_mileage" in vehicle
            assert "status" in vehicle
