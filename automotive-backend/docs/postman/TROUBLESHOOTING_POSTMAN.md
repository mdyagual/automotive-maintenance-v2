# 🔧 Troubleshooting Postman - Automotive API

## ✅ Servidor Funcionando Correctamente

El servidor está **activo y respondiendo** en:
- ✅ http://127.0.0.1:8000
- ✅ http://127.0.0.1:8000/docs (Swagger UI)

## 🚨 Problemas Comunes y Soluciones

### 1. "Could not get any response" en Postman

**Causa:** El servidor no está ejecutándose.

**Solución:**
```powershell
# Ejecutar en terminal separado:
python -m uvicorn src.web.main:app --reload
```

**Verificar que funciona:**
- Abrir en navegador: http://127.0.0.1:8000/docs
- Debe mostrar la documentación Swagger

---

### 2. "Error: connect ECONNREFUSED 127.0.0.1:8000"

**Causa:** El puerto 8000 no está escuchando.

**Solución:**
```powershell
# Verificar si el puerto está en uso:
netstat -ano | findstr :8000

# Si no aparece nada, levantar el servidor:
python -m uvicorn src.web.main:app --reload
```

---

### 3. Requests fallan con "localhost" pero funcionan con "127.0.0.1"

**Causa:** Problema de resolución DNS en Windows.

**Solución:**

**Opción A - Usar 127.0.0.1 en Postman (RECOMENDADO):**
1. En Postman, editar el environment "Automotive - Local Development"
2. Cambiar `baseUrl` de `http://localhost:8000` a `http://127.0.0.1:8000`
3. Guardar y ejecutar requests

**Opción B - Verificar archivo hosts:**
```powershell
# Abrir archivo hosts como administrador:
notepad C:\Windows\System32\drivers\etc\hosts

# Verificar que existe esta línea:
127.0.0.1       localhost
```

---

### 4. Environment no está activo

**Síntoma:** Variables como `{{baseUrl}}` no se resuelven.

**Solución:**
1. En Postman, verificar el selector de environment (esquina superior derecha)
2. Seleccionar: **"Automotive - Local Development"**
3. Debe aparecer un ojo (👁️) para ver las variables

---

### 5. Variable `vehicleId` está vacía

**Síntoma:** Request "4. Obtener Vehículo por ID" falla con 404.

**Causa:** El request "2. Crear Vehículo" no se ejecutó o falló.

**Solución:**
1. Ejecutar requests **en orden** (1 → 2 → 3 → 4...)
2. Verificar que "2. Crear Vehículo" devuelve 201 Created
3. En Postman, ir a Environment → Ver variable `vehicleId` (debe tener valor "V-POSTMAN-001")

---

### 6. Tests fallan aunque la respuesta es 200 OK

**Causa:** Schema de respuesta cambió o datos incorrectos.

**Solución:**
1. Revisar la pestaña "Test Results" en Postman
2. Ver cuál assertion específica falló
3. Comparar con la respuesta en la pestaña "Body"

Ejemplo:
```javascript
pm.test("ID del vehículo es correcto", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData.id).to.eql("V-POSTMAN-001"); // Verificar este valor
});
```

---

### 7. Postman Web no puede conectar a localhost

**Causa:** Postman Web tiene restricciones de seguridad del navegador.

**Soluciones:**

**Opción A - Usar Postman Desktop (RECOMENDADO):**
- Descargar: https://www.postman.com/downloads/

**Opción B - Usar Postman Agent:**
1. En Postman Web, instalar "Postman Desktop Agent"
2. Seguir instrucciones en pantalla

**Opción C - Usar ngrok:**
```powershell
# Instalar ngrok: https://ngrok.com/download
ngrok http 8000

# Copiar URL pública (ej: https://abc123.ngrok.io)
# Actualizar baseUrl en Postman con esa URL
```

---

## ✅ Verificación Rápida

**Paso 1 - Servidor activo:**
```powershell
# Ejecutar en terminal:
Invoke-WebRequest -Uri "http://127.0.0.1:8000/vehicles" -UseBasicParsing
```

**Resultado esperado:**
```
StatusCode : 200
Content    : [{"id":"V-123","plate":"ABC-123","model":"Toyota Corolla","current_mileage":5000,"alerts":[]}]
```

**Paso 2 - Swagger UI accesible:**
- Abrir navegador: http://127.0.0.1:8000/docs
- Debe mostrar interfaz Swagger

**Paso 3 - Postman configurado:**
1. Collection importada ✅
2. Environment importado ✅
3. Environment **activo** (selector superior) ✅
4. `baseUrl` = `http://127.0.0.1:8000` ✅

---

## 🧪 Test Manual en Postman

**Request básico para verificar:**

```
Method: GET
URL: http://127.0.0.1:8000/vehicles
Headers: (ninguno necesario)
```

**Respuesta esperada:**
```json
[
  {
    "id": "V-123",
    "plate": "ABC-123",
    "model": "Toyota Corolla",
    "current_mileage": 5000,
    "alerts": []
  }
]
```

**Status Code:** 200 OK

---

## 📞 Checklist de Diagnóstico

Antes de reportar un problema, verificar:

- [ ] Servidor FastAPI está ejecutándose (`python -m uvicorn src.web.main:app --reload`)
- [ ] http://127.0.0.1:8000/docs abre correctamente en navegador
- [ ] Environment está **activo** en Postman (esquina superior derecha)
- [ ] `baseUrl` en environment es `http://127.0.0.1:8000` (NO localhost)
- [ ] Collection fue importada correctamente
- [ ] Requests se ejecutan en orden (1 → 2 → 3...)
- [ ] Firewall/Antivirus no bloquea puerto 8000

---

## 🐛 Logs de Depuración

**Ver logs del servidor:**
```powershell
# El servidor muestra logs automáticamente:
INFO:     127.0.0.1:xxxxx - "GET /vehicles HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "POST /vehicles HTTP/1.1" 201 Created
INFO:     127.0.0.1:xxxxx - "DELETE /vehicles/V-001 HTTP/1.1" 204 No Content
```

**Activar SQL logging (debugging):**

Editar `src/infrastructure/database/connection.py`:
```python
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True,  # Cambiar a True para ver queries SQL
)
```

---

## 📧 Soporte

Si el problema persiste:
1. Capturar screenshot del error en Postman
2. Copiar logs del servidor (terminal)
3. Verificar checklist de diagnóstico
4. Contactar: gerardo.leyton@sofka.com.co

---

## 🎯 Configuración Recomendada

**Environment correcto:**
```json
{
  "baseUrl": "http://127.0.0.1:8000",
  "vehicleId": "",
  "criticalVehicleId": ""
}
```

**Headers globales (opcional):**
```
Content-Type: application/json
Accept: application/json
```

---

## ✨ Tips Avanzados

### Usar Newman para debugging
```bash
newman run Automotive_Fleet_API.postman_collection.json \
  -e Automotive_Environment.postman_environment.json \
  --verbose
```

### Ver requests en tiempo real
```powershell
# En terminal del servidor, verás cada request:
INFO: 127.0.0.1:52341 - "GET /vehicles HTTP/1.1" 200 OK
```

### Limpiar base de datos
```powershell
# Detener servidor (Ctrl+C)
Remove-Item maintenance.db
# Reiniciar servidor - se creará nueva DB
```

---

**Última actualización:** 2026-01-07
**Versión API:** 1.0.0
