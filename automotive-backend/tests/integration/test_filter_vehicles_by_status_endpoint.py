"""Integration tests for GET /vehicles?status={status} endpoint - HU-005 Escenario 2."""

import pytest
from fastapi.testclient import TestClient

from src.domain.entities.vehicle import Vehicle
from src.domain.entities.vehicle_status import VehicleStatus
from src.web.dependencies import get_vehicle_repository
from src.web.main import app


@pytest.fixture
def reset_test_data():
    """Reset database to known state before each test."""
    from src.infrastructure.database.connection import SessionLocal, engine
    from src.infrastructure.database.models import AlertModel, Base, VehicleModel

    # Recreate all tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Create test vehicles with different statuses
    vehicle_repo = get_vehicle_repository()

    test_vehicles = [
        Vehicle(
            id="V-001",
            plate="ABC-001",
            model="Toyota Corolla",
            current_mileage=50000,
            status=VehicleStatus.ACTIVE,
        ),
        Vehicle(
            id="V-002",
            plate="ABC-002",
            model="Honda Civic",
            current_mileage=60000,
            status=VehicleStatus.ACTIVE,
        ),
        Vehicle(
            id="V-003",
            plate="ABC-003",
            model="Ford Focus",
            current_mileage=70000,
            status=VehicleStatus.IN_MAINTENANCE,
        ),
        Vehicle(
            id="V-004",
            plate="ABC-004",
            model="Mazda 3",
            current_mileage=80000,
            status=VehicleStatus.INACTIVE,
        ),
        Vehicle(
            id="V-005",
            plate="ABC-005",
            model="Chevrolet Cruze",
            current_mileage=150000,
            status=VehicleStatus.RETIRED,
        ),
    ]

    for vehicle in test_vehicles:
        vehicle_repo.save(vehicle)

    yield

    # Cleanup
    session = SessionLocal()
    session.query(AlertModel).delete()
    session.query(VehicleModel).delete()
    session.commit()
    session.close()


