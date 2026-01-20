"""Tests for Maintenance Strategy Pattern following TDD approach."""
from src.domain.entities.maintenance_alert import AlertType


class TestBasicMaintenanceStrategy:
    """Test cases for BasicMaintenanceStrategy - every 10,000 km."""

    def test_should_generate_alert_at_10000_km(self) -> None:
        """
        Given: BasicMaintenanceStrategy for 10,000 km intervals
        When: Checking if alert should be generated at 10,000 km
        Then: Should return True
        """
        # Arrange
        from src.domain.strategies.basic_maintenance_strategy import BasicMaintenanceStrategy
        strategy = BasicMaintenanceStrategy()

        # Act
        result = strategy.should_generate_alert(old_mileage=5000, new_mileage=10000)

        # Assert
        assert result is True

    def test_should_not_generate_alert_before_threshold(self) -> None:
        """
        Given: BasicMaintenanceStrategy for 10,000 km intervals
        When: Checking if alert should be generated at 8,000 km
        Then: Should return False
        """
        # Arrange
        from src.domain.strategies.basic_maintenance_strategy import BasicMaintenanceStrategy
        strategy = BasicMaintenanceStrategy()

        # Act
        result = strategy.should_generate_alert(old_mileage=5000, new_mileage=8000)

        # Assert
        assert result is False

    def test_get_alert_type_returns_basic(self) -> None:
        """
        Given: BasicMaintenanceStrategy
        When: Getting alert type
        Then: Should return BASIC_MAINTENANCE
        """
        # Arrange
        from src.domain.strategies.basic_maintenance_strategy import BasicMaintenanceStrategy
        strategy = BasicMaintenanceStrategy()

        # Act
        alert_type = strategy.get_alert_type()

        # Assert
        assert alert_type == AlertType.BASIC_MAINTENANCE


class TestMajorMaintenanceStrategy:
    """Test cases for MajorMaintenanceStrategy - every 50,000 km."""

    def test_should_generate_alert_at_50000_km(self) -> None:
        """
        Given: MajorMaintenanceStrategy for 50,000 km intervals
        When: Checking if alert should be generated at 50,000 km
        Then: Should return True
        """
        # Arrange
        from src.domain.strategies.major_maintenance_strategy import MajorMaintenanceStrategy
        strategy = MajorMaintenanceStrategy()

        # Act
        result = strategy.should_generate_alert(old_mileage=30000, new_mileage=50000)

        # Assert
        assert result is True

    def test_should_not_generate_alert_at_40000_km(self) -> None:
        """
        Given: MajorMaintenanceStrategy for 50,000 km intervals
        When: Checking if alert should be generated at 40,000 km
        Then: Should return False
        """
        # Arrange
        from src.domain.strategies.major_maintenance_strategy import MajorMaintenanceStrategy
        strategy = MajorMaintenanceStrategy()

        # Act
        result = strategy.should_generate_alert(old_mileage=30000, new_mileage=40000)

        # Assert
        assert result is False

    def test_get_alert_type_returns_major(self) -> None:
        """
        Given: MajorMaintenanceStrategy
        When: Getting alert type
        Then: Should return MAJOR_MAINTENANCE
        """
        # Arrange
        from src.domain.strategies.major_maintenance_strategy import MajorMaintenanceStrategy
        strategy = MajorMaintenanceStrategy()

        # Act
        alert_type = strategy.get_alert_type()

        # Assert
        assert alert_type == AlertType.MAJOR_MAINTENANCE


class TestCriticalThresholdStrategy:
    """Test cases for CriticalThresholdStrategy - at 100,000 km (RN-007)."""

    def test_should_generate_alert_when_crossing_100000_km(self) -> None:
        """
        Given: CriticalThresholdStrategy for 100,000 km threshold
        When: Checking if alert should be generated when crossing from 99,000 to 100,001 km
        Then: Should return True
        """
        # Arrange
        from src.domain.strategies.critical_threshold_strategy import CriticalThresholdStrategy
        strategy = CriticalThresholdStrategy()

        # Act
        result = strategy.should_generate_alert(old_mileage=99000, new_mileage=100001)

        # Assert
        assert result is True

    def test_should_not_generate_alert_below_100000_km(self) -> None:
        """
        Given: CriticalThresholdStrategy for 100,000 km threshold
        When: Checking if alert should be generated at 80,000 km
        Then: Should return False
        """
        # Arrange
        from src.domain.strategies.critical_threshold_strategy import CriticalThresholdStrategy
        strategy = CriticalThresholdStrategy()

        # Act
        result = strategy.should_generate_alert(old_mileage=50000, new_mileage=80000)

        # Assert
        assert result is False

    def test_should_not_generate_alert_already_above_threshold(self) -> None:
        """
        Given: CriticalThresholdStrategy for 100,000 km threshold
        When: Vehicle already above 100,000 km (from 110,000 to 120,000)
        Then: Should return False (alert only triggers once when crossing)
        """
        # Arrange
        from src.domain.strategies.critical_threshold_strategy import CriticalThresholdStrategy
        strategy = CriticalThresholdStrategy()

        # Act
        result = strategy.should_generate_alert(old_mileage=110000, new_mileage=120000)

        # Assert
        assert result is False

    def test_get_alert_type_returns_critical(self) -> None:
        """
        Given: CriticalThresholdStrategy
        When: Getting alert type
        Then: Should return CRITICAL_THRESHOLD
        """
        # Arrange
        from src.domain.strategies.critical_threshold_strategy import CriticalThresholdStrategy
        strategy = CriticalThresholdStrategy()

        # Act
        alert_type = strategy.get_alert_type()

        # Assert
        assert alert_type == AlertType.CRITICAL_THRESHOLD
