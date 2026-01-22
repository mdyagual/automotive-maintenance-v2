"""Vehicle validator for application layer input validation."""

import re
from src.domain.entities.vehicle import Vehicle


class VehicleValidator:
    """Validator for vehicle business rules at application boundary."""
    
    # Validation patterns based on frontend and business rules
    VEHICLE_ID_PATTERN = r'^V-\d{3}$'  # V-XXX format (e.g., V-001, V-123)
    PLATE_PATTERN = r'^[A-Z]{3}-\d{3,4}$'  # XXX-123 or XXX-1234 format
    MAX_MODEL_LENGTH = 100
    MAX_MILEAGE = Vehicle.MAX_MILEAGE  # 1,000,000 km
    
    def validate_vehicle_id(self, vehicle_id: str) -> None:
        """
        Validate vehicle ID format.
        
        Valid format: V-XXX where XXX is exactly 3 digits.
        Examples: V-001, V-123, V-999
        
        Args:
            vehicle_id: Vehicle identifier to validate
            
        Raises:
            ValueError: If vehicle_id format is invalid
            TypeError: If vehicle_id is None
        """
        if vehicle_id is None:
            raise TypeError("El vehicle_id no puede ser None")
        
        if not isinstance(vehicle_id, str):
            raise TypeError(f"El vehicle_id debe ser un string, recibido: {type(vehicle_id).__name__}")
        
        if not re.match(self.VEHICLE_ID_PATTERN, vehicle_id):
            raise ValueError(
                f"Formato de vehicle_id inválido: '{vehicle_id}'. "
                f"Formato esperado: V-XXX (ejemplo: V-001, V-123)"
            )
    
    def validate_plate(self, plate: str) -> None:
        """
        Validate license plate format.
        
        Valid formats:
        - XXX-123 (3 uppercase letters, hyphen, 3 digits)
        - XXX-1234 (3 uppercase letters, hyphen, 4 digits)
        
        Examples: ABC-123, XYZ-9999, DEF-001
        
        Args:
            plate: License plate to validate
            
        Raises:
            ValueError: If plate format is invalid
            TypeError: If plate is None
        """
        if plate is None:
            raise TypeError("La placa no puede ser None")
        
        if not isinstance(plate, str):
            raise TypeError(f"La placa debe ser un string, recibido: {type(plate).__name__}")
        
        if not re.match(self.PLATE_PATTERN, plate):
            raise ValueError(
                f"Formato de placa inválido: '{plate}'. "
                f"Formato esperado: XXX-123 o XXX-1234 (ejemplo: ABC-123, XYZ-9999)"
            )
    
    def validate_model(self, model: str) -> None:
        """
        Validate vehicle model name.
        
        Valid models:
        - Non-empty strings
        - Can contain letters, numbers, spaces
        - Maximum length of 100 characters
        
        Args:
            model: Vehicle model name to validate
            
        Raises:
            ValueError: If model is invalid
            TypeError: If model is None
        """
        if model is None:
            raise TypeError("El modelo no puede ser None")
        
        if not isinstance(model, str):
            raise TypeError(f"El modelo debe ser un string, recibido: {type(model).__name__}")
        
        if not model or not model.strip():
            raise ValueError("El modelo no puede estar vacío")
        
        if len(model) > self.MAX_MODEL_LENGTH:
            raise ValueError(
                f"El modelo excede la longitud máxima de {self.MAX_MODEL_LENGTH} caracteres. "
                f"Longitud actual: {len(model)}"
            )
    
    def validate_initial_mileage(self, mileage: int) -> None:
        """
        Validate initial mileage value.
        
        Valid range: 0 to 1,000,000 km (inclusive)
        
        Args:
            mileage: Initial mileage value to validate
            
        Raises:
            ValueError: If mileage is out of valid range
            TypeError: If mileage is None or not an integer
        """
        if mileage is None:
            raise TypeError("El kilometraje no puede ser None")
        
        if not isinstance(mileage, int):
            raise TypeError(f"El kilometraje debe ser un entero, recibido: {type(mileage).__name__}")
        
        if mileage < 0:
            raise ValueError(
                f"El kilometraje inicial no puede ser negativo: {mileage}"
            )
        
        if mileage > self.MAX_MILEAGE:
            raise ValueError(
                f"El kilometraje inicial {mileage:,} km excede el máximo "
                f"permitido de {self.MAX_MILEAGE:,} km"
            )
    
    def validate_vehicle_data(
        self,
        vehicle_id: str,
        plate: str,
        model: str,
        initial_mileage: int
    ) -> None:
        """
        Validate all vehicle data together.
        
        This method validates all fields in sequence, raising an exception
        on the first validation failure.
        
        Args:
            vehicle_id: Vehicle identifier
            plate: License plate
            model: Vehicle model name
            initial_mileage: Initial mileage value
            
        Raises:
            ValueError: If any field is invalid
            TypeError: If any field is None or wrong type
        """
        self.validate_vehicle_id(vehicle_id)
        self.validate_plate(plate)
        self.validate_model(model)
        self.validate_initial_mileage(initial_mileage)
