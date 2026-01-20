# Postman Collection - Automotive Fleet API

## 📋 Descripción

Colección de **pruebas automatizadas** para la API REST de gestión de flota vehicular. Incluye validaciones completas de:

- ✅ **Status codes HTTP** (200, 201, 204, 400, 404)
- ✅ **Schemas JSON** (estructura de respuestas)
- ✅ **Reglas de negocio** (validaciones de kilometraje)
- ✅ **Patrones de diseño** (Observer Pattern, Strategy Pattern)
- ✅ **Performance** (response times)
- ✅ **Operaciones CRUD** completas

## 📦 Archivos

- **Automotive_Fleet_API.postman_collection.json** - Colección con 10 requests y 60+ tests automatizados
- **Automotive_Environment.postman_environment.json** - Variables de entorno (baseUrl, vehicleId)
- **README.md** - Esta documentación

## 🚀 Importar en Postman

### 1. Importar Colección

1. Abrir Postman Desktop o Web
2. Click en **Import** (botón superior izquierdo)
3. Seleccionar **Automotive_Fleet_API.postman_collection.json**
4. Click en **Import**

### 2. Importar Environment

1. Click en **Environments** (panel izquierdo)
2. Click en **Import**
3. Seleccionar **Automotive_Environment.postman_environment.json**
4. Click en **Import**
5. **Activar el environment** en el selector superior derecho

## ▶️ Ejecutar Pruebas

### Opción 1: Ejecución Manual (Individual)

1. Asegurarse que el servidor esté ejecutándose:
   ```bash
   uvicorn src.web.main:app --reload
   ```

2. Seleccionar el environment **"Automotive - Local Development"**

3. Ejecutar requests en orden:
   - 1. Health Check
   - 2. Crear Vehículo
   - 3. Listar Todos los Vehículos
   - 4. Obtener Vehículo por ID
   - 5. Actualizar Kilometraje (Genera Alertas)
   - 6. Obtener Alertas del Vehículo
   - 7. Actualizar Kilometraje Inválido (Validación)
   - 8. Eliminar Vehículo (Cascade)
   - 9. Verificar Eliminación (404)
   - 10. Actualizar a 100k km (Critical Threshold)

4. Verificar en **Test Results** (panel inferior)

### Opción 2: Ejecución Automática (Collection Runner)

1. Click derecho en la colección **"Automotive Fleet Management API"**
2. Seleccionar **"Run collection"**
3. Configurar:
   - **Environment**: Automotive - Local Development
   - **Iterations**: 1
   - **Delay**: 500ms (opcional)
4. Click en **"Run Automotive Fleet..."**
5. Ver resumen de resultados en el dashboard

### Opción 3: CLI con Newman (CI/CD)

```bash
# Instalar Newman
npm install -g newman

# Ejecutar colección
newman run docs/postman/Automotive_Fleet_API.postman_collection.json \
  -e docs/postman/Automotive_Environment.postman_environment.json \
  --reporters cli,json \
  --reporter-json-export results.json

# Con delay entre requests (recomendado)
newman run docs/postman/Automotive_Fleet_API.postman_collection.json \
  -e docs/postman/Automotive_Environment.postman_environment.json \
  --delay-request 500
```

## 🧪 Tests Automatizados

Cada request incluye múltiples tests JavaScript:

### Request: "2. Crear Vehículo" (6 tests)
- ✅ Status code es 201 (vehículo creado)
- ✅ Schema de respuesta es válido
- ✅ Datos del vehículo son correctos
- ✅ Tipos de datos son correctos
- ✅ Variable vehicleId configurada
- ✅ Tiempo de respuesta < 1000ms

### Request: "6. Obtener Alertas del Vehículo" (8 tests)
- ✅ Status code es 200
- ✅ Respuesta es un array de alertas
- ✅ Se generó al menos 1 alerta automática (Observer Pattern)
- ✅ Schema de alertas es válido
- ✅ Todas las alertas pertenecen al vehículo
- ✅ Existe alerta BASIC_MAINTENANCE a 10000 km
- ✅ Timestamp en formato ISO 8601
- ✅ Tipos de alerta son válidos (Strategy Pattern)

