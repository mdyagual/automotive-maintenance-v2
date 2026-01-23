"""Integration tests for vehicle status update endpoint - HU-005."""

import pytest
from fastapi.testclient import TestClient

from src.domain.entities.vehicle import Vehicle
from src.domain.entities.vehicle_status import VehicleStatus
from src.web.dependencies import get_vehicle_repository
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

    # Create test vehicle V-123 with active status
    vehicle_repo = get_vehicle_repository()
    test_vehicle = Vehicle(
        id="V-123",
        plate="ABC-123",
        model="Toyota Corolla",
        current_mileage=5000,
        status=VehicleStatus.ACTIVE
    )
    vehicle_repo.save(test_vehicle)

    yield

    # Cleanup after test
    session.query(AlertModel).delete()
    session.query(VehicleModel).delete()
    session.commit()
    session.close()


class TestUpdateVehicleStatusEndpoint:
    """Integration tests for PUT /vehicles/{id}/status endpoint."""

    def test_update_status_to_in_maintenance_successfully(self) -> None:
        """
        Given: A vehicle exists with status 'active'
        When: PUT /vehicles/{id}/status with 'in_maintenance'
        Then: Should return 200 OK and update status

        Business Rules: RN-025, RN-028
        User Story: HU-005 Escenario 1
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.put(
            "/vehicles/V-123/status",
            json={"new_status": "in_maintenance"}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "V-123"
        assert data["status"] == "in_maintenance"

    def test_update_status_to_retired_successfully(self) -> None:
        """
        Given: A vehicle exists with status 'active'
        When: PUT /vehicles/{id}/status with 'retired'
        Then: Should return 200 OK and update status to retired

        Business Rules: RN-025, RN-026
        User Story: HU-005 Escenario 3
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.put(
            "/vehicles/V-123/status",
            json={"new_status": "retired"}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "V-123"
        assert data["status"] == "retired"

    def test_update_status_to_inactive_successfully(self) -> None:
        """
        Given: A vehicle exists with status 'active'
        When: PUT /vehicles/{id}/status with 'inactive'
        Then: Should return 200 OK and update status to inactive

        Business Rules: RN-025
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.put(
            "/vehicles/V-123/status",
            json={"new_status": "inactive"}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "V-123"
        assert data["status"] == "inactive"

    def test_update_status_to_active_successfully(self) -> None:
        """
        Given: A vehicle exists with status 'inactive'
        When: PUT /vehicles/{id}/status with 'active'
        Then: Should return 200 OK and update status to active

        Business Rules: RN-025
        """
        # Arrange
        client = TestClient(app)

        # First set to inactive
        client.put("/vehicles/V-123/status", json={"new_status": "inactive"})

        # Act - change back to active
        response = client.put(
            "/vehicles/V-123/status",
            json={"new_status": "active"}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "V-123"
        assert data["status"] == "active"

    def test_update_status_with_invalid_status_returns_400(self) -> None:
        """
        Given: A vehicle exists
        When: PUT /vehicles/{id}/status with invalid status 'invalid_status'
        Then: Should return 400 Bad Request

        Business Rules: RN-025
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.put(
            "/vehicles/V-123/status",
            json={"new_status": "invalid_status"}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Estado inválido" in data["detail"]

    def test_update_status_with_nonexistent_vehicle_returns_404(self) -> None:
        """
        Given: A vehicle does not exist
        When: PUT /vehicles/{id}/status
        Then: Should return 404 Not Found
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.put(
            "/vehicles/V-999/status",
            json={"new_status": "inactive"}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_update_status_case_insensitive(self) -> None:
        """
        Given: A vehicle exists with status 'active'
        When: PUT /vehicles/{id}/status with uppercase 'IN_MAINTENANCE'
        Then: Should accept and convert to lowercase
        And: Should return 200 OK with status 'in_maintenance'
        """
        # Arrange
        client = TestClient(app)

        # Act
        response = client.put(
            "/vehicles/V-123/status",
            json={"new_status": "IN_MAINTENANCE"}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "in_maintenance"

    def test_update_status_persists_in_database(self) -> None:
        """
        Given: A vehicle exists with status 'active'
        When: PUT /vehicles/{id}/status with 'in_maintenance'
        Then: Status should be persisted in database
        And: Subsequent GET should return updated status
        """
        # Arrange
        client = TestClient(app)

        # Act - Update status
        update_response = client.put(
            "/vehicles/V-123/status",
            json={"new_status": "in_maintenance"}
        )

        # Assert - Verify update response
        assert update_response.status_code == 200

        # Act - Get vehicle to verify persistence
        get_response = client.get("/vehicles/V-123")

        # Assert - Verify persisted status
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["status"] == "in_maintenance"
