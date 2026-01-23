# Historias de Usuario - Sistema de Gestión de Flota

## HU-001: Registro automático de kilometraje de vehículos

**Como** gestor de flota
**Quiero** que el sistema registre automáticamente el kilometraje de mis vehículos
**Para** recibir alertas oportunas de mantenimiento preventivo, mayor y crítico

### Criterios de Aceptación

#### Escenario 1: Registro automático exitoso y generación de alerta

```gherkin
Given un vehículo con ID 'V-123' y kilometraje actual de 5,000 km
And existen reglas de mantenimiento cada 10,000 km
When registro un nuevo kilometraje de 10,001 km
Then el kilometraje del vehículo debe actualizarse a 10,001 km
And se debe generar una alerta de mantenimiento automáticamente
```

#### Escenario 2: Error por kilometraje menor al actual (Anti-Happy Path)

```gherkin
Given un vehículo con kilometraje actual de 5,000 km
When intento registrar un kilometraje de 4,000 km
Then el sistema debe lanzar una excepción de negocio 'InvalidMileageException'
```

#### Escenario 3: Validación de valores inválidos de kilometraje

```gherkin
Given un vehículo con kilometraje actual registrado
When intento actualizar el kilometraje con un valor inválido
Then el sistema debe rechazar la operación

Ejemplos de valores inválidos:
- Kilometraje negativo
- Kilometraje superior a 1,000,000 km
- Incremento mayor a 50,000 km respecto al último registro
```

#### Escenario 4: Registro sin generación de alerta

```gherkin
Given un vehículo con kilometraje actual de 5,000 km
When registro un nuevo kilometraje de 8,000 km
Then el kilometraje del vehículo debe actualizarse a 8,000 km
And no se debe generar ninguna alerta de mantenimiento
```

---

## HU-002: Registro de nuevos vehículos en la flota

**Como** gestor de flota
**Quiero** registrar nuevos vehículos en el sistema
**Para** poder gestionar su mantenimiento preventivo desde el inicio de su operación

### Criterios de Aceptación

#### Escenario 1: Registro exitoso de vehículo nuevo

```gherkin
Given que no existe un vehículo con ID 'V-456' en el sistema
And no existe un vehículo con placa 'XYZ-789'
When registro un nuevo vehículo con los siguientes datos:
  | Campo               | Valor        |
  | ID                  | V-456        |
  | Placa               | XYZ-789      |
  | Modelo              | Honda Civic  |
  | Kilometraje Inicial | 0            |
Then el vehículo debe ser registrado exitosamente
And debe estar disponible para consulta posterior
```

#### Escenario 2: Error por ID duplicado (Anti-Happy Path)

```gherkin
Given que existe un vehículo con ID 'V-123' en el sistema
When intento registrar un nuevo vehículo con ID 'V-123'
Then el sistema debe lanzar una excepción 'DuplicateVehicleException'
And el mensaje debe indicar "Ya existe un vehículo con ID V-123"
```

#### Escenario 3: Error por placa duplicada (Anti-Happy Path)

```gherkin
Given que existe un vehículo con placa 'ABC-123'
When intento registrar un nuevo vehículo con placa 'ABC-123'
Then el sistema debe lanzar una excepción 'DuplicatePlateException'
And el mensaje debe indicar "Ya existe un vehículo con placa ABC-123"
```

#### Escenario 4: Validación de datos obligatorios

```gherkin
When intento registrar un vehículo con datos incompletos
Then el sistema debe rechazar la operación

Ejemplos de datos inválidos:
- ID vacío o nulo
- Placa vacía o nula
- Modelo vacío o nulo
- Formato de placa inválido (debe ser XXX-### o XXX-####)
```

#### Escenario 5: Validación de kilometraje inicial

```gherkin
Given datos válidos para un nuevo vehículo
When intento registrar el vehículo con kilometraje inicial inválido
Then el sistema debe rechazar la operación

Ejemplos de kilometraje inicial inválido:
- Kilometraje negativo
- Kilometraje superior a 500,000 km (vehículos usados)
```

#### Escenario 6: Registro de vehículo usado con kilometraje inicial

```gherkin
Given que no existe un vehículo con ID 'V-789'
When registro un vehículo usado con kilometraje inicial de 25,000 km
Then el vehículo debe ser registrado exitosamente
And el kilometraje actual debe ser 25,000 km
And no se deben generar alertas automáticas en el registro inicial
```

