"""Tests for GetAllVehiclesUseCase - Application layer."""
from datetime import datetime

import pytest
from unittest.mock import Mock

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
        
        This test FAILS because:
        - GetAllVehiclesUseCase.execute() returns list[VehicleWithAlerts]
        - VehicleWithAlerts contains Vehicle and MaintenanceAlert domain entities
        - Domain entities should NEVER be exposed outside domain/application layers
        
        CORRECT IMPLEMENTATION should:
        - Return list[VehicleWithAlertsDTO]
        - VehicleWithAlertsDTO should contain VehicleDTO and list[AlertDTO]
        - Keep domain entities encapsulated
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
        
        # Assert - THIS SHOULD FAIL
        # Check if result contains domain entities
        if result:
            first_item = result[0]
            vehicle_in_result = first_item["vehicle"]
            alerts_in_result = first_item["alerts"]
            
            has_domain_entities = (
                isinstance(vehicle_in_result, Vehicle) or
                (alerts_in_result and isinstance(alerts_in_result[0], MaintenanceAlert))
            )
            
            assert not has_domain_entities, (
                "ARCHITECTURAL VIOLATION: Use case returns domain entities "
                "(Vehicle, MaintenanceAlert) instead of DTOs. "
                "Domain entities should never leave the application layer. "
                "Expected: VehicleWithAlertsDTO containing VehicleDTO and list[AlertDTO]. "
                "Got: VehicleWithAlerts containing Vehicle and MaintenanceAlert entities."
            )

    def test_return_type_should_contain_dtos_not_entities(self):
        """
        ARCHITECTURAL VIOLATION TEST: Return type contains domain entities.
        
        This test FAILS because:
        - VehicleWithAlerts TypedDict contains Vehicle and MaintenanceAlert entities
        - Should contain DTOs instead
        - Type hints reveal architectural violation
        
        CORRECT IMPLEMENTATION should:
        - Define VehicleWithAlertsDTO with VehicleDTO and list[AlertDTO]
        - Return list[VehicleWithAlertsDTO]
        """
        # Arrange
        from src.application.use_cases.get_all_vehicles_use_case import VehicleWithAlerts
        import typing
        
        # Act - Check TypedDict annotations
        if hasattr(VehicleWithAlerts, '__annotations__'):
            annotations = VehicleWithAlerts.__annotations__
            
            vehicle_type = annotations.get('vehicle')
            alerts_type = annotations.get('alerts')
            
            # Assert - THIS SHOULD FAIL
            # Check if annotations reference domain entities
            vehicle_is_entity = (vehicle_type == Vehicle or 
                                str(vehicle_type) == "<class 'src.domain.entities.vehicle.Vehicle'>")
            
            # Check alerts type (should be list[AlertDTO], not list[MaintenanceAlert])
            alerts_contains_entity = False
            if hasattr(alerts_type, '__args__'):
                alert_item_type = alerts_type.__args__[0] if alerts_type.__args__ else None
                alerts_contains_entity = (alert_item_type == MaintenanceAlert or
                                        str(alert_item_type) == "<class 'src.domain.entities.maintenance_alert.MaintenanceAlert'>")
            
            assert not vehicle_is_entity, (
                "ARCHITECTURAL VIOLATION: VehicleWithAlerts TypedDict declares "
                f"'vehicle: {vehicle_type}' (domain entity). "
                "Should declare 'vehicle: VehicleDTO' (application DTO). "
                "Domain entities should never appear in use case return types."
            )
            
            assert not alerts_contains_entity, (
                "ARCHITECTURAL VIOLATION: VehicleWithAlerts TypedDict declares "
                f"'alerts: {alerts_type}' containing MaintenanceAlert (domain entity). "
                "Should declare 'alerts: list[AlertDTO]' (application DTOs). "
                "Domain entities should never appear in use case return types."
            )

    def test_web_layer_should_not_access_domain_entity_methods(self):
        """
        ARCHITECTURAL VIOLATION TEST: Web layer can access domain entity methods.
        
        This test simulates what happens in main.py where:
        - Web layer receives domain entities from use case
        - Web layer can access entity methods like update_mileage(), attach()
        - Creates tight coupling and exposes domain logic
        
        CORRECT IMPLEMENTATION should:
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
            vehicle_from_result = result[0]["vehicle"]
            
            # Assert - THIS SHOULD FAIL
            # Check if web layer has access to domain methods
            has_domain_methods = (
                hasattr(vehicle_from_result, 'update_mileage') and
                hasattr(vehicle_from_result, 'attach') and
                hasattr(vehicle_from_result, '_notify_observers')
            )
            
            assert not has_domain_methods, (
                "ARCHITECTURAL VIOLATION: Web layer receives domain entity with business logic methods. "
                "The object has methods: update_mileage(), attach(), _notify_observers(). "
                "Web layer should only receive DTOs (data transfer objects) without business logic. "
                "This exposes domain internals and creates tight coupling between layers."
            )
