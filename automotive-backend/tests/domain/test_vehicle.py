"""Tests for Vehicle entity following TDD approach."""

from unittest.mock import Mock

import pytest

from src.domain.entities.vehicle import Vehicle
from src.domain.entities.vehicle_status import VehicleStatus
from src.domain.exceptions.invalid_mileage_exception import InvalidMileageException
from src.domain.exceptions.invalid_model_exception import InvalidModelException
from src.domain.exceptions.invalid_plate_exception import InvalidPlateException
from src.domain.exceptions.invalid_vehicle_id_exception import InvalidVehicleIdException
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
        vehicle = Vehicle(id=vehicle_id, plate=plate, model=model, current_mileage=current_mileage)

        # Assert
        assert vehicle.id == vehicle_id
        assert vehicle.plate == plate
        assert vehicle.model == model
        assert vehicle.current_mileage == current_mileage

    def test_create_vehicle_without_status_defaults_to_active(self) -> None:
        """
        Given: I'm going to register a new vehicle
        When: I register the vehicle without specifying status
        Then: The vehicle should be created with 'active' status by default
        And: It should be available for operations

        User Story: HU-005 - Escenario 4
        Business Rule: RN-026 - Default status is 'active'
        """
        # Arrange
        vehicle_id = "V-123"
        plate = "ABC-123"
        model = "Toyota Corolla"
        current_mileage = 5000

        # Act - Create vehicle without passing status parameter
        vehicle = Vehicle(id=vehicle_id, plate=plate, model=model, current_mileage=current_mileage)

        # Assert
        assert vehicle.status == "active"
        assert vehicle.id == vehicle_id
        assert vehicle.plate == plate
        assert vehicle.model == model
        assert vehicle.current_mileage == current_mileage

    def test_create_vehicle_with_invalid_id_raises_exception(self) -> None:
        """
        Test that invalid vehicle ID format is rejected by domain entity.

        Business Rule: RN-011 - Vehicle ID must follow V-XXX format
        """
        # Arrange
        invalid_ids = ["INVALID", "V-12", "V-1234", "v-001", "123", "", "V-", "V-ABC"]

        # Act & Assert
        for invalid_id in invalid_ids:
            with pytest.raises(InvalidVehicleIdException) as exc_info:
                Vehicle(id=invalid_id, plate="ABC-123", model="Toyota", current_mileage=5000)
            # Verify error message is helpful
            error_msg = str(exc_info.value).lower()
            assert "vehicle_id" in error_msg or "formato" in error_msg or "vacío" in error_msg

    def test_create_vehicle_with_invalid_plate_raises_exception(self) -> None:
        """
        Test that invalid plate format is rejected by domain entity.

        Business Rule: RN-010 - Plate must follow XXX-123 or XXX-1234 format
        """
        # Arrange
        invalid_plates = ["INVALID", "AB-123", "ABC-12345", "abc-123", "", "ABC", "123-ABC"]

        # Act & Assert
        for invalid_plate in invalid_plates:
            with pytest.raises(InvalidPlateException) as exc_info:
                Vehicle(id="V-123", plate=invalid_plate, model="Toyota", current_mileage=5000)
            # Verify error message is helpful
            error_msg = str(exc_info.value).lower()
            assert "placa" in error_msg or "formato" in error_msg or "vacía" in error_msg

    def test_create_vehicle_with_invalid_model_raises_exception(self) -> None:
        """
        Test that invalid model is rejected by domain entity.
        """
        # Arrange
        invalid_models = ["", "   ", "A" * 101]  # Empty, whitespace, too long

        # Act & Assert
        for invalid_model in invalid_models:
            with pytest.raises(InvalidModelException) as exc_info:
                Vehicle(id="V-123", plate="ABC-123", model=invalid_model, current_mileage=5000)
            # Verify error message is helpful
            assert "modelo" in str(exc_info.value).lower() or "vacío" in str(exc_info.value) or "excede" in str(exc_info.value)

    def test_create_vehicle_with_negative_mileage_raises_exception(self) -> None:
        """
        Test that negative mileage is rejected by domain entity.

        Business Rule: RN-002 - Mileage cannot be negative
        """
        # Act & Assert
        with pytest.raises(InvalidMileageException) as exc_info:
            Vehicle(id="V-123", plate="ABC-123", model="Toyota", current_mileage=-100)
        # Verify error message mentions negative
        assert "negativo" in str(exc_info.value).lower()

    def test_create_vehicle_with_excessive_mileage_raises_exception(self) -> None:
        """
        Test that mileage exceeding maximum is rejected by domain entity.

        Business Rule: RN-003 - Mileage cannot exceed 1,000,000 km
        """
        # Act & Assert
        with pytest.raises(InvalidMileageException) as exc_info:
            Vehicle(id="V-123", plate="ABC-123", model="Toyota", current_mileage=1_000_001)
        # Verify error message mentions maximum
        assert "máximo" in str(exc_info.value).lower() or "excede" in str(exc_info.value)


