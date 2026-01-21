# Clean Architecture Analysis - Automotive Backend

## Executive Summary

The backend implements Clean Architecture with **proper layer separation** and **Dependency Inversion Principle (DIP)**. However, there are **critical violations** that break the architecture's core principles:

1. ❌ **Missing Application DTOs** - Use cases receive/return primitives or domain entities
2. ❌ **Domain entities exposed to Web layer** - Violates encapsulation
3. ❌ **Infrastructure concerns in Application layer** - Observer instantiation in use case
4. ❌ **Singleton pattern in dependencies** - Breaks per-request isolation
5. ❌ **Missing input validation** - Business rules not enforced in use cases

---

## ✅ CORRECT IMPLEMENTATIONS

### 1. Layer Separation (Domain, Application, Infrastructure, Web)
**Status**: ✅ CORRECT

```
src/
├── domain/           # Business logic & rules
│   ├── entities/
│   ├── ports/
│   ├── exceptions/
│   └── strategies/
├── application/      # Use cases (orchestration)
│   └── use_cases/
├── infrastructure/   # External concerns (DB, observers)
│   ├── database/
│   ├── repositories/
│   └── observers/
└── web/             # HTTP layer (FastAPI)
```

**Why it's correct**: Clear separation of concerns with no circular dependencies.

---

### 2. Dependency Inversion Principle (DIP)
**Status**: ✅ CORRECT

```python
# Domain defines the interface (port)
class VehicleRepository(ABC):
    @abstractmethod
    def save(self, vehicle: Vehicle) -> None:
        pass
```

```python
# Infrastructure implements it
class SqliteVehicleRepository(VehicleRepository):
    def save(self, vehicle: Vehicle) -> None:
        # SQLite implementation
```

```python
# Application depends on abstraction
class RegisterVehicleUseCase:
    def __init__(self, vehicle_repository: VehicleRepository):
        self._vehicle_repository = vehicle_repository
```

**Why it's correct**: Application layer depends on domain abstractions, not concrete implementations. Infrastructure provides the concrete implementation.

---

### 3. Domain Entity Business Rules
**Status**: ✅ CORRECT

```python
# vehicle.py
class Vehicle:
    MAX_MILEAGE = 1_000_000
    MAX_MILEAGE_INCREMENT = 50_000
    
    def update_mileage(self, new_mileage: int) -> None:
        if new_mileage <= self.current_mileage:
            raise InvalidMileageException(...)
        
        if new_mileage > self.MAX_MILEAGE:
            raise InvalidMileageException(...)
```

**Why it's correct**: Business rules are encapsulated in domain entities, not scattered across layers.

---

### 4. Repository Pattern
**Status**: ✅ CORRECT

```python
# sqlite_vehicle_repository.py
def _to_entity(self, vehicle_model: VehicleModel) -> Vehicle:
    return Vehicle(
        id=vehicle_model.id,
        plate=vehicle_model.plate,
        model=vehicle_model.model,
        current_mileage=vehicle_model.current_mileage,
    )

def _to_model(self, vehicle: Vehicle) -> VehicleModel:
    return VehicleModel(
        id=vehicle.id,
        plate=vehicle.plate,
        model=vehicle.model,
        current_mileage=vehicle.current_mileage,
    )
```

**Why it's correct**: Repository handles mapping between domain entities and persistence models. Domain entities never know about database concerns.

---

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

### 3. Singleton Pattern in Dependencies
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

### Fix #2: Remove Infrastructure from Application Layer

**Option A: Factory Pattern (Recommended)**

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

**Option B: Pre-configured Entity (Alternative)**

```python
# src/domain/ports/vehicle_repository.py
class VehicleRepository(ABC):
    @abstractmethod
    def get_by_id_with_observers(self, vehicle_id: str) -> Vehicle:
        """Get vehicle with observers already attached."""
        pass
```

```python
# sqlite_vehicle_repository.py
def get_by_id_with_observers(self, vehicle_id: str) -> Vehicle:
    vehicle_model = self._get_vehicle_model_or_raise(vehicle_id)
    vehicle = self._to_entity(vehicle_model)
    
    # Attach observers before returning
    observer = MaintenanceAlertObserver(...)
    vehicle.attach(observer)
    
    return vehicle
```

```python
# update_vehicle_mileage_use_case.py
def execute(self, command: UpdateMileageCommand) -> VehicleDTO:
    # ✅ Vehicle comes with observers already attached
    vehicle = self._vehicle_repository.get_by_id_with_observers(command.vehicle_id)
    vehicle.update_mileage(command.new_mileage)
    self._vehicle_repository.save(vehicle)
    return VehicleDTO(...)
```

**Recommendation**: Use **Option A (Factory Pattern)** because:
- Keeps repository focused on persistence
- Observer creation is explicit in use case
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

## 📊 SUMMARY TABLE

| Aspect | Status | Impact | Fix Priority |
|--------|--------|--------|--------------|
| Layer Separation | ✅ Correct | - | - |
| Dependency Inversion | ✅ Correct | - | - |
| Domain Business Rules | ✅ Correct | - | - |
| Repository Pattern | ✅ Correct | - | - |
| **Application DTOs** | ❌ Missing | 🔴 HIGH | **P0 - Critical** |
| **Infrastructure in App Layer** | ❌ Violation | 🔴 HIGH | **P0 - Critical** |
| **Singleton Dependencies** | ❌ Violation | 🔴 HIGH | **P0 - Critical** |
| **Input Validation** | ❌ Missing | 🟡 MEDIUM | **P1 - Important** |
| **Web Layer Bypass** | ❌ Violation | 🔴 HIGH | **P1 - Important** |

---

## 🎯 RECOMMENDED IMPLEMENTATION ORDER

### Phase 1: Critical Fixes (Week 1)
1. **Implement Application DTOs** (Fix #1)
   - Create `application/dtos/` package
   - Define Command and DTO classes
   - Update all use cases to use DTOs
   - Update web layer mappings

2. **Fix Dependency Injection** (Fix #3)
   - Implement per-request sessions
   - Use FastAPI Depends()
   - Remove singleton pattern

### Phase 2: Architecture Fixes (Week 2)
3. **Remove Infrastructure from Application** (Fix #2)
   - Create ObserverFactory port
   - Implement factory in infrastructure
   - Update use cases to use factory

4. **Add Use Cases for All Operations** (Fix #5)
   - Create GetVehicleUseCase
   - Create GetAllVehiclesUseCase
   - Update web layer to use use cases

### Phase 3: Validation (Week 3)
5. **Implement Input Validation** (Fix #4)
   - Create VehicleValidator
   - Add validation to all use cases
   - Add custom exceptions

---

## 📚 CLEAN ARCHITECTURE PRINCIPLES CHECKLIST

- ✅ **Independence of Frameworks**: Domain doesn't depend on FastAPI/SQLAlchemy
- ✅ **Testability**: Domain and application can be tested without infrastructure
- ✅ **Independence of UI**: Business logic not coupled to web layer
- ✅ **Independence of Database**: Repository pattern abstracts persistence
- ❌ **Dependency Rule**: Application layer depends on infrastructure (observer)
- ❌ **Entities Encapsulation**: Domain entities exposed to outer layers
- ❌ **Use Case Isolation**: Web layer bypasses use cases in some endpoints
- ❌ **Input/Output Boundaries**: Missing DTOs at application boundaries

**Overall Score**: 5/9 principles correctly implemented

---

## 🔗 REFERENCES

- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)

---

**Document Version**: 1.0  
**Last Updated**: January 2026  
**Author**: Architecture Review Team
