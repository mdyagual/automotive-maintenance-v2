"""
Integration test for Vehicle Status implementation.

This test verifies that the status field works correctly across
all layers: Domain, Infrastructure, and Persistence.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from src.domain.entities.vehicle import Vehicle
from src.domain.entities.vehicle_status import VehicleStatus
from src.infrastructure.database.models import Base
from src.infrastructure.repositories.sqlite_vehicle_repository import SqliteVehicleRepository


def test_status_field_integration():
    """
    Integration test: Vehicle status across all layers.

    Tests:
    1. Domain entity with default status
    2. Domain entity with explicit status
    3. Persistence to database
    4. Retrieval from database
    5. Status enum values
    """
    print("\n" + "=" * 60)
    print("Integration Test: Vehicle Status Field")
    print("=" * 60)

    # Setup test database
    test_db_path = "test_status_integration.db"
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

    engine = create_engine(f"sqlite:///{test_db_path}")
    Base.metadata.create_all(engine)
    session_local = sessionmaker(bind=engine)
    session = session_local()

    try:
        repository = SqliteVehicleRepository(session)

        # Test 1: Default status
        print("\n1. Testing default status...")
        vehicle1 = Vehicle(id="V-001", plate="ABC-001", model="Toyota Corolla", current_mileage=5000)
        assert vehicle1.status == VehicleStatus.ACTIVE
        assert vehicle1.status == "active"
        print("   ✓ Default status is ACTIVE")

        # Test 2: Explicit statuses
        print("\n2. Testing explicit statuses...")
        vehicles = [
            Vehicle("V-002", "ABC-002", "Honda Civic", 10000, VehicleStatus.ACTIVE),
            Vehicle("V-003", "ABC-003", "Mazda 3", 15000, VehicleStatus.INACTIVE),
            Vehicle("V-004", "ABC-004", "Ford Focus", 20000, VehicleStatus.IN_MAINTENANCE),
            Vehicle("V-005", "ABC-005", "Chevy Spark", 25000, VehicleStatus.RETIRED),
        ]

        for vehicle in vehicles:
            print(f"   ✓ Vehicle {vehicle.id}: status={vehicle.status.value}")

        # Test 3: Persist to database
        print("\n3. Testing persistence...")
        for vehicle in [vehicle1] + vehicles:
            repository.save(vehicle)
        print(f"   ✓ Saved {len(vehicles) + 1} vehicles to database")

        # Test 4: Retrieve from database
        print("\n4. Testing retrieval...")
        retrieved_vehicles = repository.get_all()
        assert len(retrieved_vehicles) == 5
        print(f"   ✓ Retrieved {len(retrieved_vehicles)} vehicles")

        # Verify statuses are preserved
        status_map = {v.id: v.status for v in retrieved_vehicles}
        assert status_map["V-001"] == VehicleStatus.ACTIVE
        assert status_map["V-002"] == VehicleStatus.ACTIVE
        assert status_map["V-003"] == VehicleStatus.INACTIVE
        assert status_map["V-004"] == VehicleStatus.IN_MAINTENANCE
        assert status_map["V-005"] == VehicleStatus.RETIRED
        print("   ✓ All statuses preserved correctly")

        # Test 5: Retrieve individual vehicle
        print("\n5. Testing individual retrieval...")
        vehicle_in_maintenance = repository.get_by_id("V-004")
        assert vehicle_in_maintenance.status == VehicleStatus.IN_MAINTENANCE
        assert vehicle_in_maintenance.status == "in_maintenance"
        print(f"   ✓ Vehicle V-004 status: {vehicle_in_maintenance.status.value}")

        # Test 6: Update vehicle (status should persist)
        print("\n6. Testing update with status...")
        vehicle_in_maintenance.current_mileage = 21000
        repository.save(vehicle_in_maintenance)

        updated_vehicle = repository.get_by_id("V-004")
        assert updated_vehicle.current_mileage == 21000
        assert updated_vehicle.status == VehicleStatus.IN_MAINTENANCE
        print("   ✓ Status preserved after update")

        # Test 7: Verify database schema
        print("\n7. Verifying database schema...")
        result = session.execute(text("PRAGMA table_info(vehicles)"))
        columns = {row[1]: row[2] for row in result}
        assert "status" in columns
        print("   ✓ Status column exists in database")
        print(f"   ✓ Status column type: {columns['status']}")

        print("\n" + "=" * 60)
        print("✓ ALL INTEGRATION TESTS PASSED!")
        print("=" * 60)
        print("\nSummary:")
        print("  - Default status works (RN-026)")
        print("  - All 4 status values work")
        print("  - Persistence works correctly")
        print("  - Retrieval preserves status")
        print("  - Updates preserve status")
        print("  - Database schema correct")

    finally:
        session.close()
        engine.dispose()  # Close all connections
        if os.path.exists(test_db_path):
            try:
                os.remove(test_db_path)
            except PermissionError:
                pass  # File still in use, will be cleaned up later


if __name__ == "__main__":
    test_status_field_integration()