class TestVehicleStatusUpdate:
    """Test cases for Vehicle status updates - HU-005 Escenario 1."""

    def test_update_vehicle_status_to_in_maintenance(self) -> None:
        """
        Test updating vehicle status from active to in_maintenance.

        Given: A vehicle with ID 'V-123' with status 'active'
        When: I update the vehicle status to 'in_maintenance'
        Then: The vehicle status should be 'in_maintenance'
        And: The vehicle should remain visible in the vehicle list
        And: The status change should record the update timestamp

        User Story: HU-005 - Escenario 1
        Business Rule: RN-028 - Status change must record update timestamp

        EXPECTED TO FAIL: Vehicle entity doesn't have update_status() method yet
        """
        # Arrange
        from datetime import datetime

        from src.domain.entities.vehicle import Vehicle
        from src.domain.entities.vehicle_status import VehicleStatus

        vehicle = Vehicle(id="V-123", plate="ABC-123", model="Toyota Corolla", current_mileage=5000, status=VehicleStatus.ACTIVE)

        # Verify initial state
        assert vehicle.status == VehicleStatus.ACTIVE
        assert vehicle.status == "active"

        # Act - Update status to in_maintenance
        timestamp_before = datetime.now()
        vehicle.update_status(VehicleStatus.IN_MAINTENANCE)
        timestamp_after = datetime.now()

        # Assert
        assert vehicle.status == VehicleStatus.IN_MAINTENANCE
        assert vehicle.status == "in_maintenance"

        # Verify timestamp was recorded (RN-028)
        assert hasattr(vehicle, "status_updated_at"), "Vehicle should track status update timestamp"
        assert vehicle.status_updated_at is not None
        assert timestamp_before <= vehicle.status_updated_at <= timestamp_after

        # Verify vehicle is still accessible (not deleted or hidden)
        assert vehicle.id == "V-123"
        assert vehicle.plate == "ABC-123"
        assert vehicle.model == "Toyota Corolla"
        assert vehicle.current_mileage == 5000

    def test_update_vehicle_status_from_active_to_inactive(self) -> None:
        """Test updating vehicle status from active to inactive."""
        # Arrange
        vehicle = Vehicle(id="V-456", plate="XYZ-456", model="Honda Civic", current_mileage=10000, status=VehicleStatus.ACTIVE)

        # Act
        vehicle.update_status(VehicleStatus.INACTIVE)

        # Assert
        assert vehicle.status == VehicleStatus.INACTIVE
        assert vehicle.status == "inactive"

    def test_update_vehicle_status_to_retired(self) -> None:
        """Test updating vehicle status to retired."""
        # Arrange
        vehicle = Vehicle(id="V-789", plate="DEF-789", model="Ford Focus", current_mileage=200000, status=VehicleStatus.ACTIVE)

        # Act
        vehicle.update_status(VehicleStatus.RETIRED)

        # Assert
        assert vehicle.status == VehicleStatus.RETIRED
        assert vehicle.status == "retired"

    def test_update_status_records_timestamp_on_each_change(self) -> None:
        """Test that each status change updates the timestamp."""
        import time

        # Arrange
        vehicle = Vehicle(id="V-100", plate="TST-100", model="Test Vehicle", current_mileage=5000, status=VehicleStatus.ACTIVE)

        # Act - First status change
        vehicle.update_status(VehicleStatus.IN_MAINTENANCE)
        first_timestamp = vehicle.status_updated_at

        time.sleep(0.01)  # Small delay to ensure different timestamps

        # Act - Second status change
        vehicle.update_status(VehicleStatus.ACTIVE)
        second_timestamp = vehicle.status_updated_at

        # Assert
        assert first_timestamp is not None
        assert second_timestamp is not None
        assert second_timestamp > first_timestamp, "Timestamp should update on each status change"

    def test_update_status_with_invalid_value_raises_exception(self) -> None:
        """
        Test that updating vehicle status with invalid value raises exception.

        Given: A vehicle with ID 'V-456' exists
        When: I attempt to update the status to an invalid value 'broken'
        Then: The system should reject the operation
        And: Should raise TypeError
        And: The message should indicate the valid statuses: active, inactive, in_maintenance, retired

        User Story: HU-005 - Escenario 3
        Business Rule: RN-025 - Valid statuses are: active, inactive, in_maintenance, retired
        """
        # Arrange
        vehicle = Vehicle(id="V-456", plate="XYZ-456", model="Honda Civic", current_mileage=10000, status=VehicleStatus.ACTIVE)

        # Act & Assert - Attempt to pass invalid string value
        with pytest.raises(TypeError) as exc_info:
            # This should fail because 'broken' is not a valid VehicleStatus
            vehicle.update_status("broken")

        # Verify error message mentions valid statuses
        error_message = str(exc_info.value).lower()
        # Check that the error message contains information about valid statuses
        assert "vehiclestatus" in error_message or ("active" in error_message and "inactive" in error_message), f"Error message should indicate valid statuses. Got: {exc_info.value}"

    def test_update_status_only_accepts_vehicle_status_enum(self) -> None:
        """
        Test that update_status only accepts VehicleStatus enum values.

        Given: A vehicle exists
        When: I attempt to update status with non-enum values
        Then: The system should reject the operation
        And: Only VehicleStatus enum values should be accepted

        User Story: HU-005 - Escenario 3
        Business Rule: RN-025 - Valid statuses are: active, inactive, in_maintenance, retired
        """
        # Arrange
        vehicle = Vehicle(id="V-789", plate="DEF-789", model="Ford Focus", current_mileage=50000, status=VehicleStatus.ACTIVE)

        # Act & Assert - Test various invalid inputs
        invalid_values = [
            "broken",  # Invalid string
            "ACTIVE",  # Wrong case
            "in-maintenance",  # Wrong format
            123,  # Integer
            None,  # None
            True,  # Boolean
            {"status": "active"},  # Dictionary
        ]

        for invalid_value in invalid_values:
            with pytest.raises(TypeError):
                vehicle.update_status(invalid_value)

        # Verify vehicle status remains unchanged after failed attempts
        assert vehicle.status == VehicleStatus.ACTIVE
        assert vehicle.status == "active"

    def test_all_valid_vehicle_statuses_are_accepted(self) -> None:
        """
        Test that all valid VehicleStatus enum values are accepted.

        Given: A vehicle exists
        When: I update status with each valid VehicleStatus enum value
        Then: All updates should succeed
        And: Valid statuses are: ACTIVE, INACTIVE, IN_MAINTENANCE, RETIRED

        User Story: HU-005 - Escenario 3
        Business Rule: RN-025 - Valid statuses are: active, inactive, in_maintenance, retired
        """
        # Arrange
        vehicle = Vehicle(id="V-999", plate="TST-999", model="Test Vehicle", current_mileage=25000, status=VehicleStatus.ACTIVE)

        # Act & Assert - Test all valid enum values
        valid_statuses = [
            VehicleStatus.ACTIVE,
            VehicleStatus.INACTIVE,
            VehicleStatus.IN_MAINTENANCE,
            VehicleStatus.RETIRED,
        ]

        for valid_status in valid_statuses:
            # Should not raise any exception
            vehicle.update_status(valid_status)
            assert vehicle.status == valid_status
            assert vehicle.status == valid_status.value
            assert vehicle.status_updated_at is not None


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

    def test_update_mileage_on_retired_vehicle_raises_exception(self) -> None:
        """
        Given: A vehicle with status 'retired'
        When: Attempting to update mileage
        Then: System should raise InvalidMileageException
        And: Error message should indicate retired vehicle restriction

        User Story: HU-005 - Escenario 5
        Business Rule: RN-027 - Cannot update mileage of retired vehicles
        """
        # Arrange
        vehicle = Vehicle(id="V-789", plate="DEF-789", model="Ford Focus", current_mileage=200000, status=VehicleStatus.RETIRED)

        # Act & Assert
        with pytest.raises(InvalidMileageException) as exc_info:
            vehicle.update_mileage(205000)

        # Verify error message
        error_message = str(exc_info.value)
        assert "retirado" in error_message.lower() or "retired" in error_message.lower()

    def test_update_mileage_notifies_observers(self):
        """
        This test validates that the logic of 'notifying' about the change in mileage
        now lives in the Domain (Entity), not in the Use Case.
        """
        # Given
        vehicle = Vehicle(id="V-001", plate="ABC-123", model="Test", current_mileage=0)
        mock_observer = Mock()
        vehicle.attach(mock_observer)  # We assume that you implement the Observer pattern in Vehicle.

        # When
        # We simulate what the use case previously did manually.
        vehicle.update_mileage(5000)

        # Then
        # We verified that the domain triggered the notification.
        mock_observer.update.assert_called_once_with("V-001", 5000)
        assert vehicle.current_mileage == 5000


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
        And: Observer SHOULD be notified (Vehicle notifies on every update)
        And: Observer decides whether to generate alerts based on thresholds
        """
        # Arrange
        vehicle = Vehicle(id="V-123", plate="ABC-123", model="Toyota", current_mileage=5000)
        mock_observer = MockObserver()
        vehicle.attach(mock_observer)

        # Act
        vehicle.update_mileage(8000)

        # Assert
        assert vehicle.current_mileage == 8000
        # Observer IS notified (Vehicle notifies on every update)
        assert len(mock_observer.notifications) == 1
        assert mock_observer.notifications[0]["vehicle_id"] == "V-123"
        assert mock_observer.notifications[0]["mileage"] == 8000
        # Note: Whether alerts are generated is the observer's responsibility
