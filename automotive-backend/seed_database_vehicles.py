"""
Seed script to populate the database with test data.

This script creates a variety of vehicles with different statuses, mileages,
and maintenance alerts to test all functionality including filters, updates,
and deletes.

Usage:
    python seed_database.py
"""

import random
from datetime import datetime, timedelta

from src.domain.entities.maintenance_alert import AlertType, MaintenanceAlert
from src.domain.entities.vehicle import Vehicle
from src.domain.entities.vehicle_status import VehicleStatus
from src.infrastructure.database.connection import SessionLocal, create_tables
from src.infrastructure.database.models import AlertModel, VehicleModel


def clear_database(session):
    """Clear all existing data from the database."""
    print("🗑️  Clearing existing data...")
    session.query(AlertModel).delete()
    session.query(VehicleModel).delete()
    session.commit()
    print("✅ Database cleared")


def create_test_vehicles():
    """
    Create a diverse set of test vehicles with different characteristics.
    
    Returns:
        List of tuples (Vehicle entity, list of alerts)
    """
    vehicles_data = [
        # Active vehicles with various mileages
        {
            "id": "V-001",
            "plate": "ABC-123",
            "model": "Toyota Corolla 2020",
            "mileage": 15000,
            "status": VehicleStatus.ACTIVE,
            "alerts": [
                (10000, AlertType.BASIC_MAINTENANCE, -5),  # 5 days ago
            ]
        },
        {
            "id": "V-002",
            "plate": "XYZ-456",
            "model": "Honda Civic 2019",
            "mileage": 52000,
            "status": VehicleStatus.ACTIVE,
            "alerts": [
                (10000, AlertType.BASIC_MAINTENANCE, -30),
                (20000, AlertType.BASIC_MAINTENANCE, -25),
                (30000, AlertType.BASIC_MAINTENANCE, -20),
                (40000, AlertType.BASIC_MAINTENANCE, -15),
                (50000, AlertType.MAJOR_MAINTENANCE, -10),
            ]
        },
        {
            "id": "V-003",
            "plate": "DEF-789",
            "model": "Mazda 3 2021",
            "mileage": 8500,
            "status": VehicleStatus.ACTIVE,
            "alerts": []  # No alerts yet
        },
        {
            "id": "V-004",
            "plate": "GHI-1234",
            "model": "Ford Focus 2018",
            "mileage": 105000,
            "status": VehicleStatus.ACTIVE,
            "alerts": [
                (10000, AlertType.BASIC_MAINTENANCE, -90),
                (20000, AlertType.BASIC_MAINTENANCE, -85),
                (30000, AlertType.BASIC_MAINTENANCE, -80),
                (40000, AlertType.BASIC_MAINTENANCE, -75),
                (50000, AlertType.MAJOR_MAINTENANCE, -70),
                (60000, AlertType.BASIC_MAINTENANCE, -65),
                (70000, AlertType.BASIC_MAINTENANCE, -60),
                (80000, AlertType.BASIC_MAINTENANCE, -55),
                (90000, AlertType.BASIC_MAINTENANCE, -50),
                (100000, AlertType.CRITICAL_THRESHOLD, -45),
            ]
        },
        {
            "id": "V-005",
            "plate": "JKL-567",
            "model": "Chevrolet Spark 2022",
            "mileage": 3200,
            "status": VehicleStatus.ACTIVE,
            "alerts": []
        },
        
        # Vehicles in maintenance
        {
            "id": "V-006",
            "plate": "MNO-890",
            "model": "Nissan Sentra 2020",
            "mileage": 45000,
            "status": VehicleStatus.IN_MAINTENANCE,
            "alerts": [
                (10000, AlertType.BASIC_MAINTENANCE, -40),
                (20000, AlertType.BASIC_MAINTENANCE, -35),
                (30000, AlertType.BASIC_MAINTENANCE, -30),
                (40000, AlertType.BASIC_MAINTENANCE, -2),  # Recent alert
            ]
        },
        {
            "id": "V-007",
            "plate": "PQR-234",
            "model": "Hyundai Accent 2019",
            "mileage": 62000,
            "status": VehicleStatus.IN_MAINTENANCE,
            "alerts": [
                (10000, AlertType.BASIC_MAINTENANCE, -50),
                (20000, AlertType.BASIC_MAINTENANCE, -45),
                (30000, AlertType.BASIC_MAINTENANCE, -40),
                (40000, AlertType.BASIC_MAINTENANCE, -35),
                (50000, AlertType.MAJOR_MAINTENANCE, -30),
                (60000, AlertType.BASIC_MAINTENANCE, -1),  # Yesterday
            ]
        },
        
        # Inactive vehicles
        {
            "id": "V-008",
            "plate": "STU-678",
            "model": "Kia Rio 2017",
            "mileage": 78000,
            "status": VehicleStatus.INACTIVE,
            "alerts": [
                (10000, AlertType.BASIC_MAINTENANCE, -120),
                (20000, AlertType.BASIC_MAINTENANCE, -115),
                (30000, AlertType.BASIC_MAINTENANCE, -110),
                (40000, AlertType.BASIC_MAINTENANCE, -105),
                (50000, AlertType.MAJOR_MAINTENANCE, -100),
                (60000, AlertType.BASIC_MAINTENANCE, -95),
                (70000, AlertType.BASIC_MAINTENANCE, -90),
            ]
        },
        {
            "id": "V-009",
            "plate": "VWX-901",
            "model": "Renault Logan 2018",
            "mileage": 35000,
            "status": VehicleStatus.INACTIVE,
            "alerts": [
                (10000, AlertType.BASIC_MAINTENANCE, -60),
                (20000, AlertType.BASIC_MAINTENANCE, -55),
                (30000, AlertType.BASIC_MAINTENANCE, -50),
            ]
        },
        
        # Retired vehicles
        {
            "id": "V-010",
            "plate": "YZA-345",
            "model": "Volkswagen Gol 2015",
            "mileage": 250000,
            "status": VehicleStatus.RETIRED,
            "alerts": [
                (10000, AlertType.BASIC_MAINTENANCE, -200),
                (20000, AlertType.BASIC_MAINTENANCE, -195),
                (30000, AlertType.BASIC_MAINTENANCE, -190),
                (40000, AlertType.BASIC_MAINTENANCE, -185),
                (50000, AlertType.MAJOR_MAINTENANCE, -180),
                (100000, AlertType.CRITICAL_THRESHOLD, -150),
                (200000, AlertType.BASIC_MAINTENANCE, -100),
            ]
        },
        {
            "id": "V-011",
            "plate": "BCD-789",
            "model": "Fiat Palio 2014",
            "mileage": 180000,
            "status": VehicleStatus.RETIRED,
            "alerts": [
                (10000, AlertType.BASIC_MAINTENANCE, -180),
                (50000, AlertType.MAJOR_MAINTENANCE, -160),
                (100000, AlertType.CRITICAL_THRESHOLD, -140),
                (150000, AlertType.MAJOR_MAINTENANCE, -120),
            ]
        },
        
        # Additional active vehicles for testing filters
        {
            "id": "V-012",
            "plate": "EFG-123",
            "model": "Toyota Yaris 2021",
            "mileage": 22000,
            "status": VehicleStatus.ACTIVE,
            "alerts": [
                (10000, AlertType.BASIC_MAINTENANCE, -10),
                (20000, AlertType.BASIC_MAINTENANCE, -3),
            ]
        },
        {
            "id": "V-013",
            "plate": "HIJ-456",
            "model": "Mazda CX-5 2020",
            "mileage": 95000,
            "status": VehicleStatus.ACTIVE,
            "alerts": [
                (10000, AlertType.BASIC_MAINTENANCE, -80),
                (20000, AlertType.BASIC_MAINTENANCE, -75),
                (30000, AlertType.BASIC_MAINTENANCE, -70),
                (40000, AlertType.BASIC_MAINTENANCE, -65),
                (50000, AlertType.MAJOR_MAINTENANCE, -60),
                (60000, AlertType.BASIC_MAINTENANCE, -55),
                (70000, AlertType.BASIC_MAINTENANCE, -50),
                (80000, AlertType.BASIC_MAINTENANCE, -45),
                (90000, AlertType.BASIC_MAINTENANCE, -40),
            ]
        },
        {
            "id": "V-014",
            "plate": "KLM-789",
            "model": "Honda CR-V 2019",
            "mileage": 5000,
            "status": VehicleStatus.ACTIVE,
            "alerts": []
        },
        {
            "id": "V-015",
            "plate": "NOP-012",
            "model": "Chevrolet Onix 2022",
            "mileage": 12000,
            "status": VehicleStatus.ACTIVE,
            "alerts": [
                (10000, AlertType.BASIC_MAINTENANCE, -7),
            ]
        },
    ]
    
    return vehicles_data


