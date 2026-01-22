"""Exception for invalid license plate format."""


class InvalidPlateException(Exception):
    """Raised when license plate format is invalid."""

    def __init__(self, message: str = "Formato de placa inválido") -> None:
        """
        Initialize InvalidPlateException.

        Args:
            message: Error message describing the validation failure
        """
        self.message = message
        super().__init__(self.message)