---

## HU-003: Consulta de todos los vehículos con sus alertas

**Como** gestor de flota
**Quiero** consultar todos los vehículos registrados con sus alertas e información completa
**Para** tener una visión general del estado de mantenimiento de mi flota

### Criterios de Aceptación

#### Escenario 1: Consulta exitosa con vehículos y alertas

```gherkin
Given existen 3 vehículos registrados en el sistema
And el vehículo 'V-123' tiene 2 alertas de mantenimiento
And el vehículo 'V-456' tiene 1 alerta de mantenimiento
And el vehículo 'V-789' no tiene alertas
When solicito la lista completa de vehículos
Then el sistema debe devolver los 3 vehículos
And cada vehículo debe incluir: ID, placa, modelo, kilometraje actual
And cada vehículo debe incluir su lista de alertas ordenadas cronológicamente
And las alertas deben incluir: tipo, mensaje, kilometraje y fecha
```

#### Escenario 2: Consulta cuando no existen vehículos

```gherkin
Given no existen vehículos registrados en el sistema
When solicito la lista completa de vehículos
Then el sistema debe devolver una lista vacía
And el código de respuesta debe ser 200 OK
```

#### Escenario 3: Consulta con vehículos sin alertas

```gherkin
Given existe un vehículo 'V-100' con kilometraje 5,000 km
And el vehículo no ha alcanzado ningún umbral de mantenimiento
When solicito la lista completa de vehículos
Then el sistema debe devolver el vehículo 'V-100'
And la lista de alertas del vehículo debe estar vacía
```

#### Escenario 4: Validación de estructura de respuesta

```gherkin
Given existen vehículos con alertas en el sistema
When solicito la lista completa de vehículos
Then cada vehículo debe tener el siguiente formato:
  | Campo            | Tipo              | Obligatorio |
  | id               | String            | Sí          |
  | plate            | String            | Sí          |
  | model            | String            | Sí          |
  | current_mileage  | Integer           | Sí          |
  | alerts           | Array[Alert]      | Sí          |
And cada alerta debe tener el siguiente formato:
  | Campo            | Tipo              | Obligatorio |
  | alert_type       | String            | Sí          |
  | message          | String            | Sí          |
  | mileage          | Integer           | Sí          |
  | timestamp        | DateTime          | Sí          |
```

#### Escenario 5: Ordenamiento de alertas por fecha

```gherkin
Given existe un vehículo 'V-200' con 5 alertas generadas en diferentes fechas
When solicito la lista de vehículos
Then las alertas del vehículo 'V-200' deben estar ordenadas cronológicamente
And la alerta más reciente debe aparecer primero
```

#### Escenario 6: Visualización de alertas en detalles del vehículo

```gherkin
Given existe un vehículo 'V-123' con 3 alertas de mantenimiento
When el usuario hace clic en el botón "Detalles" del vehículo
Then el sistema debe mostrar un modal con la información del vehículo
And el modal debe incluir una sección de "Alertas de Mantenimiento"
And debe mostrar las 3 alertas ordenadas cronológicamente (más reciente primero)
And cada alerta debe mostrar: tipo, mensaje, kilometraje y fecha de generación

```
---

## HU-004: Eliminación de vehículos por ID

**Como** gestor de flota
**Quiero** eliminar vehículos del sistema usando su ID
**Para** mantener actualizada la información de mi flota cuando un vehículo deja de operar

### Criterios de Aceptación

#### Escenario 1: Eliminación exitosa de vehículo existente

```gherkin
Given existe un vehículo con ID 'V-999' en el sistema
And el vehículo tiene 3 alertas asociadas
When elimino el vehículo con ID 'V-999'
Then el vehículo debe ser eliminado del sistema
And el código de respuesta debe ser 204 No Content
And las 3 alertas asociadas deben eliminarse automáticamente (cascada)
```

#### Escenario 2: Error al eliminar vehículo inexistente (Anti-Happy Path)

```gherkin
Given no existe un vehículo con ID 'V-888' en el sistema
When intento eliminar el vehículo con ID 'V-888'
Then el sistema debe lanzar una excepción 'VehicleNotFoundException'
And el código de respuesta debe ser 404 Not Found
And el mensaje debe indicar "Vehículo con ID V-888 no encontrado"
```

#### Escenario 3: Verificación de eliminación en cascada de alertas

