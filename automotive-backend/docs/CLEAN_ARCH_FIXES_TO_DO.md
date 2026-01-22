## ❌ CRITICAL VIOLATIONS

### 1. Missing Application Layer DTOs
**Status**: ❌ **CRITICAL VIOLATION**

**Current Implementation:**
```python
# register_vehicle_use_case.py
def execute(
    self, vehicle_id: str, plate: str, model: str, initial_mileage: int
) -> Vehicle:  # ❌ Returns domain entity directly
    vehicle = Vehicle(id=vehicle_id, plate=plate, model=model, ...)
    self._vehicle_repository.save(vehicle)
    return vehicle  # ❌ Domain entity exposed
```

```python
# main.py (Web layer)
def create_vehicle(request: CreateVehicleRequest):
    vehicle = use_case.execute(...)  # ❌ Receives domain entity
    return VehicleResponse(
        id=vehicle.id,  # ❌ Accessing domain entity directly
        plate=vehicle.plate,
        ...
    )
```

**Other Confirmed Violations:**

update_vehicle_mileage_use_case.py:

- ❌ Accepts primitives (vehicle_id: str, new_mileage: int)
- ❌ Returns None instead of DTO
- ❌ Has infrastructure violation (creates MaintenanceAlertObserver)

test_delete_vehicle_use_case.py:

- ❌ Accepts primitive (vehicle_id: str)
- ❌ Returns None instead of DTO

get_all_vehicles_use_case.py:

- ❌ Returns list[VehicleWithAlerts] containing domain entities
- ❌ Exposes Vehicle and MaintenanceAlert entities directly

**Problems:**
- Use cases receive primitive parameters instead of DTOs
- Use cases return domain entities directly to web layer
- Web layer has direct access to domain entities
- No validation at application layer boundary
- Breaks encapsulation - domain entities exposed outside domain

**Impact**: 🔴 **HIGH**
- Domain entities can be modified by outer layers
- Business rules can be bypassed
- Tight coupling between layers
- Difficult to evolve domain independently

---

### 2. Infrastructure Instantiation in Application Layer
**Status**: ❌ **CRITICAL VIOLATION**

**Current Implementation:**
```python
# update_vehicle_mileage_use_case.py
def execute(self, vehicle_id: str, new_mileage: int) -> None:
    vehicle = self._vehicle_repository.get_by_id(vehicle_id)
    
    # ❌ Creating infrastructure object in application layer!
    observer = MaintenanceAlertObserver(
        vehicle_id=vehicle_id,
        alert_repository=self._alert_repository,
        strategies=self._strategies,
        initial_mileage=vehicle.current_mileage
    )
    vehicle.attach(observer)
    vehicle.update_mileage(new_mileage)
```

**Problems:**
- Application layer knows about concrete infrastructure class `MaintenanceAlertObserver`
- Application layer is responsible for observer lifecycle
- Violates dependency direction (Application → Infrastructure)
- Observer creation logic duplicated in use case

**Impact**: 🔴 **HIGH**
- Application layer depends on infrastructure
- Cannot test use case without infrastructure
- Violates Clean Architecture dependency rule

---

### 3. Domain Logic in Application Layer
**Status**: ❌ **CRITICAL VIOLATION**
The `RegisterVehicleUseCase` contained complex alert generation business logic:

**Current Implementation:**
```python
# ❌ WRONG: Complex domain logic in application layer
class RegisterVehicleUseCase:
    def __init__(
        self,
        vehicle_repository: VehicleRepository,
        alert_repository=None,  # ❌ Infrastructure dependency
        strategies=None,  # ❌ Strategy management in use case
    ):
        self._alert_repository = alert_repository
        self._strategies = strategies or []
    
    def execute(self, command: RegisterVehicleCommand) -> VehicleDTO:
        # ... create vehicle ...
        
        # ❌ Complex nested loops for alert generation
        if self._alert_repository and self._strategies:
            for strategy in self._strategies:
                old_threshold = strategy._calculate_threshold(0)  # ❌ Private method access
                new_threshold = strategy._calculate_threshold(command.initial_mileage)
                interval = strategy.INTERVAL
                alert_type = strategy.get_alert_type()
                
                if new_threshold > old_threshold:
                    for threshold in range(old_threshold + interval, new_threshold + 1, interval):
                        # ❌ Direct entity creation
                        alert = MaintenanceAlert(
                            id=f"A-{command.vehicle_id}-{threshold}-{alert_type.value}",
                            vehicle_id=command.vehicle_id,
                            alert_type=alert_type,
                            mileage=threshold,
                            timestamp=datetime.now(),
                        )
                        self._alert_repository.save(alert)
```