**Total: 60+ assertions automatizadas**

## 🎯 Validaciones de Patrones

### Observer Pattern
El request **"5. Actualizar Kilometraje"** y **"6. Obtener Alertas"** validan que:
- Al actualizar kilometraje se generan alertas automáticamente
- Las alertas se crean sin intervención manual
- El sistema notifica correctamente los eventos

### Strategy Pattern
El request **"10. Actualizar a 100k km"** valida que:
- Se ejecutan todas las estrategias (Basic, Major, Critical)
- Cada estrategia genera su alerta correspondiente
- Las estrategias son extensibles (OCP)

### Repository Pattern
Todos los requests validan que:
- La persistencia funciona correctamente (SQLite)
- Las operaciones CRUD son consistentes
- El cascade delete funciona automáticamente

## 📊 Cobertura de Pruebas

| Endpoint | Method | Tests | Validaciones |
|----------|--------|-------|--------------|
| `/vehicles` | GET | 6 | Health check, lista, schemas |
| `/vehicles` | POST | 6 | Creación, validación, tipos |
| `/vehicles/{id}` | GET | 5 | Obtención por ID, datos |
| `/vehicles/{id}/mileage` | PUT | 5 | Actualización, reglas negocio |
| `/vehicles/{id}/alerts` | GET | 8 | Observer Pattern, schemas |
| `/vehicles/{id}` | DELETE | 3 | Cascade, 204 response |

**Total: 6 endpoints, 10 requests, 60+ tests automatizados**

## ⚙️ Configuración de Variables

### Variables de Colección
- `baseUrl`: URL base de la API (default: http://localhost:8000)
- `vehicleId`: ID del vehículo creado (auto-configurado)
- `criticalVehicleId`: ID para prueba de umbral crítico (auto-configurado)

### Modificar baseUrl para otros entornos

**Desarrollo:**
```json
"baseUrl": "http://localhost:8000"
```

**Staging:**
```json
"baseUrl": "https://staging-automotive.azurewebsites.net"
```

**Producción:**
```json
"baseUrl": "https://automotive-api.azurewebsites.net"
```

## 🐛 Troubleshooting

### Error: "Could not get any response"
**Solución:** Verificar que el servidor FastAPI esté ejecutándose:
```bash
uvicorn src.web.main:app --reload
```

### Error: "404 Not Found" en todos los requests
**Solución:** Verificar que `baseUrl` sea correcto:
- En Postman Desktop: http://localhost:8000
- En Postman Web: usar ngrok si es necesario

### Tests fallan con "vehicleId is undefined"
**Solución:** Ejecutar requests en orden. El request "2. Crear Vehículo" configura `vehicleId`.

### Error: "ECONNREFUSED"
**Solución:** Firewall bloqueando Postman. Agregar excepción o usar Postman Web.

## 📝 Notas Importantes

1. **Orden de ejecución**: Los requests deben ejecutarse en orden (1-10) para garantizar el flujo CRUD completo.

2. **Variables automáticas**: `vehicleId` y `criticalVehicleId` se configuran automáticamente durante la ejecución.

3. **Pre-request scripts**: El request #10 incluye un script que crea un vehículo adicional automáticamente.

4. **Cleanup automático**: No es necesario limpiar datos entre ejecuciones (SQLite en memoria).

5. **Tests asíncronos**: El request #10 usa `setTimeout` para validar alertas después de la actualización.

## 🔗 Referencias

- [Postman Documentation](https://learning.postman.com/)
- [Newman CLI](https://www.npmjs.com/package/newman)
- [Postman JavaScript Reference](https://learning.postman.com/docs/writing-scripts/script-references/postman-sandbox-api-reference/)
- [API REST Documentation](../../README.md)

## 📧 Soporte

Para reportar issues o sugerencias, contactar a: gerardo.leyton@sofka.com.co
