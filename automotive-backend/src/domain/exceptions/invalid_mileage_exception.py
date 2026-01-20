"""Business exception for invalid mileage operations."""


class InvalidMileageException(Exception):
    """Exception raised when mileage update violates business rules."""

    def __init__(self, message: str = "El kilometraje debe ser mayor al actual") -> None:
        """
        Initialize InvalidMileageException.

        Args:
            message: Error message describing the validation failure
        """
        self.message = message
        super().__init__(self.message)
