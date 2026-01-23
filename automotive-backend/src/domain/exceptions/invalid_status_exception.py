"""Business exception for invalid status operations."""


class InvalidStatusException(Exception):
    """Exception raised when status update violates business rules."""

    def __init__(self, message: str = "Estado inválido") -> None:
        """
        Initialize InvalidStatusException.

        Args:
            message: Error message describing the validation failure
        """
        self.message = message
        super().__init__(self.message)
