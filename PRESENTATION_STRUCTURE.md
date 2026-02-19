# 🚗 Automotive Fleet Management System - Presentation Structure

Based on the project documentation and current status, here's a comprehensive presentation structure:

---

## **Min 0-2: Contexto y Desafío de Negocio**

### Slide 1: El Problema
**"Gestión Manual de Mantenimiento Vehicular"**
- Flotas vehiculares sin sistema automatizado de alertas
- Mantenimientos preventivos olvidados → costos elevados
- Falta de visibilidad del estado operativo de la flota
- Búsqueda manual de vehículos por registros físicos

### Slide 2: La Solución
**"Sistema Inteligente de Gestión de Flota"**
- ✅ Registro de kilometraje
- ✅ Alertas preventivas (10k, 50k, 100k km)
- ✅ Dashboard en tiempo real
- ✅ Gestión de estados operativos (activo, inactivo,  mantenimiento, retirado)
- ✅ Búsqueda rápida por placa

**Valor de Negocio:**
- Reducción de costos de mantenimiento correctivo
- Mayor disponibilidad de vehículos
- Trazabilidad completa del historial

---

## **Min 2-10: "Deep Dive" de Ingeniería**

### Slide 3: Arquitectura del Sistema (1 min)
**"Clean Architecture + Hexagonal"**

```
┌─────────────────────────────────────────┐
│         WEB LAYER (FastAPI)             │
│  - REST API endpoints                   │
│  - DTOs de entrada/salida               │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      APPLICATION LAYER                  │
│  - Use Cases (casos de uso)             │
│  - Command/Query DTOs                   │
│  - Validación de negocio                │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         DOMAIN LAYER                    │
│  - Entidades (Vehicle, Alert)           │
│  - Value Objects (VehicleStatus)        │
│  - Reglas de negocio                    │
│  - Ports (interfaces)                   │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│     INFRASTRUCTURE LAYER                │
│  - SQLite repositories                  │
│  - Observer pattern (alertas)           │
│  - Factories                            │
└─────────────────────────────────────────┘
```

**Principios Aplicados:**
- ✅ Independencia de frameworks
- ✅ Testabilidad sin infraestructura
- ✅ Inversión de dependencias
- ✅ Separación de responsabilidades

### Slide 4: Clean Architecture Fixes (2 min)
**"De Código Acoplado a Arquitectura Limpia"**

**Problemas Identificados (CLEAN_ARCHITECTURE_ANALYSIS.md):**
- 🔴 **CRITICAL**: Domain entities en web layer
- 🔴 **CRITICAL**: Infraestructura en application layer
- 🔴 **CRITICAL**: Singleton dependencies
- 🟡 **MEDIUM**: Falta de validación de entrada

**Soluciones Implementadas (CLEAN_ARCH_FIXES_TO_DO.md):**

**Phase 1 - Critical Fixes ✅**
1. **Application DTOs** 
   - Creado `application/dtos/` package
   - `RegisterVehicleCommand`, `UpdateMileageCommand`
   - `VehicleDTO`, `AlertDTO`
   - Mapeo web ↔ application ↔ domain

2. **Dependency Injection**
   - FastAPI `Depends()` para per-request sessions
   - Eliminado patrón singleton
   - Inyección limpia de repositorios

**Phase 2 - Architecture Fixes ✅**
3. **Observer Factory Port**
   - `ObserverFactory` interface en domain
   - Implementación en infrastructure
   - Use cases desacoplados de infraestructura

4. **Use Cases Completos**
   - `GetVehicleUseCase`
   - `GetVehicleAlertsUseCase`
   - `GetAllVehiclesUseCase`
   - Web layer solo orquesta

