# Automotive: Gestión de Flota y Mantenimiento

Sistema de gestión de flota de vehículos con monitoreo de kilometraje y alertas automáticas de mantenimiento.

---

## 🚀 Colección Postman

Incluye una colección lista para importar y ejecutar en Postman, cubriendo todos los endpoints, reglas de negocio y escenarios del reto.

- Archivo: `postman/automotive-maintenance.postman_collection.json`
- Instrucciones: ver `postman/README.md`

---

## Descripción

Sistema que implementa **Arquitectura Hexagonal** con **TDD estricto** para gestionar una flota de vehículos, monitoreando el kilometraje y generando alertas automáticas cuando se requiere mantenimiento.

## Características

- ✓ Gestión completa de vehículos (CRUD)
- ✓ Actualización de kilometraje con validaciones
- ✓ Sistema de alertas automáticas (Patrón Observer)
- ✓ Reglas de mantenimiento extensibles (Strategy Pattern)
- ✓ API REST con 5 endpoints
- ✓ Arquitectura Limpia (Hexagonal)
- ✓ TDD estricto con cobertura >= 70%
- ✓ Principios SOLID

## Requisitos

- Python 3.11+
- pip

## Instalación

```bash
# Clonar repositorio
git clone https://github.com/gerardleython-coder/automotive-maintenance.git
cd automotive-maintenance

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

---

## Ejecución de Pruebas

```bash
# Ejecutar todos los tests con cobertura
pytest --cov=src --cov-report=term-missing

# Ejecutar tests de dominio
pytest tests/domain/ -v

# Ejecutar tests de integración
pytest tests/integration/ -v
```

## Arquitectura

```
src/
├── domain/            # Entidades, excepciones, contratos (ports)
├── application/       # Casos de uso, lógica de aplicación
├── infrastructure/    # Implementaciones concretas (repositories, observers)
└── web/              # API REST (FastAPI)
```

La explicación detallada de los patrones y la arquitectura se encuentra en este README y en los módulos de `src/domain` y `src/application`.

---

### API REST

**Endpoints disponibles:**

- `POST /vehicles` - Registrar nuevo vehículo
- `PUT /vehicles/{id}/mileage` - Actualizar kilometraje
- `GET /vehicles/{id}` - Consultar vehículo por ID
- `GET /vehicles` - Listar todos los vehículos con alertas
- `DELETE /vehicles/{id}` - Eliminar vehículo (con cascade de alertas)

**Documentación interactiva (OpenAPI/Swagger):**
- [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Patrones de Diseño

- **Observer Pattern**: Sistema de eventos para alertas de mantenimiento
- **Strategy Pattern**: Reglas de mantenimiento extensibles
- **Repository Pattern**: Abstracción de persistencia (DIP)

La documentación de los patrones y su implementación se encuentra explicada en este README y en los módulos de dominio y aplicación.

## Desarrollo

Este proyecto sigue **TDD estricto**. El historial de Git muestra el ciclo RED → GREEN → REFACTOR.

Ver [USER_STORIES.md](USER_STORIES.md) para historias de usuario y criterios de aceptación.

## Diseño UI/UX

Especificaciones de diseño, mockups y guías de estilo en [docs/design/DESIGN.md](docs/design/DESIGN.md)

## Pruebas Automatizadas con Postman

Colección de **60+ tests automatizados** que validan:
- ✅ Status codes HTTP (200, 201, 204, 400, 404)
- ✅ Schemas JSON de respuestas
- ✅ Reglas de negocio (validaciones de kilometraje)
- ✅ Observer Pattern (alertas automáticas)
- ✅ Strategy Pattern (estrategias de mantenimiento)
- ✅ Operaciones CRUD completas

**Ejecución:**
```bash
# Importar en Postman Desktop/Web
1. Importar: docs/postman/Automotive_Fleet_API.postman_collection.json
2. Importar: docs/postman/Automotive_Environment.postman_environment.json
3. Activar environment "Automotive - Local Development"
4. Run Collection

# O usar Newman CLI
newman run docs/postman/Automotive_Fleet_API.postman_collection.json \
  -e docs/postman/Automotive_Environment.postman_environment.json
```

Ver [docs/postman/README.md](docs/postman/README.md) para documentación completa.

## CI/CD

GitHub Actions ejecuta automáticamente:
- Linting con Ruff
- Tests con pytest
- Validación de cobertura >= 70%

## Estado del Proyecto

**Historias de Usuario Implementadas:**
- ✅ HU-001: Actualización de kilometraje con alertas automáticas
- ✅ HU-002: Registro de nuevos vehículos
- ✅ HU-003: Consulta de vehículos con alertas
- ✅ HU-004: Eliminación de vehículos con cascade

**Métricas:**
- 46 tests pasando
- 95.96% cobertura de código
- 0 errores de linter

---