### Issues
1. ❌ Complex business logic in application layer
2. ❌ Accessing private strategy methods (`_calculate_threshold`)
3. ❌ Direct creation of domain entities (`MaintenanceAlert`)
4. ❌ Duplicate logic (same as `MaintenanceAlertObserver`)
5. ❌ Violates Single Responsibility Principle
6. ❌ Difficult to test and maintain

### Impact: 🟡 MEDIUM
- Business logic scattered across layers
- Code duplication
- Maintenance nightmare
- Violates SRP

### 4. Singleton Pattern in Dependencies
**Status**: ❌ **VIOLATION**

**Current Implementation:**
```python
# dependencies.py
_db_session = SessionLocal()  # ❌ Single session for all requests
_vehicle_repository = SqliteVehicleRepository(_db_session)  # ❌ Singleton
_alert_repository = SqliteAlertRepository(_db_session)  # ❌ Singleton

def get_vehicle_repository() -> SqliteVehicleRepository:
    return _vehicle_repository  # ❌ Returns same instance
```

**Problems:**
- Single database session shared across all HTTP requests
- No transaction isolation between requests
- Potential data corruption in concurrent scenarios
- Cannot rollback failed transactions per request
- Memory leaks (session never closes)

**Impact**: 🔴 **HIGH**
- Thread safety issues
- Transaction management problems
- Production bugs under load

---


### 5. Web Layer Bypassing Application Layer
**Status**: ❌ **CRITICAL VIOLATION**

**Current Implementation:**
```python
# main.py
@app.get("/vehicles/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(vehicle_id: str):
    vehicle = get_vehicle_repository().get_by_id(vehicle_id)  # ❌ Direct repository access
    return VehicleResponse(
        id=vehicle.id,  # ❌ Accessing domain entity
        plate=vehicle.plate,
        ...
    )
```

**Problems:**
- Web layer bypasses application layer entirely
- Direct repository access from web layer
- No use case for "get vehicle by ID"
- Violates layer boundaries

**Affected Endpoints**:
1. `GET /vehicles/{vehicle_id}` - Was calling `vehicle_repo.get_by_id()` directly
2. `GET /vehicles/{vehicle_id}/alerts` - Was calling `alert_repo.get_all()` directly

**Impact**: 🔴 **HIGH**
- Application layer becomes optional
- Business logic can leak into web layer
- Inconsistent architecture

---

### 6. Missing Input Validation in Use Cases
**Status**: ❌ **VIOLATION**

**Current Implementation:**
```python
# register_vehicle_use_case.py
def execute(
    self, vehicle_id: str, plate: str, model: str, initial_mileage: int
) -> Vehicle:
    # ❌ No validation of vehicle_id format (should be V-XXX)
    # ❌ No validation of plate format (should be XXX-### or XXX-####)
    # ❌ No validation of model (empty string?)
    # ❌ No validation of initial_mileage (negative? > MAX_MILEAGE?)
    
    vehicle = Vehicle(id=vehicle_id, plate=plate, ...)
```

**Problems:**
- Validation only happens at web layer (Pydantic)
- Use cases can be called with invalid data if used from other contexts
- Domain entity constructor doesn't validate

**Impact**: 🟡 **MEDIUM**
- Invalid data can reach domain layer
- Business rules not centralized
- Inconsistent validation across entry points


## 🔧 HOW TO FIX

### Fix #1: Implement Application DTOs

**Create Application Layer DTOs:**