class TestFilterVehiclesByStatusEndpoint:
    """
    Integration tests for GET /vehicles?status={status} endpoint.

    Implements HU-005 Escenario 2: Filter vehicles by status.

    EXPECTED TO FAIL: Endpoint doesn't exist yet.
    """

    def test_endpoint_exists_and_accepts_status_query_parameter(self, reset_test_data):
        """
        Test that GET /vehicles?status={status} endpoint exists.

        EXPECTED TO FAIL: Endpoint not implemented yet.

        Given: Multiple vehicles exist with different statuses
        When: GET /vehicles?status=active
        Then: Should return 200 OK (not 404 or 422)
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.get("/vehicles?status=active")

        # Assert
        assert response.status_code == 200, (
            "Endpoint should exist and return 200 OK. "
            f"Got status code: {response.status_code}"
        )

    def test_filter_vehicles_by_active_status_gherkin_scenario(self, reset_test_data):
        """
        Test the exact Gherkin scenario from HU-005 Escenario 2.

        Given: 5 vehicles in the system with different statuses
          | ID    | Status          |
          | V-001 | active          |
          | V-002 | active          |
          | V-003 | in_maintenance  |
          | V-004 | inactive        |
          | V-005 | retired         |
        When: GET /vehicles?status=active
        Then: System should return 2 vehicles
        And: Both vehicles should have status 'active'

        EXPECTED TO FAIL: Endpoint not implemented yet.
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.get("/vehicles?status=active")

        # Assert
        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list), "Response should be a list"
        assert len(data) == 2, "Sistema debe devolver 2 vehículos"

        # Verify both vehicles have active status
        for vehicle in data:
            assert vehicle["status"] == "active", "Ambos vehículos deben tener estado 'active'"

        # Verify correct vehicles are returned
        vehicle_ids = [v["id"] for v in data]
        assert "V-001" in vehicle_ids
        assert "V-002" in vehicle_ids

    def test_filter_vehicles_by_in_maintenance_status(self, reset_test_data):
        """
        Test filtering vehicles with IN_MAINTENANCE status.

        EXPECTED TO FAIL: Endpoint not implemented yet.

        Given: 5 vehicles exist, 1 with status 'in_maintenance'
        When: GET /vehicles?status=in_maintenance
        Then: Should return 1 vehicle
        And: Vehicle should have status 'in_maintenance'
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.get("/vehicles?status=in_maintenance")

        # Assert
        assert response.status_code == 200
        data = response.json()

        assert len(data) == 1, "Should return 1 vehicle in maintenance"
        assert data[0]["id"] == "V-003"
        assert data[0]["status"] == "in_maintenance"

    def test_filter_vehicles_by_inactive_status(self, reset_test_data):
        """
        Test filtering vehicles with INACTIVE status.

        EXPECTED TO FAIL: Endpoint not implemented yet.

        Given: 5 vehicles exist, 1 with status 'inactive'
        When: GET /vehicles?status=inactive
        Then: Should return 1 vehicle
        And: Vehicle should have status 'inactive'
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.get("/vehicles?status=inactive")

        # Assert
        assert response.status_code == 200
        data = response.json()

        assert len(data) == 1, "Should return 1 inactive vehicle"
        assert data[0]["id"] == "V-004"
        assert data[0]["status"] == "inactive"

    def test_filter_vehicles_by_retired_status(self, reset_test_data):
        """
        Test filtering vehicles with RETIRED status.

        EXPECTED TO FAIL: Endpoint not implemented yet.

        Given: 5 vehicles exist, 1 with status 'retired'
        When: GET /vehicles?status=retired
        Then: Should return 1 vehicle
        And: Vehicle should have status 'retired'
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.get("/vehicles?status=retired")

        # Assert
        assert response.status_code == 200
        data = response.json()

        assert len(data) == 1, "Should return 1 retired vehicle"
        assert data[0]["id"] == "V-005"
        assert data[0]["status"] == "retired"

    def test_filter_returns_empty_list_when_no_vehicles_match(self, reset_test_data):
        """
        Test that filtering returns empty list when no vehicles have the status.

        EXPECTED TO FAIL: Endpoint not implemented yet.

        Given: No vehicles with status 'retired' exist (after deleting V-005)
        When: GET /vehicles?status=retired
        Then: Should return 200 OK with empty list
        """
        # Arrange
        client = TestClient(app)
        # Delete the retired vehicle
        client.delete("/vehicles/V-005")

        # Act
        response = client.get("/vehicles?status=retired")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data == [], "Should return empty list"

    def test_filter_with_invalid_status_returns_400(self, reset_test_data):
        """
        Test that invalid status value returns 400 Bad Request.

        EXPECTED TO FAIL: Endpoint not implemented yet.

        Given: Multiple vehicles exist
        When: GET /vehicles?status=broken (invalid status)
        Then: Should return 400 Bad Request
        And: Error message should indicate valid statuses

        Business Rule: RN-025 - Valid statuses are: active, inactive, in_maintenance, retired
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.get("/vehicles?status=broken")

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        error_message = data["detail"].lower()

        # Verify error message mentions valid statuses
        assert "active" in error_message or "válido" in error_message or "invalid" in error_message

    def test_filter_response_includes_all_vehicle_fields(self, reset_test_data):
        """
        Test that filtered response includes all vehicle fields.

        EXPECTED TO FAIL: Endpoint not implemented yet.

        Given: Vehicles exist with active status
        When: GET /vehicles?status=active
        Then: Each vehicle should include: id, plate, model, current_mileage, status
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.get("/vehicles?status=active")

        # Assert
        assert response.status_code == 200
        data = response.json()

        for vehicle in data:
            assert "id" in vehicle
            assert "plate" in vehicle
            assert "model" in vehicle
            assert "current_mileage" in vehicle
            assert "status" in vehicle

    def test_filter_without_status_parameter_returns_all_vehicles(self, reset_test_data):
        """
        Test that GET /vehicles without status parameter returns all vehicles.

        EXPECTED BEHAVIOR: Should maintain backward compatibility.

        Given: 5 vehicles exist with different statuses
        When: GET /vehicles (no status parameter)
        Then: Should return all 5 vehicles
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.get("/vehicles")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5, "Should return all vehicles when no filter is applied"

    def test_filter_is_case_insensitive(self, reset_test_data):
        """
        Test that status filter is case-insensitive.

        EXPECTED TO FAIL: Endpoint not implemented yet.

        Given: Vehicles exist with active status
        When: GET /vehicles?status=ACTIVE (uppercase)
        Then: Should return same results as lowercase
        """
        # Arrange
        client = TestClient(app)

        # Act
        response_lower = client.get("/vehicles?status=active")
        response_upper = client.get("/vehicles?status=ACTIVE")

        # Assert
        assert response_lower.status_code == 200
        assert response_upper.status_code == 200

        data_lower = response_lower.json()
        data_upper = response_upper.json()

        assert len(data_lower) == len(data_upper), "Case should not matter"
        assert data_lower == data_upper, "Results should be identical"

    def test_filter_response_does_not_include_alerts(self, reset_test_data):
        """
        Test that filtered response includes empty alerts list (for consistency with response model).

        Note: We use the same VehicleWithAlertsResponse model but return empty alerts
        for filtered results to maintain API consistency.

        Given: Vehicles exist with active status
        When: GET /vehicles?status=active
        Then: Response should include alerts field but it should be empty
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.get("/vehicles?status=active")

        # Assert
        assert response.status_code == 200
        data = response.json()

        for vehicle in data:
            assert "alerts" in vehicle, "Response should include alerts field for consistency"
            assert vehicle["alerts"] == [], "Filtered response should have empty alerts list"
