"""Exception for invalid vehicle ID format."""


class InvalidVehicleIdException(Exception):
    """Raised when vehicle ID format is invalid."""

    def __init__(self, message: str = "Formato de vehicle_id inválido") -> None:
        """
        Initialize InvalidVehicleIdException.

        Args:
            message: Error message describing the validation failure
        """
        self.message = message
        super().__init__(self.message)