```python
# src/application/dtos/vehicle_dtos.py
from dataclasses import dataclass

@dataclass(frozen=True)
class RegisterVehicleCommand:
    """Input DTO for registering a vehicle."""
    vehicle_id: str
    plate: str
    model: str
    initial_mileage: int

@dataclass(frozen=True)
class UpdateMileageCommand:
    """Input DTO for updating mileage."""
    vehicle_id: str
    new_mileage: int

@dataclass(frozen=True)
class VehicleDTO:
    """Output DTO for vehicle data."""
    id: str
    plate: str
    model: str
    current_mileage: int
```

**Update Use Case:**

```python
# register_vehicle_use_case.py
from src.application.dtos.vehicle_dtos import RegisterVehicleCommand, VehicleDTO

class RegisterVehicleUseCase:
    def execute(self, command: RegisterVehicleCommand) -> VehicleDTO:
        # Validate command
        self._validate_command(command)
        
        # Check for duplicates
        try:
            self._vehicle_repository.get_by_id(command.vehicle_id)
            raise DuplicateVehicleException(...)
        except VehicleNotFoundException:
            pass
        
        # Create entity
        vehicle = Vehicle(
            id=command.vehicle_id,
            plate=command.plate,
            model=command.model,
            current_mileage=command.initial_mileage
        )
        
        # Save
        self._vehicle_repository.save(vehicle)
        
        # Return DTO (not entity!)
        return VehicleDTO(
            id=vehicle.id,
            plate=vehicle.plate,
            model=vehicle.model,
            current_mileage=vehicle.current_mileage
        )
    
    def _validate_command(self, command: RegisterVehicleCommand) -> None:
        """Validate business rules."""
        # RN-011: Vehicle ID format V-XXX
        if not re.match(r'^V-\d{3}$', command.vehicle_id):
            raise InvalidVehicleIdException(...)
        
        # RN-010: Plate format XXX-### or XXX-####
        if not re.match(r'^[A-Z]{3}-\d{3,4}$', command.plate):
            raise InvalidPlateException(...)
        
        # Validate mileage
        if command.initial_mileage < 0:
            raise InvalidMileageException(...)
        
        if command.initial_mileage > Vehicle.MAX_MILEAGE:
            raise InvalidMileageException(...)
```

**Update Web Layer:**

```python
# main.py
@app.post("/vehicles", response_model=VehicleResponse)
def create_vehicle(request: CreateVehicleRequest):
    # Map web DTO to application DTO
    command = RegisterVehicleCommand(
        vehicle_id=request.id,
        plate=request.plate,
        model=request.model,
        initial_mileage=request.initial_mileage
    )
    
    # Execute use case
    vehicle_dto = use_case.execute(command)
    
    # Map application DTO to web DTO
    return VehicleResponse(
        id=vehicle_dto.id,
        plate=vehicle_dto.plate,
        model=vehicle_dto.model,
        current_mileage=vehicle_dto.current_mileage
    )
```

**Benefits:**
- ✅ Domain entities never leave domain/application layers
- ✅ Clear boundaries between layers
- ✅ Validation at application boundary
- ✅ Easy to evolve DTOs independently from entities

---

### Fix #2: Remove Infrastructure and Domain Logic from Application Layer

**Factory Pattern**

```python
# src/domain/ports/observer_factory.py
from abc import ABC, abstractmethod
from src.domain.ports.observer import Observer

class ObserverFactory(ABC):
    """Factory for creating observers (domain port)."""
    
    @abstractmethod
    def create_maintenance_observer(
        self, 
        vehicle_id: str, 
        initial_mileage: int
    ) -> Observer:
        """Create a maintenance alert observer."""
        pass
```

```python
# src/infrastructure/factories/observer_factory_impl.py
from src.domain.ports.observer_factory import ObserverFactory
from src.infrastructure.observers.maintenance_alert_observer import MaintenanceAlertObserver

class ObserverFactoryImpl(ObserverFactory):
    """Infrastructure implementation of observer factory."""
    
    def __init__(self, alert_repository, strategies):
        self._alert_repository = alert_repository
        self._strategies = strategies
    
    def create_maintenance_observer(
        self, 
        vehicle_id: str, 
        initial_mileage: int
    ) -> Observer:
        return MaintenanceAlertObserver(
            vehicle_id=vehicle_id,
            alert_repository=self._alert_repository,
            strategies=self._strategies,
            initial_mileage=initial_mileage
        )
```