def seed_database():
    """Main function to seed the database with test data."""
    print("🌱 Starting database seeding...")
    print("=" * 60)
    
    # Create tables if they don't exist
    create_tables()
    
    # Get database session
    session = SessionLocal()
    
    try:
        # Clear existing data
        clear_database(session)
        
        # Get test vehicles data
        vehicles_data = create_test_vehicles()
        
        print(f"\n📦 Creating {len(vehicles_data)} vehicles...")
        print("=" * 60)
        
        # Create vehicles and alerts
        for vehicle_data in vehicles_data:
            # Create vehicle model directly (bypass domain validation for seeding)
            vehicle_model = VehicleModel(
                id=vehicle_data["id"],
                plate=vehicle_data["plate"],
                model=vehicle_data["model"],
                current_mileage=vehicle_data["mileage"],
                status=vehicle_data["status"],
                status_updated_at=datetime.now()
            )
            
            session.add(vehicle_model)
            
            # Create alerts for this vehicle
            for alert_data in vehicle_data["alerts"]:
                mileage, alert_type, days_ago = alert_data
                
                # Generate alert ID
                alert_id = f"{vehicle_data['id']}-{mileage}-{alert_type.value.upper()}"
                
                # Calculate timestamp
                timestamp = datetime.now() + timedelta(days=days_ago)
                
                # Create alert model
                alert_model = AlertModel(
                    id=alert_id,
                    vehicle_id=vehicle_data["id"],
                    alert_type=alert_type,
                    mileage=mileage,
                    timestamp=timestamp
                )
                
                session.add(alert_model)
            
            # Print vehicle info
            status_emoji = {
                VehicleStatus.ACTIVE: "🟢",
                VehicleStatus.IN_MAINTENANCE: "🟡",
                VehicleStatus.INACTIVE: "⚪",
                VehicleStatus.RETIRED: "🔴"
            }
            
            print(f"{status_emoji[vehicle_data['status']]} {vehicle_data['id']} - "
                  f"{vehicle_data['model']} ({vehicle_data['plate']}) - "
                  f"{vehicle_data['mileage']:,} km - "
                  f"{len(vehicle_data['alerts'])} alerts - "
                  f"Status: {vehicle_data['status'].value}")
        
        # Commit all changes
        session.commit()
        
        print("\n" + "=" * 60)
        print("✅ Database seeding completed successfully!")
        print("=" * 60)
        
        # Print summary statistics
        print("\n📊 SUMMARY:")
        print(f"   Total vehicles: {len(vehicles_data)}")
        
        status_counts = {}
        total_alerts = 0
        for vehicle_data in vehicles_data:
            status = vehicle_data["status"].value
            status_counts[status] = status_counts.get(status, 0) + 1
            total_alerts += len(vehicle_data["alerts"])
        
        print(f"   Total alerts: {total_alerts}")
        print("\n   Vehicles by status:")
        print(f"      🟢 Active: {status_counts.get('active', 0)}")
        print(f"      🟡 In Maintenance: {status_counts.get('in_maintenance', 0)}")
        print(f"      ⚪ Inactive: {status_counts.get('inactive', 0)}")
        print(f"      🔴 Retired: {status_counts.get('retired', 0)}")
        
        print("\n💡 TIP: You can now test:")
        print("   - Filter vehicles by status")
        print("   - Update mileage (avoid retired vehicles)")
        print("   - Delete vehicles")
        print("   - View alerts for each vehicle")
        print("   - Update vehicle status")
        
        print("\n🚀 Start the backend and frontend to see the data!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed_database()
