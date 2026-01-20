"""Exception for duplicate vehicle registration."""


class DuplicateVehicleException(Exception):
    """Raised when attempting to register a vehicle with existing ID or plate."""

    pass