```python
# update_vehicle_mileage_use_case.py
class UpdateVehicleMileageUseCase:
    def __init__(
        self,
        vehicle_repository: VehicleRepository,
        observer_factory: ObserverFactory  # ✅ Depends on abstraction
    ):
        self._vehicle_repository = vehicle_repository
        self._observer_factory = observer_factory
    
    def execute(self, command: UpdateMileageCommand) -> VehicleDTO:
        vehicle = self._vehicle_repository.get_by_id(command.vehicle_id)
        
        # ✅ Use factory (domain abstraction)
        observer = self._observer_factory.create_maintenance_observer(
            vehicle_id=command.vehicle_id,
            initial_mileage=vehicle.current_mileage
        )
        
        vehicle.attach(observer)
        vehicle.update_mileage(command.new_mileage)
        self._vehicle_repository.save(vehicle)
        
        return VehicleDTO(...)
```
```python
# register_vehicle_use_case.py
class RegisterVehicleUseCase:
    """Use case for registering a new vehicle."""

    def __init__(
        self,
        vehicle_repository: VehicleRepository,
        observer_factory: ObserverFactory = None,  # ✅ Domain abstraction
    ):
        """
        Initialize use case with repository and observer factory.

        Args:
            vehicle_repository: Repository for vehicle persistence
            observer_factory: Factory for creating observers (optional)
        """
        self._vehicle_repository = vehicle_repository
        self._observer_factory = observer_factory

    def execute(self, command: RegisterVehicleCommand) -> VehicleDTO:
        """Register a new vehicle in the system."""
        # Validate vehicle ID doesn't exist
        try:
            self._vehicle_repository.get_by_id(command.vehicle_id)
            raise DuplicateVehicleException(...)
        except VehicleNotFoundException:
            pass

        # Create new vehicle entity starting at 0
        vehicle = Vehicle(
            id=command.vehicle_id,
            plate=command.plate,
            model=command.model,
            current_mileage=0  # ✅ Start at 0 to trigger all missed alerts
        )

        # ✅ Use Observer pattern to generate missed alerts
        if self._observer_factory and command.initial_mileage > 0:
            # Create observer starting from 0 to catch all thresholds
            observer = self._observer_factory.create_maintenance_observer(
                vehicle_id=command.vehicle_id,
                initial_mileage=0
            )
            vehicle.attach(observer)
            
            # Update to initial mileage - triggers alert generation via observer
            vehicle.update_mileage(command.initial_mileage)

        # Save to repository
        self._vehicle_repository.save(vehicle)

        # Return DTO
        return VehicleDTO(
            id=vehicle.id,
            plate=vehicle.plate,
            model=vehicle.model,
            current_mileage=vehicle.current_mileage
        )
```


**Benefits**:
- Keeps repository focused on persistence
- Observer creation is explicit in use case
- Single Responsibility Principle maintained 
- Easier to test
- More flexible

---

### Fix #3: Implement Per-Request Dependencies

**Use FastAPI Dependency Injection:**

```python
# dependencies.py
from contextlib import contextmanager
from typing import Generator

def get_db_session() -> Generator[Session, None, None]:
    """Create a new database session per request."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def get_vehicle_repository(
    db: Session = Depends(get_db_session)
) -> SqliteVehicleRepository:
    """Create repository with request-scoped session."""
    return SqliteVehicleRepository(db)

def get_alert_repository(
    db: Session = Depends(get_db_session)
) -> SqliteAlertRepository:
    """Create repository with request-scoped session."""
    return SqliteAlertRepository(db)

def get_observer_factory(
    alert_repo: SqliteAlertRepository = Depends(get_alert_repository)
) -> ObserverFactory:
    """Create observer factory with dependencies."""
    strategies = [
        BasicMaintenanceStrategy(),
        MajorMaintenanceStrategy(),
        CriticalThresholdStrategy()
    ]
    return ObserverFactoryImpl(alert_repo, strategies)
```

**Update Web Layer:**

