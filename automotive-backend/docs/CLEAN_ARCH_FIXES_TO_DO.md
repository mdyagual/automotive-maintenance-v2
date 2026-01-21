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

**Functional Tests**: `tests/architecture/test_singleton_dependency_violation.py`
- ✅ 13 behavioral tests demonstrating the violation
- ✅ Tests show real-world impact (data corruption, memory leaks, transaction issues)
- ✅ All tests currently FAIL (as expected with violation)
- ✅ Tests will PASS after implementing per-request dependencies

**Test Documentation**: `SINGLETON_DEPENDENCY_VIOLATION_TESTS.md`

---

### 4. Missing Input Validation in Use Cases
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
- Business rules from DESIGN.md not enforced (RN-010, RN-011)
- Validation only happens at web layer (Pydantic)
- Use cases can be called with invalid data if used from other contexts
- Domain entity constructor doesn't validate

**Impact**: 🟡 **MEDIUM**
- Invalid data can reach domain layer
- Business rules not centralized
- Inconsistent validation across entry points

---

### 5. Domain Entities Exposed to Web Layer
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

**Impact**: 🔴 **HIGH**
- Application layer becomes optional
- Business logic can leak into web layer
- Inconsistent architecture

---

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

### Fix #4: Add Input Validation to Use Cases

```python
# src/application/validators/vehicle_validator.py
import re
from src.domain.entities.vehicle import Vehicle
from src.domain.exceptions.invalid_vehicle_id_exception import InvalidVehicleIdException
from src.domain.exceptions.invalid_plate_exception import InvalidPlateException

class VehicleValidator:
    """Validator for vehicle business rules."""
    
    VEHICLE_ID_PATTERN = r'^V-\d{3}$'  # RN-011
    PLATE_PATTERN = r'^[A-Z]{3}-\d{3,4}$'  # RN-010
    
    @staticmethod
    def validate_vehicle_id(vehicle_id: str) -> None:
        """Validate vehicle ID format (RN-011)."""
        if not re.match(VehicleValidator.VEHICLE_ID_PATTERN, vehicle_id):
            raise InvalidVehicleIdException(
                f"ID de vehículo inválido: {vehicle_id}. "
                f"Formato esperado: V-XXX (ej: V-123)"
            )
    
    @staticmethod
    def validate_plate(plate: str) -> None:
        """Validate plate format (RN-010)."""
        if not re.match(VehicleValidator.PLATE_PATTERN, plate.upper()):
            raise InvalidPlateException(
                f"Placa inválida: {plate}. "
                f"Formato esperado: XXX-### o XXX-#### (ej: ABC-123)"
            )
    
    @staticmethod
    def validate_initial_mileage(mileage: int) -> None:
        """Validate initial mileage."""
        if mileage < 0:
            raise InvalidMileageException(
                f"El kilometraje inicial no puede ser negativo: {mileage}"
            )
        
        if mileage > Vehicle.MAX_MILEAGE:
            raise InvalidMileageException(
                f"El kilometraje inicial {mileage:,} excede el máximo "
                f"permitido de {Vehicle.MAX_MILEAGE:,} km"
            )
```

```python
# register_vehicle_use_case.py
class RegisterVehicleUseCase:
    def execute(self, command: RegisterVehicleCommand) -> VehicleDTO:
        # ✅ Validate at application boundary
        VehicleValidator.validate_vehicle_id(command.vehicle_id)
        VehicleValidator.validate_plate(command.plate)
        VehicleValidator.validate_initial_mileage(command.initial_mileage)
        
        # Rest of the logic...
```

---

### Fix #5: Create Use Case for Get Vehicle

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
```

---