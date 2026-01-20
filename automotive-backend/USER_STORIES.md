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

## Reglas de Negocio

- RN-001: El kilometraje debe ser siempre mayor al valor actual
- RN-002: El kilometraje no puede ser negativo
- RN-003: El kilometraje máximo permitido es 1,000,000 km
- RN-004: El incremento máximo permitido es 50,000 km
- RN-005: Se genera alerta cada 10,000 km (mantenimiento básico)
- RN-006: Se genera alerta cada 50,000 km (mantenimiento mayor)
- RN-007: Se genera alerta crítica al superar 100,000 km
- RN-008: El ID del vehículo debe ser único en el sistema
- RN-009: La placa del vehículo debe ser única en el sistema
- RN-010: El formato de placa debe seguir el estándar colombiano (XXX-### o XXX-####)
- RN-011: El ID del vehículo debe seguir el formato V-XXX
- RN-012: El modelo del vehículo no puede estar vacío
- RN-013: El kilometraje inicial debe estar entre 0 y 500,000 km
- RN-014: No se generan alertas durante el registro inicial del vehículo
- RN-015: La consulta de vehículos debe incluir todas las alertas asociadas a cada vehículo
- RN-016: Las alertas en la respuesta deben ordenarse cronológicamente (más reciente primero)
- RN-017: La respuesta de consulta debe incluir campos obligatorios: id, plate, model, current_mileage, alerts
- RN-018: La eliminación de un vehículo debe eliminar en cascada todas sus alertas asociadas
- RN-019: No se permite eliminar un vehículo que no existe (debe retornar 404)
- RN-020: La eliminación exitosa debe retornar código 204 No Content
- RN-021: El ID para eliminación debe seguir el formato V-XXX (validación obligatoria)
- RN-022: No deben quedar alertas huérfanas después de eliminar un vehículo
- RN-023: La eliminación es permanente y no reversible
- RN-024: Un vehículo eliminado no debe aparecer en consultas posteriores

---