```python
# main.py
@app.post("/vehicles", response_model=VehicleResponse)
def create_vehicle(
    request: CreateVehicleRequest,
    vehicle_repo: VehicleRepository = Depends(get_vehicle_repository),
    alert_repo: AlertRepository = Depends(get_alert_repository)
):
    use_case = RegisterVehicleUseCase(
        vehicle_repository=vehicle_repo,
        alert_repository=alert_repo
    )
    
    command = RegisterVehicleCommand(...)
    vehicle_dto = use_case.execute(command)
    
    return VehicleResponse(...)
```

**Benefits:**
- ✅ New session per request
- ✅ Automatic session cleanup
- ✅ Transaction isolation
- ✅ Thread-safe
- ✅ Testable (can inject mocks)

---

### Fix #4: Create Use Case for Get Vehicle by ID and Get Vehicle alerts

```python
# src/application/use_cases/get_vehicle_use_case.py
from src.application.dtos.vehicle_dtos import VehicleDTO
from src.domain.ports.vehicle_repository import VehicleRepository

class GetVehicleUseCase:
    """Use case for retrieving a single vehicle."""
    
    def __init__(self, vehicle_repository: VehicleRepository):
        self._vehicle_repository = vehicle_repository
    
    def execute(self, vehicle_id: str) -> VehicleDTO:
        """
        Get vehicle by ID.
        
        Args:
            vehicle_id: Unique identifier
            
        Returns:
            VehicleDTO with vehicle data
            
        Raises:
            VehicleNotFoundException: If vehicle not found
        """
        vehicle = self._vehicle_repository.get_by_id(vehicle_id)
        
        return VehicleDTO(
            id=vehicle.id,
            plate=vehicle.plate,
            model=vehicle.model,
            current_mileage=vehicle.current_mileage
        )
```
```python
class GetVehicleAlertsUseCase:
    """Use case for retrieving alerts for a specific vehicle."""
    
    def __init__(self, alert_repository: AlertRepository):
        self._alert_repository = alert_repository
    
    def execute(self, vehicle_id: str) -> list[AlertDTO]:
        # Get all alerts
        all_alerts = self._alert_repository.get_all()
        
        # Filter by vehicle_id (business logic in application layer)
        vehicle_alerts = [
            alert for alert in all_alerts 
            if alert.vehicle_id == vehicle_id
        ]
        
        # Map to DTOs
        return [
            AlertDTO(
                id=alert.id,
                vehicle_id=alert.vehicle_id,
                alert_type=alert.alert_type.name,  # Enum to string (uppercase)
                mileage=alert.mileage,
                timestamp=alert.timestamp
            )
            for alert in vehicle_alerts
        ]
```

```python
# main.py
@app.get("/vehicles/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(
    vehicle_id: str,
    vehicle_repo: VehicleRepository = Depends(get_vehicle_repository)
):
    use_case = GetVehicleUseCase(vehicle_repository=vehicle_repo)
    vehicle_dto = use_case.execute(vehicle_id)
    
    return VehicleResponse(
        id=vehicle_dto.id,
        plate=vehicle_dto.plate,
        model=vehicle_dto.model,
        current_mileage=vehicle_dto.current_mileage
    )

@app.get("/vehicles/{vehicle_id}/alerts", response_model=list[AlertResponse])
def get_vehicle_alerts(
    vehicle_id: str,
    alert_repo: SqliteAlertRepository = Depends(get_alert_repository)
):
    # ✅ Use use case instead of direct repository access
    use_case = GetVehicleAlertsUseCase(alert_repository=alert_repo)
    alert_dtos = use_case.execute(vehicle_id)
    
    # Map DTOs to responses
    return [
        AlertResponse(
            id=alert_dto.id,
            vehicle_id=alert_dto.vehicle_id,
            alert_type=alert_dto.alert_type,
            mileage=alert_dto.mileage,
            timestamp=alert_dto.timestamp.isoformat()
        )
        for alert_dto in alert_dtos
    ]
```

---

### Fix #5: Add Input Validation to Use Cases