```gherkin
Given existe un vehículo 'V-777' con 10 alertas registradas
When elimino el vehículo 'V-777'
Then no deben quedar alertas huérfanas en la base de datos
And una consulta de alertas para 'V-777' debe retornar error
```

#### Escenario 4: Validación de formato de ID

```gherkin
When intento eliminar un vehículo con ID en formato inválido
Then el sistema debe rechazar la operación
And debe retornar un código 400 Bad Request

Ejemplos de formatos inválidos:
- ID vacío o nulo
- ID sin el prefijo 'V-' (ejemplo: '123')
- ID con caracteres especiales (ejemplo: 'V-@@@')
```

#### Escenario 5: Confirmación de eliminación permanente

```gherkin
Given existe un vehículo 'V-555' en el sistema
When elimino el vehículo 'V-555'
And posteriormente intento consultar el vehículo 'V-555'
Then el sistema debe retornar 404 Not Found
And el vehículo no debe aparecer en la lista de vehículos
```

#### Escenario 6: Eliminación de vehículo sin alertas

```gherkin
Given existe un vehículo 'V-333' sin alertas asociadas
When elimino el vehículo 'V-333'
Then el vehículo debe ser eliminado exitosamente
And el código de respuesta debe ser 204 No Content
```

---

## HU-005: Gestión de Estado Operativo de Vehículos

**Como** gestor de flota  
**Quiero** gestionar el estado operativo de cada vehículo  
**Para** saber qué vehículos están disponibles, en mantenimiento o fuera de servicio

### Criterios de Aceptación

#### Escenario 1: Cambiar estado de vehículo a "en mantenimiento"

```gherkin
Given existe un vehículo con ID 'V-123' con estado 'active'
When actualizo el estado del vehículo a 'in_maintenance'
Then el estado del vehículo debe ser 'in_maintenance'
And el vehículo debe seguir visible en la lista de vehículos
And el cambio de estado debe registrar la fecha de actualización
```

#### Escenario 2: Filtrar vehículos por estado

```gherkin
Given existen 5 vehículos en el sistema:
  | ID    | Estado          |
  | V-001 | active          |
  | V-002 | active          |
  | V-003 | in_maintenance  |
  | V-004 | inactive        |
  | V-005 | retired         |
When solicito la lista de vehículos con filtro status='active'
Then el sistema debe devolver 2 vehículos
And ambos vehículos deben tener estado 'active'
```

#### Escenario 3: Validación de estados permitidos

```gherkin
Given existe un vehículo con ID 'V-456'
When intento actualizar el estado a un valor inválido 'broken'
Then el sistema debe rechazar la operación
And debe retornar un código 400 Bad Request
And el mensaje debe indicar los estados válidos: active, inactive, in_maintenance, retired
```

#### Escenario 4: Registro de vehículo nuevo con estado inicial

```gherkin
Given voy a registrar un nuevo vehículo
When registro el vehículo sin especificar estado
Then el vehículo debe crearse con estado 'active' por defecto
And debe estar disponible para operaciones
```

#### Escenario 5: Prevenir actualización de kilometraje en vehículos retirados

```gherkin
Given existe un vehículo 'V-789' con estado 'retired'
When intento actualizar el kilometraje del vehículo
Then el sistema debe rechazar la operación
And debe retornar un código 400 Bad Request
And el mensaje debe indicar "No se puede actualizar kilometraje de vehículos retirados"
```

---

## HU-006: Búsqueda de vehículos por placa

**Como** gestor de flota  
**Quiero** buscar vehículos por su placa  
**Para** encontrar rápidamente un vehículo específico sin revisar toda la lista

### Criterios de Aceptación

#### Escenario 1: Búsqueda exitosa por placa completa

```gherkin
Given existen los siguientes vehículos en el sistema:
  | ID    | Placa   | Modelo        |
  | V-001 | ABC-123 | Toyota Corolla|
  | V-002 | XYZ-456 | Honda Civic   |
  | V-003 | ABC-789 | Mazda 3       |
When busco vehículos con la placa "ABC-123"
Then el sistema debe devolver 1 vehículo
And el vehículo debe tener placa "ABC-123"
```

#### Escenario 2: Búsqueda por placa parcial (coincidencia parcial)

