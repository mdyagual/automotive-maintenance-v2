"""Tests for Vehicle entity following TDD approach."""
import pytest

from src.domain.entities.vehicle import Vehicle
from src.domain.exceptions.invalid_mileage_exception import InvalidMileageException
from src.domain.ports.observer import Observer


class TestVehicleCreation:
    """Test cases for Vehicle creation."""

    def test_create_vehicle_with_valid_data(self) -> None:
        """
        Given: Valid vehicle data
        When: Creating a new Vehicle instance
        Then: Vehicle should be created with correct attributes
        """
        # Arrange
        vehicle_id = "V-123"
        plate = "ABC-123"
        model = "Toyota Corolla"
        current_mileage = 5000

        # Act
        vehicle = Vehicle(
            id=vehicle_id,
            plate=plate,
            model=model,
            current_mileage=current_mileage
        )

        # Assert
        assert vehicle.id == vehicle_id
        assert vehicle.plate == plate
        assert vehicle.model == model
        assert vehicle.current_mileage == current_mileage


class TestVehicleMileageUpdate:
    """Test cases for Vehicle mileage update - HU-001 Escenario 2."""

    def test_update_mileage_with_lower_value_raises_exception(self) -> None:
        """
        Given: A vehicle with current mileage of 5,000 km
        When: Attempting to update mileage to 4,000 km (lower value)
        Then: System should raise InvalidMileageException
        """
        # Arrange
        vehicle = Vehicle(id="V-123", plate="ABC-123", model="Toyota", current_mileage=5000)

        # Act & Assert
        with pytest.raises(InvalidMileageException):
            vehicle.update_mileage(4000)

    def test_update_mileage_with_negative_value_raises_exception(self) -> None:
        """
        Given: A vehicle with current mileage
        When: Attempting to update mileage to negative value (RN-002)
        Then: System should raise InvalidMileageException
        """
        # Arrange
        vehicle = Vehicle(id="V-123", plate="ABC-123", model="Toyota", current_mileage=5000)

        # Act & Assert
        with pytest.raises(InvalidMileageException):
            vehicle.update_mileage(-100)

    def test_update_mileage_exceeding_limit_raises_exception(self) -> None:
        """
        Given: A vehicle with current mileage
        When: Attempting to update mileage exceeding 1,000,000 km (RN-003)
        Then: System should raise InvalidMileageException
        """
        # Arrange
        vehicle = Vehicle(id="V-123", plate="ABC-123", model="Toyota", current_mileage=500000)

        # Act & Assert
        with pytest.raises(InvalidMileageException):
            vehicle.update_mileage(1000001)

    def test_update_mileage_with_excessive_increment_raises_exception(self) -> None:
        """
        Given: A vehicle with current mileage
        When: Attempting to update with increment > 50,000 km (RN-004)
        Then: System should raise InvalidMileageException
        """
        # Arrange
        vehicle = Vehicle(id="V-123", plate="ABC-123", model="Toyota", current_mileage=5000)

        # Act & Assert
        with pytest.raises(InvalidMileageException):
            vehicle.update_mileage(60000)  # Increment of 55,000 km


class MockObserver(Observer):
    """Mock observer for testing."""

    def __init__(self) -> None:
        self.notifications = []

    def update(self, vehicle_id: str, mileage: int) -> None:
        """Record notification."""
        self.notifications.append({"vehicle_id": vehicle_id, "mileage": mileage})


class TestVehicleObserverPattern:
    """Test cases for Vehicle Observer Pattern - HU-001 Escenario 1."""

    def test_update_mileage_to_10000_generates_alert(self) -> None:
        """
        Given: A vehicle with 5,000 km and a registered observer
        And: Maintenance rule every 10,000 km
        When: Updating mileage to 10,001 km
        Then: Mileage should be updated to 10,001 km
        And: Observer should be notified automatically
        """
        # Arrange
        vehicle = Vehicle(id="V-123", plate="ABC-123", model="Toyota", current_mileage=5000)
        mock_observer = MockObserver()
        vehicle.attach(mock_observer)

        # Act
        vehicle.update_mileage(10001)

        # Assert
        assert vehicle.current_mileage == 10001
        assert len(mock_observer.notifications) == 1
        assert mock_observer.notifications[0]["vehicle_id"] == "V-123"
        assert mock_observer.notifications[0]["mileage"] == 10001

    def test_update_mileage_without_crossing_threshold_no_alert(self) -> None:
        """
        Given: A vehicle with 5,000 km and a registered observer
        When: Updating mileage to 8,000 km (not crossing threshold)
        Then: Mileage should be updated to 8,000 km
        And: Observer should NOT be notified
        """
        # Arrange
        vehicle = Vehicle(id="V-123", plate="ABC-123", model="Toyota", current_mileage=5000)
        mock_observer = MockObserver()
        vehicle.attach(mock_observer)

        # Act
        vehicle.update_mileage(8000)

        # Assert
        assert vehicle.current_mileage == 8000
        assert len(mock_observer.notifications) == 0
