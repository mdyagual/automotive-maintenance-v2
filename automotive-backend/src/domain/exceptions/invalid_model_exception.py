"""Exception for invalid vehicle model."""


class InvalidModelException(Exception):
    """Raised when vehicle model is invalid."""

    def __init__(self, message: str = "El modelo es inválido") -> None:
        """
        Initialize InvalidModelException.

        Args:
            message: Error message describing the validation failure
        """
        self.message = message
        super().__init__(self.message)