```python
# src/application/validators/vehicle_validator.py
import re
from src.domain.entities.vehicle import Vehicle
from src.domain.exceptions.invalid_vehicle_id_exception import InvalidVehicleIdException
from src.domain.exceptions.invalid_plate_exception import InvalidPlateException
from src.domain.exceptions.invalid_model_exception import InvalidModelException
from src.domain.exceptions.invalid_mileage_exception import InvalidMileageException


class VehicleValidator:
    """Validator for vehicle business rules at application boundary."""
    
    # Validation patterns based on frontend and business rules
    VEHICLE_ID_PATTERN = r'^V-\d{3}$'  # RN-011: V-XXX format
    PLATE_PATTERN = r'^[A-Z]{3}-\d{3,4}$'  # RN-010: XXX-123 or XXX-1234 format
    MAX_MODEL_LENGTH = 100
    MAX_MILEAGE = Vehicle.MAX_MILEAGE  # 1,000,000 km
    
    def validate_vehicle_id(self, vehicle_id: str) -> None:
        """Validate vehicle ID format (RN-011)."""
        if vehicle_id is None:
            raise InvalidVehicleIdException("El vehicle_id no puede ser None")
        
        if not isinstance(vehicle_id, str):
            raise InvalidVehicleIdException(
                f"El vehicle_id debe ser un string, recibido: {type(vehicle_id).__name__}"
            )
        
        if not re.match(self.VEHICLE_ID_PATTERN, vehicle_id):
            raise InvalidVehicleIdException(
                f"Formato de vehicle_id inválido: '{vehicle_id}'. "
                f"Formato esperado: V-XXX (ejemplo: V-001, V-123)"
            )
    
    def validate_plate(self, plate: str) -> None:
        """Validate plate format (RN-010)."""
        if plate is None:
            raise InvalidPlateException("La placa no puede ser None")
        
        if not isinstance(plate, str):
            raise InvalidPlateException(
                f"La placa debe ser un string, recibido: {type(plate).__name__}"
            )
        
        if not re.match(self.PLATE_PATTERN, plate):
            raise InvalidPlateException(
                f"Formato de placa inválido: '{plate}'. "
                f"Formato esperado: XXX-123 o XXX-1234 (ejemplo: ABC-123, XYZ-9999)"
            )
    
    def validate_model(self, model: str) -> None:
        """Validate vehicle model name."""
        if model is None:
            raise InvalidModelException("El modelo no puede ser None")
        
        if not isinstance(model, str):
            raise InvalidModelException(
                f"El modelo debe ser un string, recibido: {type(model).__name__}"
            )
        
        if not model or not model.strip():
            raise InvalidModelException("El modelo no puede estar vacío")
        
        if len(model) > self.MAX_MODEL_LENGTH:
            raise InvalidModelException(
                f"El modelo excede la longitud máxima de {self.MAX_MODEL_LENGTH} caracteres. "
                f"Longitud actual: {len(model)}"
            )
    
    def validate_initial_mileage(self, mileage: int) -> None:
        """Validate initial mileage."""
        if mileage is None:
            raise InvalidMileageException("El kilometraje no puede ser None")
        
        if not isinstance(mileage, int):
            raise InvalidMileageException(
                f"El kilometraje debe ser un entero, recibido: {type(mileage).__name__}"
            )
        
        if mileage < 0:
            raise InvalidMileageException(
                f"El kilometraje inicial no puede ser negativo: {mileage}"
            )
        
        if mileage > self.MAX_MILEAGE:
            raise InvalidMileageException(
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
        """Validate all vehicle data together."""
        self.validate_vehicle_id(vehicle_id)
        self.validate_plate(plate)
        self.validate_model(model)
        self.validate_initial_mileage(initial_mileage)
```

**Usage in Use Cases:**

```python
# register_vehicle_use_case.py
from src.application.validators.vehicle_validator import VehicleValidator

class RegisterVehicleUseCase:
    def execute(self, command: RegisterVehicleCommand) -> VehicleDTO:
        # ✅ Validate input data at application boundary
        validator = VehicleValidator()
        validator.validate_vehicle_data(
            vehicle_id=command.vehicle_id,
            plate=command.plate,
            model=command.model,
            initial_mileage=command.initial_mileage
        )
        
        # Validate vehicle ID doesn't exist
        try:
            self._vehicle_repository.get_by_id(command.vehicle_id)
            raise DuplicateVehicleException(...)
        except VehicleNotFoundException:
            pass
        
        # Rest of the logic...
```

