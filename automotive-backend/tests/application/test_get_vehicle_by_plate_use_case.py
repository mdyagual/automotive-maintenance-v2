"""Tests for GetVehicleByPlateUseCase - Application layer."""

import pytest

from src.application.dtos.vehicle_dtos import VehicleDTO
from src.application.use_cases.get_vehicle_by_plate_use_case import GetVehicleByPlateUseCase
from src.domain.entities.vehicle import Vehicle
from src.domain.exceptions.vehicle_not_found_exception import VehicleNotFoundException


@pytest.fixture
def vehicle_repository():
    """Fixture for vehicle repository with test data."""
    from src.infrastructure.database.connection import SessionLocal, engine
    from src.infrastructure.database.models import Base
    from src.infrastructure.repositories.sqlite_vehicle_repository import SqliteVehicleRepository

    # Recreate tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    repository = SqliteVehicleRepository(db_session=session)

    # Create test vehicles
    vehicle1 = Vehicle(id="V-001", plate="ABC-123", model="Toyota Corolla", current_mileage=5000)
    vehicle2 = Vehicle(id="V-002", plate="XYZ-456", model="Honda Civic", current_mileage=10000)
    vehicle3 = Vehicle(id="V-003", plate="ABC-789", model="Mazda 3", current_mileage=15000)

    repository.save(vehicle1)
    repository.save(vehicle2)
    repository.save(vehicle3)

    yield repository

    session.close()


class TestGetVehicleByPlateUseCase:
    """Test cases for GetVehicleByPlateUseCase."""

    def test_search_vehicle_by_exact_plate_returns_one_vehicle(self, vehicle_repository) -> None:
        """
        Test searching vehicle by exact plate match.

        Given: Vehicles exist in the system with plates ABC-123, XYZ-456, ABC-789
        When: I search for vehicles with plate "ABC-123"
        Then: The system should return 1 vehicle
        And: The vehicle should have plate "ABC-123"

        User Story: HU-006 - Escenario 1
        Business Rule: RN-031 - Search must be case-insensitive
        """
        # Arrange
        use_case = GetVehicleByPlateUseCase(vehicle_repository=vehicle_repository)

        # Act
        result = use_case.execute(plate="ABC-123")

        # Assert
        assert isinstance(result, VehicleDTO)
        assert result.plate == "ABC-123"
        assert result.id == "V-001"
        assert result.model == "Toyota Corolla"
        assert result.current_mileage == 5000

    def test_search_vehicle_by_plate_case_insensitive(self, vehicle_repository) -> None:
        """
        Test that search is case-insensitive.

        Given: A vehicle exists with plate "ABC-123"
        When: I search for vehicles with plate "abc-123" (lowercase)
        Then: The system should return the vehicle with plate "ABC-123"
        And: The search should be case-insensitive

        User Story: HU-006 - Escenario 4
        Business Rule: RN-031 - Search must be case-insensitive
        """
        # Arrange
        use_case = GetVehicleByPlateUseCase(vehicle_repository=vehicle_repository)

        # Act
        result = use_case.execute(plate="abc-123")

        # Assert
        assert isinstance(result, VehicleDTO)
        assert result.plate == "ABC-123"
        assert result.id == "V-001"

    def test_search_vehicle_by_nonexistent_plate_raises_exception(self, vehicle_repository) -> None:
        """
        Test searching for a vehicle with a plate that doesn't exist.

        Given: Vehicles exist in the system
        When: I search for vehicles with plate "ZZZ-999"
        Then: The system should raise VehicleNotFoundException

        User Story: HU-006 - Escenario 3
        """
        # Arrange
        use_case = GetVehicleByPlateUseCase(vehicle_repository=vehicle_repository)

        # Act & Assert
        with pytest.raises(VehicleNotFoundException) as exc_info:
            use_case.execute(plate="ZZZ-999")

        assert "ZZZ-999" in str(exc_info.value)

    def test_search_vehicle_validates_plate_format(self, vehicle_repository) -> None:
        """
        Test that the use case validates plate format.

        Given: I'm searching for a vehicle
        When: I provide an invalid plate format
        Then: The system should raise an exception

        Business Rule: RN-010 - Plate must follow XXX-123 or XXX-1234 format
        """
        # Arrange
        use_case = GetVehicleByPlateUseCase(vehicle_repository=vehicle_repository)

        # Act & Assert - Test various invalid formats
        invalid_plates = ["", "   ", "AB-123", "ABCD-123", "123-ABC"]

        for invalid_plate in invalid_plates:
            with pytest.raises(Exception):  # Could be InvalidPlateException or ValueError
                use_case.execute(plate=invalid_plate)

    def test_search_returns_dto_not_entity(self, vehicle_repository) -> None:
        """
        Test that use case returns DTO, not domain entity.

        This ensures proper layer separation in Clean Architecture.

        Given: A vehicle exists with plate "ABC-123"
        When: I search for the vehicle
        Then: The result should be a VehicleDTO
        And: The result should not be a Vehicle entity
        """
        # Arrange
        use_case = GetVehicleByPlateUseCase(vehicle_repository=vehicle_repository)

        # Act
        result = use_case.execute(plate="ABC-123")

        # Assert
        assert isinstance(result, VehicleDTO), f"Expected VehicleDTO, got {type(result).__name__}"
        assert not isinstance(result, Vehicle), "Use case should return DTO, not domain entity"
        assert hasattr(result, 'id')
        assert hasattr(result, 'plate')
        assert hasattr(result, 'model')
        assert hasattr(result, 'current_mileage')
        assert hasattr(result, 'status')