**Phase 3 - Validation ✅**
5. **Domain Validation**
   - `VehicleValidator` con 30+ tests
   - Validación de placa colombiana (XXX-### / XXX-####)
   - Validación de ID (V-XXX)
   - Validación de kilometraje (0-500k inicial, incrementos)

**Resultado (CLEAN_ARCH_RESIDUAL_RISKS.md):**
- 🔴 CRITICAL: 0 (ALL FIXED)
- 🟡 MEDIUM: 0 (ALL FIXED)
- 🟢 LOW: 1 (Nice to have)

### Slide 5: Patrones de Diseño Implementados (1.5 min)
**"Soluciones Elegantes a Problemas Comunes"**

**1. Observer Pattern (Alertas Automáticas)**
```python
# Domain: Vehicle notifica cambios
vehicle.update_mileage(new_mileage)
# → Observers detectan umbrales
# → Generan alertas automáticamente
```

**2. Repository Pattern**
```python
# Port en domain
class VehicleRepository(ABC):
    @abstractmethod
    def save(self, vehicle: Vehicle) -> None: ...

# Implementación en infrastructure
class SqliteVehicleRepository(VehicleRepository):
    # SQLAlchemy implementation
```

**3. Factory Pattern**
```python
# ObserverFactory crea observers según configuración
factory.create_observers(vehicle)
# → BasicMaintenanceObserver (10k km)
# → MajorMaintenanceObserver (50k km)
# → CriticalMaintenanceObserver (100k km)
```

**4. Command Pattern (CQRS)**
```python
# Commands para escritura
RegisterVehicleCommand(id, plate, model, mileage)
UpdateMileageCommand(vehicle_id, new_mileage)

# DTOs para lectura
VehicleDTO(id, plate, model, current_mileage, alerts)
```

### Slide 6: Historias de Usuario (1.5 min)
**"De Requisitos a Código"**

**Historias Implementadas (USER_STORIES.md):**

**HU-001**: Registro automático de kilometraje ✅
- Validación de incrementos
- Generación automática de alertas
- Reglas de negocio: RN-001 a RN-007

**HU-002**: Registro de nuevos vehículos ✅
- Validación de unicidad (ID, placa)
- Formato de placa colombiano
- Reglas de negocio: RN-008 a RN-014

**HU-003**: Consulta de vehículos con alertas ✅
- Inclusión de alertas ordenadas cronológicamente
- **NUEVO**: Visualización en modal de detalles
- Reglas de negocio: RN-015 a RN-017

**HU-004**: Eliminación de vehículos ✅
- Eliminación en cascada de alertas
- Validaciones de formato
- Reglas de negocio: RN-018 a RN-024

**HU-005**: Gestión de estado operativo ✅ (NUEVA)
- Estados: active, inactive, in_maintenance, retired
- Filtrado por estado
- Prevención de actualizaciones en vehículos retirados
- Reglas de negocio: RN-025 a RN-030

**HU-006**: Búsqueda por placa ✅ (NUEVA)
- Búsqueda case-insensitive
- Coincidencias parciales
- Resultados con alertas incluidas
- Reglas de negocio: RN-031 a RN-035

### Slide 7: Stack Tecnológico (1 min)
**"Herramientas Modernas y Probadas"**

**Backend:**
- **FastAPI**: Framework web moderno, async, OpenAPI automático
- **Python 3.8+**: Type hints, dataclasses
- **SQLAlchemy**: ORM con soporte para múltiples DBs
- **SQLite**: Base de datos embebida (fácil deployment)
- **Pytest**: Testing framework con 30+ tests

**Frontend:**
- **React 19**: UI moderna
- **TypeScript**: Type safety end-to-end
- **Vite**: Build tool ultra-rápido (HMR)
- **CSS3 Variables**: Design system consistente
- **Fetch API**: Comunicación con backend

**DevOps:**
- **Git**: Control de versiones
- **Uvicorn**: ASGI server de alto rendimiento
- **npm**: Gestión de dependencias frontend

### Slide 8: API Design (1 min)
**"RESTful API con OpenAPI"**

**Endpoints Implementados:**
```
POST   /vehicles                    → Registrar vehículo
GET    /vehicles                    → Listar todos (con filtros)
GET    /vehicles?status=active      → Filtrar por estado
GET    /vehicles/search?plate=ABC   → Buscar por placa (NUEVO)
GET    /vehicles/{id}               → Obtener uno
PUT    /vehicles/{id}/mileage       → Actualizar kilometraje
DELETE /vehicles/{id}               → Eliminar vehículo
GET    /vehicles/{id}/alerts        → Obtener alertas
```

**Características:**
- ✅ Documentación automática (Swagger UI)
- ✅ Validación con Pydantic
- ✅ Códigos HTTP semánticos (200, 201, 204, 400, 404)
- ✅ CORS configurado para frontend
- ✅ DTOs tipados para request/response

---

## **Min 10-14: Cultura DevOps y Calidad**

### Slide 9: Testing Strategy (2 min)
**"Confianza a Través de Tests"**

**Cobertura de Tests (automotive-backend/tests/):**

**1. Domain Layer Tests**
```python
# test_vehicle.py - Entidad Vehicle
- Creación de vehículos
- Actualización de kilometraje
- Validaciones de negocio
- Observer notifications

# test_maintenance_alert.py - Entidad Alert
- Creación de alertas
- Tipos de alerta (BASIC, MAJOR, CRITICAL)
```

**2. Application Layer Tests**
```python
# test_register_vehicle_use_case.py
- Registro exitoso
- Validación de duplicados
- Validación de formato

# test_update_mileage_use_case.py
- Actualización válida
- Generación de alertas
- Validación de incrementos

# test_vehicle_validator.py (30+ tests)
- Validación de placa colombiana
- Validación de ID (V-XXX)
- Validación de kilometraje
- Edge cases
```

**3. Infrastructure Layer Tests**
```python
# test_sqlite_vehicle_repository.py
- CRUD operations
- Persistencia
- Queries

# test_sqlite_alert_repository.py
- Almacenamiento de alertas
- Consultas por vehículo
```

**Métricas:**
- ✅ **175+ tests automatizados** (Backend)
  - 85+ tests de aplicación (incluyendo 30+ de validación)
  - 20+ tests de dominio
  - 55+ tests de integración
  - 15+ tests de infraestructura
- ✅ **50+ tests frontend** (Vitest)
- ✅ Cobertura >70% enforced en CI
- ✅ Tests de validación exhaustivos
- ✅ Mocks para infraestructura

### Slide 10: CI/CD Pipeline (1 min)
**"Automatización y Calidad Continua"**

**GitHub Actions Workflows:**

**1. Backend CI (.github/workflows/backend-ci.yml)**
```yaml
Job 1: Quality & Security Checks
  - Lint with Ruff
  - Format check with Ruff
  - Type checking (mypy)
  - Security scan (bandit)
  - Dependency check (safety)
  - Upload security reports

Job 2: Unit Tests (Python 3.11 & 3.12)
  - Run domain & application tests
  - Multi-version testing

Job 3: Integration Tests & Coverage
  - Run all tests with coverage
  - Enforce 70% coverage threshold
  - Upload to Codecov
  - PR coverage comments

Job 4: Docker Build & Test
  - Build Docker image
  - Health check validation
  - Image size inspection

Job 5: CI Success Summary
  - Aggregate results
  - Post GitHub summary
```

**2. Frontend CI (.github/workflows/frontend-ci.yml)**
```yaml
Job 1: Code Quality & Linting
  - ESLint validation
  - Prettier format check
  - TypeScript type checking

Job 2: Tests & Coverage
  - Run Vitest tests
  - Enforce 70% coverage threshold
  - Upload to Codecov
  - PR coverage comments

Job 3: Build Validation
  - Production build
  - Bundle size check
  - Upload artifacts

Job 4: Docker Build & Test (optional)
  - Build Docker image (if Dockerfile exists)
  - Container validation

Job 5: CI Success Summary
  - Aggregate results
  - Post GitHub summary
```

**Beneficios:**
- ✅ **5 jobs paralelos** por pipeline (optimizado)
- ✅ **Multi-version testing** (Python 3.11 & 3.12)
- ✅ **Security scanning** automático (bandit, safety)
- ✅ **Coverage enforcement** (70% threshold)
- ✅ **Docker validation** en cada build
- ✅ Tests automáticos en cada push
- ✅ Detección temprana de errores
- ✅ Calidad de código consistente
- ✅ Documentación viva (tests como specs)

### Slide 11: Code Quality & Best Practices (1 min)
**"Código Limpio y Mantenible"**

**Convenciones Aplicadas:**

**Backend:**
- ✅ Type hints en todo el código
- ✅ Docstrings en clases y métodos
- ✅ PEP 8 compliance (ruff linter)
- ✅ Nombres descriptivos
- ✅ Single Responsibility Principle

**Frontend:**
- ✅ TypeScript strict mode
- ✅ Componentes funcionales con hooks
- ✅ Props tipadas con interfaces
- ✅ Custom hooks para lógica reutilizable
- ✅ CSS con metodología BEM implícita

**Documentación:**
- ✅ README.md completo
- ✅ RUN_INSTRUCTIONS.md paso a paso
- ✅ DESIGN.md con especificaciones UI
- ✅ USER_STORIES.md con Gherkin
- ✅ Comentarios en código complejo

---

## **Min 14-17: Demo en Vivo**

### Slide 12: Demo Script
**"Sistema en Acción"**

**Preparación:**
1. Backend corriendo: `http://127.0.0.1:8000`
2. Frontend corriendo: `http://localhost:5173`
3. Base de datos limpia

**Demo Flow (3 minutos):**

**1. Dashboard Inicial (30s)**
- Mostrar interfaz vacía
- Explicar diseño dark theme (Slate Neon)
- Mostrar stats en 0

**2. Registrar Vehículo (45s)**
- Click "Nuevo Vehículo"
- Llenar formulario:
  - ID: V-001
  - Placa: ABC-123
  - Modelo: Toyota Corolla 2020
  - Kilometraje: 5,000 km
- Mostrar validaciones en tiempo real
- Registrar → Toast de éxito
- Stats actualizados

**3. Actualizar Kilometraje y Generar Alertas (45s)**
- Click "Actualizar KM"
- Ingresar: 15,000 km
- Mostrar que genera alerta (10k threshold)
- Badge de alerta aparece
- Stats muestran 1 alerta

**4. Búsqueda por Placa (30s)** ⭐ FUNCIONALIDAD COMPLETA
- Registrar segundo vehículo (ABC-456)
- Usar search bar: "ABC"
- Mostrar búsqueda en tiempo real (debounced 300ms)
- Búsqueda case-insensitive con coincidencias parciales
- Endpoint: `GET /vehicles/search?plate=ABC`
- Integrada con paginación automática

**5. Gestión de Estados (30s)**
- Click en badge de estado
- Cambiar a "En Mantenimiento"
- Filtrar por estado "active"
- Mostrar solo vehículos activos

**6. Ver Detalles con Alertas (30s)** ⭐
- Click "Detalles"
- Mostrar modal con:
  - Información del vehículo
  - **Sección de alertas** (nueva)
  - Alertas ordenadas cronológicamente

---

## **Min 17-20: Aprendizajes y Conclusiones**

### Slide 13: Logros del Proyecto (1.5 min)
**"Lo Que Construimos"**

**✅ Clean Architecture Completa:**
- Migración de código acoplado a arquitectura limpia
- 0 violaciones críticas (de 4 iniciales)
- Código testeable y mantenible

**✅ Frontend Moderno:**
- Migración de Vanilla JS a React + TypeScript
- Dark theme profesional (Slate Neon)
- Componentes reutilizables
- Type safety end-to-end

**✅ Funcionalidades de Negocio:**
- 6 Historias de Usuario implementadas
- 35+ Reglas de Negocio codificadas
- Sistema de alertas automático
- Gestión completa de flota

**✅ Calidad y Testing:**
- **175+ tests backend** (pytest)
  - 85+ tests de aplicación
  - 20+ tests de dominio
  - 55+ tests de integración
  - 15+ tests de infraestructura
- **50+ tests frontend** (vitest)
- CI/CD pipeline funcional
- Cobertura >70% enforced
- Validaciones exhaustivas
- Documentación completa

**✅ Nuevas Funcionalidades:**
- HU-006: Búsqueda por placa (COMPLETA con backend + frontend)
- HU-003 mejorada: Alertas en modal de detalles
- Filtrado por estado operativo
- Prevención de actualizaciones en vehículos retirados
- Paginación funcional (8 vehículos por página)
- Búsqueda con debounce (300ms) integrada con paginación

### Slide 14: Desafíos Superados (1 min)
**"Obstáculos y Soluciones"**

**1. Arquitectura Acoplada → Clean Architecture**
- **Desafío**: Código legacy con dependencias circulares
- **Solución**: Refactoring incremental con DTOs y ports
- **Aprendizaje**: La inversión de dependencias es clave

**2. Validación Distribuida → Domain Validation**
- **Desafío**: Validaciones en múltiples capas
- **Solución**: VehicleValidator centralizado en domain
- **Aprendizaje**: Single source of truth para reglas

**3. UI Estática → React Dinámico**
- **Desafío**: Migrar de Vanilla JS sin perder funcionalidad
- **Solución**: Hooks personalizados + TypeScript
- **Aprendizaje**: Type safety previene errores en runtime

**4. Alertas Manuales → Sistema Automático**
- **Desafío**: Cálculo manual de mantenimientos
- **Solución**: Observer pattern con estrategias
- **Aprendizaje**: Patrones de diseño simplifican lógica compleja

### Slide 15: Próximos Pasos (1 min)
**"Roadmap Futuro"**

**Corto Plazo (1-2 semanas):**
- [ ] Tests E2E con Playwright
- [ ] Búsqueda avanzada (por ID, modelo)
- [ ] Exportar reportes (PDF/Excel)

**Mediano Plazo (1 mes):**
- [ ] Autenticación y autorización
- [ ] Roles de usuario (admin, operador)
- [ ] Historial de cambios (audit log)
- [ ] Notificaciones push

**Largo Plazo (3 meses):**
- [ ] Dashboard de analytics
- [ ] Integración con GPS
- [ ] App móvil (React Native)
- [ ] Machine Learning para predicción de fallas

### Slide 16: Conclusiones (30s)
**"Reflexiones Finales"**

**Lecciones Clave:**
1. **Clean Architecture funciona**: Código testeable, mantenible, escalable
2. **TypeScript es esencial**: Previene errores, mejora DX
3. **Tests dan confianza**: Refactoring sin miedo
4. **Documentación importa**: README salva vidas
5. **Iteración continua**: De MVP a producto robusto

**Impacto:**
- ✅ Sistema productivo listo para deployment
- ✅ Arquitectura preparada para escalar
- ✅ Código que otros pueden mantener
- ✅ Base sólida para nuevas features

---

## **Materiales de Apoyo**

**Documentos a Tener Abiertos:**
1. `RUN_INSTRUCTIONS.md` - Para troubleshooting en vivo
2. `USER_STORIES.md` - Referencia de HUs
3. `CLEAN_ARCH_FIXES_TO_DO.md` - Checklist de fixes
4. `http://127.0.0.1:8000/docs` - Swagger UI
5. `http://localhost:5173` - App corriendo

**Backup Slides:**
- Diagrama de base de datos (SQLite schema)
- Ejemplo de código de Observer pattern
- Comparativa antes/después de Clean Architecture
- Métricas de performance (response times)
- **Test Coverage Breakdown** (NUEVO):
  ```
  Backend (175 tests):
  - Domain: 20 tests (entities, strategies)
  - Application: 85 tests (use cases, validator)
  - Infrastructure: 15 tests (repositories, DI)
  - Integration: 55 tests (API endpoints, E2E)
  
  Frontend (50+ tests):
  - Formatters: 30+ tests
  - API service: 12+ tests
  - Hooks: 8+ tests (pagination, search)
  - Components: Tests en progreso
  ```
- **CI/CD Pipeline Details** (NUEVO):
  ```
  Backend Pipeline (5 jobs):
  1. Quality & Security: Ruff, mypy, bandit, safety
  2. Unit Tests: Python 3.11 & 3.12 (matrix)
  3. Integration & Coverage: 70% threshold enforced
  4. Docker Build: Image validation + health checks
  5. Summary: Aggregate results + GitHub summary
  
  Frontend Pipeline (5 jobs):
  1. Code Quality: ESLint, Prettier, TypeScript
  2. Tests & Coverage: Vitest, 70% threshold
  3. Build Validation: Production bundle + size check
  4. Docker Build: Optional container validation
  5. Summary: Aggregate results + GitHub summary
  
  Features:
  - Parallel execution for speed
  - Multi-version testing (Python 3.11/3.12)
  - Security scanning (bandit, safety)
  - Coverage reporting (Codecov)
  - PR comments with coverage diff
  - Artifact uploads (reports, builds)
  ```

---

**¡Buena suerte con la presentación! 🚀**