```gherkin
Given existen los siguientes vehículos en el sistema:
  | ID    | Placa   | Modelo        |
  | V-001 | ABC-123 | Toyota Corolla|
  | V-002 | XYZ-456 | Honda Civic   |
  | V-003 | ABC-789 | Mazda 3       |
When busco vehículos con la placa "ABC"
Then el sistema debe devolver 2 vehículos
And ambos vehículos deben tener placas que contengan "ABC"
```

#### Escenario 3: Búsqueda sin resultados

```gherkin
Given existen vehículos registrados en el sistema
When busco vehículos con la placa "ZZZ-999"
Then el sistema debe retornar un código 404 Not Found
And el mensaje debe indicar que no se encontraron vehículos con esa placa

```

#### Escenario 4: Búsqueda case-insensitive (sin distinción de mayúsculas/minúsculas)

```gherkin
Given existe un vehículo con placa "ABC-123"
When busco vehículos con la placa "abc-123"
Then el sistema debe devolver el vehículo con placa "ABC-123"
And la búsqueda debe ser insensible a mayúsculas/minúsculas
```

#### Escenario 5: Búsqueda con término vacío (Anti-Happy Path)

```gherkin
Given existen vehículos registrados en el sistema
When busco vehículos con una placa vacía o solo espacios
Then el sistema debe retornar un código 404 Not Found
And el mensaje debe indicar "La placa de búsqueda no puede estar vacía"
```

## Reglas de Negocio

### Gestión de Kilometraje (HU-001)
- RN-001: El kilometraje debe ser siempre mayor al valor actual
- RN-002: El kilometraje no puede ser negativo
- RN-003: El kilometraje máximo permitido es 1,000,000 km
- RN-004: El incremento máximo permitido es 50,000 km
- RN-005: Se genera alerta cada 10,000 km (mantenimiento básico)
- RN-006: Se genera alerta cada 50,000 km (mantenimiento mayor)
- RN-007: Se genera alerta crítica al superar 100,000 km

### Registro de Vehículos (HU-002)
- RN-008: El ID del vehículo debe ser único en el sistema
- RN-009: La placa del vehículo debe ser única en el sistema
- RN-010: El formato de placa debe seguir el estándar colombiano (XXX-### o XXX-####)
- RN-011: El ID del vehículo debe seguir el formato V-XXX
- RN-012: El modelo del vehículo no puede estar vacío
- RN-013: El kilometraje inicial debe estar entre 0 y 500,000 km
- RN-014: No se generan alertas durante el registro inicial del vehículo

### Consulta de Vehículos (HU-003)
- RN-015: La consulta de vehículos debe incluir todas las alertas asociadas a cada vehículo
- RN-016: Las alertas en la respuesta deben ordenarse cronológicamente (más reciente primero)
- RN-017: La respuesta de consulta debe incluir campos obligatorios: id, plate, model, current_mileage, alerts

### Eliminación de Vehículos (HU-004)
- RN-018: La eliminación de un vehículo debe eliminar en cascada todas sus alertas asociadas
- RN-019: No se permite eliminar un vehículo que no existe (debe retornar 404)
- RN-020: La eliminación exitosa debe retornar código 204 No Content
- RN-021: El ID para eliminación debe seguir el formato V-XXX (validación obligatoria)
- RN-022: No deben quedar alertas huérfanas después de eliminar un vehículo
- RN-023: La eliminación es permanente y no reversible
- RN-024: Un vehículo eliminado no debe aparecer en consultas posteriores

### Estado Operativo de Vehículos (HU-005)
- RN-025: Los estados válidos son: active, inactive, in_maintenance, retired
- RN-026: El estado por defecto al registrar un vehículo es 'active'
- RN-027: No se puede actualizar el kilometraje de vehículos con estado 'retired'
- RN-028: El cambio de estado debe registrar la fecha de actualización
- RN-029: Los vehículos pueden filtrarse por estado en las consultas
- RN-030: Todos los estados son visibles en la lista de vehículos

### Búsqueda de Vehículos (HU-006)
- RN-031: La búsqueda debe ser case-insensitive (sin distinción de mayúsculas/minúsculas)
- RN-032: La búsqueda debe soportar coincidencias parciales en la placa
- RN-033: Un término de búsqueda vacío o solo espacios debe retornar error 404 Not Found
- RN-034: Los resultados de búsqueda deben incluir las alertas de cada vehículo
- RN-035: Los resultados de búsqueda deben mantener el orden cronológico de las alertas

---