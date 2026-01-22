"""Tests for GetAllVehiclesUseCase - Application layer."""
from datetime import datetime

import pytest
from unittest.mock import Mock

from src.application.dtos.vehicle_dtos import VehicleDTO, AlertDTO, VehicleWithAlertsDTO
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
        assert all(isinstance(item, VehicleWithAlertsDTO) for item in result)

        # Verify vehicle1 with 2 alerts (most recent first)
        vehicle1_result = next(v for v in result if v.vehicle.id == "V-100")
        assert isinstance(vehicle1_result.vehicle, VehicleDTO)
        assert vehicle1_result.vehicle.plate == "ABC-100"
        assert vehicle1_result.vehicle.current_mileage == 15000
        assert len(vehicle1_result.alerts) == 2
        assert all(isinstance(alert, AlertDTO) for alert in vehicle1_result.alerts)
        assert vehicle1_result.alerts[0].id == "alert-2"  # Most recent first
        assert vehicle1_result.alerts[1].id == "alert-1"

        # Verify vehicle2 with 1 alert
        vehicle2_result = next(v for v in result if v.vehicle.id == "V-200")
        assert vehicle2_result.vehicle.plate == "XYZ-200"
        assert len(vehicle2_result.alerts) == 1
        assert vehicle2_result.alerts[0].id == "alert-3"

        # Verify vehicle3 with no alerts
        vehicle3_result = next(v for v in result if v.vehicle.id == "V-300")
        assert vehicle3_result.vehicle.plate == "DEF-300"
        assert len(vehicle3_result.alerts) == 0

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

    """
    Tests to demonstrate Clean Architecture violation: Missing Application Layer DTOs.
    
    ARCHITECTURAL FLAW:
    - Use case returns domain entities (Vehicle, MaintenanceAlert) directly
    - Web layer receives and accesses domain entities
    - Domain entities exposed to outer layers
    - TypedDict contains domain entities instead of DTOs
    """

    def test_use_case_should_not_return_domain_entities(self):
        """
        ARCHITECTURAL VIOLATION TEST: Use case returns domain entities instead of DTOs.
        
        This test PASSES NOW because:
        - GetAllVehiclesUseCase.execute() returns list[VehicleWithAlertsDTO]
        - VehicleWithAlertsDTO contains VehicleDTO and list[AlertDTO]
        - Domain entities are encapsulated
        """
        # Arrange
        mock_vehicle_repo = Mock()
        mock_alert_repo = Mock()
        
        vehicle = Vehicle(
            id="V-001",
            plate="ABC-123",
            model="Toyota Corolla",
            current_mileage=5000
        )
        alert = MaintenanceAlert(
            id="A-001",
            vehicle_id="V-001",
            alert_type=AlertType.BASIC_MAINTENANCE,
            mileage=10000,
            timestamp=datetime.now()
        )
        
        mock_vehicle_repo.get_all.return_value = [vehicle]
        mock_alert_repo.get_by_vehicle_id.return_value = [alert]
        
        use_case = GetAllVehiclesUseCase(
            vehicle_repository=mock_vehicle_repo,
            alert_repository=mock_alert_repo
        )
        
        # Act
        result = use_case.execute()
        
        # Assert - THIS SHOULD NOW PASS
        # Check if result contains DTOs, not domain entities
        if result:
            first_item = result[0]
            assert isinstance(first_item, VehicleWithAlertsDTO), (
                f"Expected VehicleWithAlertsDTO, got {type(first_item).__name__}"
            )
            
            vehicle_in_result = first_item.vehicle
            alerts_in_result = first_item.alerts
            
            assert isinstance(vehicle_in_result, VehicleDTO), (
                f"Expected VehicleDTO, got {type(vehicle_in_result).__name__}"
            )
            
            assert not isinstance(vehicle_in_result, Vehicle), (
                "Should not return Vehicle domain entity"
            )
            
            if alerts_in_result:
                assert isinstance(alerts_in_result[0], AlertDTO), (
                    f"Expected AlertDTO, got {type(alerts_in_result[0]).__name__}"
                )
                assert not isinstance(alerts_in_result[0], MaintenanceAlert), (
                    "Should not return MaintenanceAlert domain entity"
                )

    def test_return_type_should_contain_dtos_not_entities(self):
        """
        ARCHITECTURAL VIOLATION TEST: Return type contains domain entities.
        
        This test PASSES NOW because:
        - Return type is list[VehicleWithAlertsDTO]
        - VehicleWithAlertsDTO contains VehicleDTO and list[AlertDTO]
        - No domain entities in type hints
        """
        # Arrange
        use_case = GetAllVehiclesUseCase(
            vehicle_repository=Mock(),
            alert_repository=Mock()
        )
        
        # Act - Check return type annotation
        import inspect
        sig = inspect.signature(use_case.execute)
        return_annotation = sig.return_annotation
        
        # Assert - THIS SHOULD NOW PASS
        # Check if return type contains VehicleWithAlertsDTO
        return_str = str(return_annotation)
        
        assert 'VehicleWithAlertsDTO' in return_str, (
            f"Expected return type to contain VehicleWithAlertsDTO. Got: {return_annotation}"
        )
        
        # Ensure it doesn't contain domain entity types
        assert 'Vehicle' not in return_str or 'VehicleDTO' in return_str or 'VehicleWithAlertsDTO' in return_str, (
            "Return type should not reference Vehicle domain entity directly"
        )

    def test_web_layer_should_not_access_domain_entity_methods(self):
        """
        ARCHITECTURAL VIOLATION TEST: Web layer can access domain entity methods.
        
        This test PASSES NOW because:
        - Web layer receives DTOs (data only, no methods)
        - DTOs are immutable
        - No access to domain logic
        """
        # Arrange
        mock_vehicle_repo = Mock()
        mock_alert_repo = Mock()
        
        vehicle = Vehicle(
            id="V-001",
            plate="ABC-123",
            model="Toyota Corolla",
            current_mileage=5000
        )
        
        mock_vehicle_repo.get_all.return_value = [vehicle]
        mock_alert_repo.get_by_vehicle_id.return_value = []
        
        use_case = GetAllVehiclesUseCase(
            vehicle_repository=mock_vehicle_repo,
            alert_repository=mock_alert_repo
        )
        
        # Act - Simulate what web layer does
        result = use_case.execute()
        
        if result:
            vehicle_from_result = result[0].vehicle
            
            # Assert - THIS SHOULD NOW PASS
            # Check that web layer doesn't have access to domain methods
            has_domain_methods = (
                hasattr(vehicle_from_result, 'update_mileage') and
                hasattr(vehicle_from_result, 'attach') and
                hasattr(vehicle_from_result, '_notify_observers')
            )
            
            assert not has_domain_methods, (
                "Web layer should receive DTO without business logic methods. "
                f"Got object with type: {type(vehicle_from_result).__name__}"
            )
            
            # Verify it's a DTO
            assert isinstance(vehicle_from_result, VehicleDTO), (
                f"Expected VehicleDTO, got {type(vehicle_from_result).__name__}"
            )
