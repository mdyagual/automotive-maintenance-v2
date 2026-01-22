"""Unit tests for VehicleValidator in application layer."""

import pytest
from unittest.mock import Mock

from src.application.validators.vehicle_validator import VehicleValidator
from src.domain.exceptions.invalid_mileage_exception import InvalidMileageException

# TODO: Create these domain exceptions
# from src.domain.exceptions.invalid_vehicle_id_exception import InvalidVehicleIdException
# from src.domain.exceptions.invalid_plate_exception import InvalidPlateException
# from src.domain.exceptions.invalid_model_exception import InvalidModelException


class TestVehicleValidator:
    """Test suite for VehicleValidator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.validator = VehicleValidator()

    # ==================== VEHICLE ID VALIDATION TESTS ====================

    def test_validate_vehicle_id_with_valid_format(self):
        """
        Test that valid vehicle IDs pass validation.
        
        Valid format: V-XXX where XXX is exactly 3 digits.
        Examples: V-001, V-123, V-999
        """
        # Valid IDs
        valid_ids = ["V-001", "V-123", "V-999", "V-000"]
        
        for vehicle_id in valid_ids:
            # Should not raise any exception
            self.validator.validate_vehicle_id(vehicle_id)

    def test_validate_vehicle_id_rejects_invalid_format(self):
        """
        Test that invalid vehicle ID formats are rejected.
        
        Invalid cases:
        - Wrong prefix (not V-)
        - Wrong number of digits
        - Missing hyphen
        - Contains letters in number part
        
        Should raise: InvalidVehicleIdException (domain exception)
        """
        invalid_ids = [
            "A-001",      # Wrong prefix
            "V-12",       # Too few digits
            "V-1234",     # Too many digits
            "V001",       # Missing hyphen
            "V-ABC",      # Letters instead of numbers
            "v-001",      # Lowercase prefix
            "V-01",       # Only 2 digits
            "",           # Empty string
            "V-",         # Missing number
            "123",        # No prefix
        ]
        
        for vehicle_id in invalid_ids:
            # TODO: Change to InvalidVehicleIdException when created
            with pytest.raises((ValueError, Exception)) as exc_info:
                self.validator.validate_vehicle_id(vehicle_id)
            # Verify error message is descriptive
            error_msg = str(exc_info.value).lower()
            assert "vehicle_id" in error_msg or "formato" in error_msg or "inválido" in error_msg

    def test_validate_vehicle_id_rejects_none(self):
        """
        Test that None vehicle_id is rejected.
        
        Should raise: InvalidVehicleIdException (domain exception)
        """
        # TODO: Change to InvalidVehicleIdException when created
        with pytest.raises((ValueError, TypeError, Exception)):
            self.validator.validate_vehicle_id(None)

    # ==================== PLATE VALIDATION TESTS ====================

    def test_validate_plate_with_valid_format(self):
        """
        Test that valid plate formats pass validation.
        
        Valid formats:
        - XXX-123 (3 uppercase letters, hyphen, 3 digits)
        - XXX-1234 (3 uppercase letters, hyphen, 4 digits)
        
        Examples: ABC-123, XYZ-9999, DEF-001
        """
        valid_plates = [
            "ABC-123",
            "XYZ-456",
            "DEF-789",
            "ABC-1234",
            "XYZ-9999",
            "AAA-000",
        ]
        
        for plate in valid_plates:
            # Should not raise any exception
            self.validator.validate_plate(plate)

    def test_validate_plate_rejects_invalid_format(self):
        """
        Test that invalid plate formats are rejected.
        
        Invalid cases:
        - Wrong number of letters
        - Wrong number of digits
        - Lowercase letters
        - Missing hyphen
        - Numbers in letter section
        - Letters in number section
        
        Should raise: InvalidPlateException (domain exception)
        """
        invalid_plates = [
            "AB-123",      # Only 2 letters
            "ABCD-123",    # 4 letters
            "ABC-12",      # Only 2 digits
            "ABC-12345",   # 5 digits
            "abc-123",     # Lowercase letters
            "ABC123",      # Missing hyphen
            "123-ABC",     # Reversed format
            "A1C-123",     # Number in letter section
            "ABC-12A",     # Letter in number section
            "",            # Empty string
            "ABC-",        # Missing numbers
            "-123",        # Missing letters
        ]
        
        for plate in invalid_plates:
            # TODO: Change to InvalidPlateException when created
            with pytest.raises((ValueError, Exception)) as exc_info:
                self.validator.validate_plate(plate)
            # Verify error message is descriptive
            error_msg = str(exc_info.value).lower()
            assert "plate" in error_msg or "placa" in error_msg or "formato" in error_msg

    def test_validate_plate_rejects_none(self):
        """
        Test that None plate is rejected.
        
        Should raise: InvalidPlateException (domain exception)
        """
        # TODO: Change to InvalidPlateException when created
        with pytest.raises((ValueError, TypeError, Exception)):
            self.validator.validate_plate(None)

    # ==================== MODEL VALIDATION TESTS ====================

    def test_validate_model_with_valid_values(self):
        """
        Test that valid model names pass validation.
        
        Valid models:
        - Non-empty strings
        - Can contain letters, numbers, spaces
        - Reasonable length
        """
        valid_models = [
            "Toyota Corolla",
            "Honda Civic 2020",
            "Mazda 3",
            "Ford F-150",
            "Chevrolet Spark GT",
            "BMW X5",
        ]
        
        for model in valid_models:
            # Should not raise any exception
            self.validator.validate_model(model)

    def test_validate_model_rejects_empty_string(self):
        """
        Test that empty model string is rejected.
        
        Should raise: InvalidModelException (domain exception)
        """
        # TODO: Change to InvalidModelException when created
        with pytest.raises((ValueError, Exception)) as exc_info:
            self.validator.validate_model("")
        error_msg = str(exc_info.value).lower()
        assert "model" in error_msg or "modelo" in error_msg or "vacío" in error_msg

    def test_validate_model_rejects_whitespace_only(self):
        """
        Test that whitespace-only model is rejected.
        
        Should raise: InvalidModelException (domain exception)
        """
        invalid_models = ["   ", "\t", "\n", "  \t  "]
        
        for model in invalid_models:
            # TODO: Change to InvalidModelException when created
            with pytest.raises((ValueError, Exception)) as exc_info:
                self.validator.validate_model(model)
            error_msg = str(exc_info.value).lower()
            assert "model" in error_msg or "modelo" in error_msg or "vacío" in error_msg

    def test_validate_model_rejects_none(self):
        """
        Test that None model is rejected.
        
        Should raise: InvalidModelException (domain exception)
        """
        # TODO: Change to InvalidModelException when created
        with pytest.raises((ValueError, TypeError, Exception)):
            self.validator.validate_model(None)

    def test_validate_model_rejects_too_long(self):
        """
        Test that excessively long model names are rejected.
        
        Model name longer than 100 characters should be rejected.
        Should raise: InvalidModelException (domain exception)
        """
        # Model name longer than 100 characters should be rejected
        too_long_model = "A" * 101
        
        # TODO: Change to InvalidModelException when created
        with pytest.raises((ValueError, Exception)) as exc_info:
            self.validator.validate_model(too_long_model)
        error_msg = str(exc_info.value).lower()
        assert "model" in error_msg or "modelo" in error_msg or "longitud" in error_msg

    # ==================== INITIAL MILEAGE VALIDATION TESTS ====================

    def test_validate_initial_mileage_with_valid_values(self):
        """
        Test that valid initial mileage values pass validation.
        
        Valid range: 0 to 1,000,000 km (inclusive)
        """
        valid_mileages = [0, 1, 5000, 10000, 50000, 100000, 500000, 999999, 1000000]
        
        for mileage in valid_mileages:
            # Should not raise any exception
            self.validator.validate_initial_mileage(mileage)

    def test_validate_initial_mileage_rejects_negative(self):
        """
        Test that negative mileage values are rejected.
        
        Should raise: InvalidMileageException (domain exception)
        """
        invalid_mileages = [-1, -100, -5000]
        
        for mileage in invalid_mileages:
            with pytest.raises(InvalidMileageException) as exc_info:
                self.validator.validate_initial_mileage(mileage)
            error_msg = str(exc_info.value).lower()
            assert "mileage" in error_msg or "kilometraje" in error_msg or "negativo" in error_msg

    def test_validate_initial_mileage_rejects_exceeds_max(self):
        """
        Test that mileage exceeding MAX_MILEAGE is rejected.
        
        MAX_MILEAGE = 1,000,000 km
        Should raise: InvalidMileageException (domain exception)
        """
        invalid_mileages = [1000001, 1500000, 2000000, 10000000]
        
        for mileage in invalid_mileages:
            with pytest.raises(InvalidMileageException) as exc_info:
                self.validator.validate_initial_mileage(mileage)
            error_msg = str(exc_info.value).lower()
            assert "mileage" in error_msg or "kilometraje" in error_msg or "máximo" in error_msg or "excede" in error_msg

    def test_validate_initial_mileage_rejects_none(self):
        """
        Test that None mileage is rejected.
        
        Should raise: InvalidMileageException (domain exception)
        """
        with pytest.raises((InvalidMileageException, TypeError, Exception)):
            self.validator.validate_initial_mileage(None)

    # ==================== COMPLETE VEHICLE DATA VALIDATION TESTS ====================

    def test_validate_vehicle_data_with_all_valid_inputs(self):
        """
        Test that complete vehicle data validation passes with all valid inputs.
        
        This method should validate all fields together.
        """
        # Should not raise any exception
        self.validator.validate_vehicle_data(
            vehicle_id="V-123",
            plate="ABC-123",
            model="Toyota Corolla",
            initial_mileage=5000
        )

    def test_validate_vehicle_data_rejects_invalid_vehicle_id(self):
        """
        Test that validate_vehicle_data rejects invalid vehicle_id.
        
        Should raise: InvalidVehicleIdException (domain exception)
        """
        # TODO: Change to InvalidVehicleIdException when created
        with pytest.raises((ValueError, Exception)):
            self.validator.validate_vehicle_data(
                vehicle_id="INVALID",
                plate="ABC-123",
                model="Toyota Corolla",
                initial_mileage=5000
            )

    def test_validate_vehicle_data_rejects_invalid_plate(self):
        """
        Test that validate_vehicle_data rejects invalid plate.
        
        Should raise: InvalidPlateException (domain exception)
        """
        # TODO: Change to InvalidPlateException when created
        with pytest.raises((ValueError, Exception)):
            self.validator.validate_vehicle_data(
                vehicle_id="V-123",
                plate="INVALID",
                model="Toyota Corolla",
                initial_mileage=5000
            )

    def test_validate_vehicle_data_rejects_invalid_model(self):
        """
        Test that validate_vehicle_data rejects invalid model.
        
        Should raise: InvalidModelException (domain exception)
        """
        # TODO: Change to InvalidModelException when created
        with pytest.raises((ValueError, Exception)):
            self.validator.validate_vehicle_data(
                vehicle_id="V-123",
                plate="ABC-123",
                model="",
                initial_mileage=5000
            )

    def test_validate_vehicle_data_rejects_invalid_mileage(self):
        """
        Test that validate_vehicle_data rejects invalid mileage.
        
        Should raise: InvalidMileageException (domain exception)
        """
        with pytest.raises(InvalidMileageException):
            self.validator.validate_vehicle_data(
                vehicle_id="V-123",
                plate="ABC-123",
                model="Toyota Corolla",
                initial_mileage=-100
            )

    def test_validate_vehicle_data_with_edge_case_values(self):
        """Test validation with edge case but valid values."""
        # Minimum valid values
        self.validator.validate_vehicle_data(
            vehicle_id="V-000",
            plate="AAA-000",
            model="A",
            initial_mileage=0
        )
        
        # Maximum valid values
        self.validator.validate_vehicle_data(
            vehicle_id="V-999",
            plate="ZZZ-9999",
            model="A" * 100,  # Max length
            initial_mileage=1000000
        )

    # ==================== INTEGRATION WITH USE CASE TESTS ====================

    def test_validator_can_be_used_in_use_case_context(self):
        """
        Test that validator can be instantiated and used in a use case context.
        
        This ensures the validator follows dependency injection patterns.
        """
        # Validator should be instantiable without dependencies
        validator = VehicleValidator()
        
        # Should be able to validate data
        validator.validate_vehicle_data(
            vehicle_id="V-123",
            plate="ABC-123",
            model="Toyota Corolla",
            initial_mileage=5000
        )

    def test_validator_provides_clear_error_messages(self):
        """
        Test that validator provides clear, actionable error messages.
        
        Error messages should help developers understand what went wrong.
        """
        # Test vehicle_id error message
        # TODO: Change to InvalidVehicleIdException when created
        with pytest.raises((ValueError, Exception)) as exc_info:
            self.validator.validate_vehicle_id("INVALID")
        error_msg = str(exc_info.value)
        assert len(error_msg) > 0
        assert "V-" in error_msg or "formato" in error_msg.lower()
        
        # Test plate error message
        # TODO: Change to InvalidPlateException when created
        with pytest.raises((ValueError, Exception)) as exc_info:
            self.validator.validate_plate("INVALID")
        error_msg = str(exc_info.value)
        assert len(error_msg) > 0
        
        # Test model error message
        # TODO: Change to InvalidModelException when created
        with pytest.raises((ValueError, Exception)) as exc_info:
            self.validator.validate_model("")
        error_msg = str(exc_info.value)
        assert len(error_msg) > 0
        
        # Test mileage error message
        with pytest.raises(InvalidMileageException) as exc_info:
            self.validator.validate_initial_mileage(-100)
        error_msg = str(exc_info.value)
        assert len(error_msg) > 0