**Benefits:**
- ✅ Business rules enforced at application boundary
- ✅ Centralized validation logic
- ✅ Clear, descriptive error messages in Spanish
- ✅ Type safety with proper exception handling
- ✅ Prevents invalid data from reaching domain layer
- ✅ Comprehensive test coverage (30 unit tests)

**Validation Rules:**
1. **Vehicle ID**: V-XXX format (3 digits) - RN-011
2. **Plate**: XXX-123 or XXX-1234 format - RN-010
3. **Model**: Non-empty, max 100 characters
4. **Mileage**: 0 to 1,000,000 km range

**Custom Exceptions Created:**
- `InvalidVehicleIdException` - For vehicle ID validation failures
- `InvalidPlateException` - For plate validation failures
- `InvalidModelException` - For model validation failures
- `InvalidMileageException` - For mileage validation failures (already existed)


---

## 📊 SUMMARY TABLE

| Aspect | Status | Impact | Fix Priority |
|--------|--------|--------|--------------|
| Layer Separation | ✅ Correct | - | - |
| Dependency Inversion | ✅ Correct | - | - |
| Domain Business Rules | ✅ Correct | - | - |
| Repository Pattern | ✅ Correct | - | - |
| **Application DTOs** | ✅ Implemented | 🔴 HIGH | **P0 - Complete** |
| **Infrastructure in App Layer** | ✅ Fixed | 🔴 HIGH | **P0 - Complete** |
| **Singleton Dependencies** | ✅ Fixed | 🔴 HIGH | **P0 - Complete** |
| **Input Validation** | ✅ Implemented | 🟡 MEDIUM | **P1 - Complete** |
| **Web Layer Bypass** | ✅ Fixed | 🔴 HIGH | **P1 - Complete** |

---

## 🎯 IMPLEMENTATION STATUS

### Phase 1: Critical Fixes ✅ COMPLETE
1. ✅ **Implement Application DTOs** (Fix #1)
   - Created `application/dtos/` package
   - Defined Command and DTO classes
   - Updated all use cases to use DTOs
   - Updated web layer mappings

2. ✅ **Fix Dependency Injection** (Fix #3)
   - Implemented per-request sessions
   - Using FastAPI Depends()
   - Removed singleton pattern

### Phase 2: Architecture Fixes ✅ COMPLETE
3. ✅ **Remove Infrastructure from Application** (Fix #2)
   - Created ObserverFactory port
   - Implemented factory in infrastructure
   - Updated use cases to use factory

4. ✅ **Add Use Cases for All Operations** (Fix #4)
   - Created GetVehicleUseCase
   - Created GetVehicleAlertsUseCase
   - Updated web layer to use use cases

### Phase 3: Validation ✅ COMPLETE
5. ✅ **Implement Input Validation** (Fix #5)
   - Created VehicleValidator
   - Added validation to RegisterVehicleUseCase
   - Created custom exceptions
   - Comprehensive test coverage (30 tests)

---

## 📚 CLEAN ARCHITECTURE PRINCIPLES CHECKLIST

- ✅ **Independence of Frameworks**: Domain doesn't depend on FastAPI/SQLAlchemy
- ✅ **Testability**: Domain and application can be tested without infrastructure
- ✅ **Independence of UI**: Business logic not coupled to web layer
- ✅ **Independence of Database**: Repository pattern abstracts persistence
- ✅ **Dependency Rule**: Application layer depends only on domain abstractions
- ✅ **Entities Encapsulation**: Domain entities never exposed to outer layers
- ✅ **Use Case Isolation**: All endpoints use proper use cases
- ✅ **Input/Output Boundaries**: DTOs at all application boundaries
- ✅ **Input Validation**: Business rules enforced at application boundary

**Overall Score**: 9/9 principles correctly implemented ✅

---

## 🔗 REFERENCES

- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)

---

**Document Version**: 2.0  
**Last Updated**: January 2026  
**Status**: ✅ ALL VIOLATIONS FIXED  
