# 🚗 Frontend - Sistema de Gestión de Flota Vehicular

Interfaz web para la gestión de flota vehicular con monitoreo de mantenimiento preventivo.

## 📋 Características

- ✅ Dashboard con estadísticas en tiempo real
- ✅ Registro de nuevos vehículos
- ✅ Actualización de kilometraje
- ✅ Visualización de alertas de mantenimiento
- ✅ Eliminación de vehículos
- ✅ Interfaz responsive y moderna
- ✅ Validaciones en tiempo real
- ✅ Notificaciones toast

## 🛠️ Tecnologías

- **HTML5**: Estructura semántica
- **CSS3**: Diseño moderno con CSS Variables
- **JavaScript ES6+**: Lógica de aplicación
- **Fetch API**: Comunicación con backend
- **Sin frameworks**: Vanilla JavaScript puro

## 🎨 Design System

### Paleta de Colores

- **Primario**: `#2563EB` (Azul) - Acciones principales
- **Success**: `#10B981` (Verde) - Sin alertas
- **Warning**: `#F59E0B` (Naranja) - Alertas moderadas
- **Error**: `#EF4444` (Rojo) - Alertas críticas

### Tipografía

- **Fuente**: Inter (Google Fonts)
- **Tamaños**: 12px - 32px
- **Pesos**: 400, 500, 600, 700

## 📁 Estructura de Archivos

```
frontend/
├── index.html              # Página principal
├── css/
│   └── styles.css          # Estilos CSS
├── js/
│   ├── api.js             # Wrapper para API REST
│   └── app.js             # Lógica de la aplicación
└── README.md              # Este archivo
```

## 🚀 Instalación y Uso

### Prerrequisitos

1. **Backend ejecutándose** en `http://127.0.0.1:8000`
2. **Python 3.11+** instalado
3. **Navegador moderno** (Chrome, Firefox, Edge)

### Paso 1: Iniciar el Backend

```bash
# Desde la raíz del proyecto maintenance/
cd c:\Users\gerardo.leyton\Documents\sofka\trainning\Taller5\maintenance

# Iniciar el servidor backend
python -m uvicorn src.web.main:app --reload --port 8000
```

Verificar que el backend esté corriendo en: http://127.0.0.1:8000/docs

### Paso 2: Iniciar el Frontend

```bash
# Desde el directorio frontend/
cd frontend

# Iniciar servidor HTTP simple
python -m http.server 8080
```

### Paso 3: Abrir en el Navegador

Abrir: **http://localhost:8080**

## 📖 Guía de Uso

### 1. Registrar Vehículo

1. Clic en **"Registrar Vehículo"** (botón superior derecho)
2. Completar el formulario:
   - **ID**: Formato `V-XXX` (ejemplo: `V-001`)
   - **Placa**: Formato `XXX-123` o `XXX-1234` (ejemplo: `ABC-123`)
   - **Modelo**: Texto libre (ejemplo: `Toyota Corolla 2020`)
   - **Kilometraje Inicial**: Número entre 0 y 1,000,000
3. Clic en **"Registrar"**

### 2. Actualizar Kilometraje

1. Buscar el vehículo en el dashboard
2. Clic en **"Actualizar KM"**
3. Ingresar el nuevo kilometraje (debe ser mayor al actual)
4. Clic en **"Actualizar"**

**Nota**: Al actualizar el kilometraje, el sistema automáticamente:
- Genera alertas de mantenimiento según las reglas:
  - **BASIC**: Cada 5,000 km
  - **MAJOR**: Cada 20,000 km
  - **CRITICAL**: Al alcanzar 95,000 km o más

### 3. Ver Alertas

1. Clic en el **badge de alertas** del vehículo
2. Se abrirá un modal mostrando todas las alertas activas
3. Las alertas se clasifican por color:
   - 🔵 **Azul**: BASIC (mantenimiento básico)
   - 🟠 **Naranja**: MAJOR (mantenimiento mayor)
   - 🔴 **Rojo**: CRITICAL (umbral crítico)

### 4. Ver Detalles

1. Clic en **"Ver Detalles"**
2. Se muestra información completa del vehículo:
   - ID
   - Placa
   - Modelo
   - Kilometraje actual

### 5. Eliminar Vehículo

1. Clic en **"Eliminar"**
2. Confirmar en el modal de advertencia
3. El vehículo y todas sus alertas se eliminan permanentemente

## 🔗 API Endpoints Utilizados

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/vehicles` | Listar todos los vehículos con alertas |
| POST | `/vehicles` | Crear nuevo vehículo |
| GET | `/vehicles/{id}` | Obtener detalles de un vehículo |
| PUT | `/vehicles/{id}/mileage` | Actualizar kilometraje |
| DELETE | `/vehicles/{id}` | Eliminar vehículo |
| GET | `/vehicles/{id}/alerts` | Obtener alertas de un vehículo |

## ✅ Validaciones Implementadas

### Formulario de Registro

- **ID**: Debe seguir patrón `V-XXX` (V seguido de guion y 3 dígitos)
- **Placa**: Debe seguir patrón `XXX-123` o `XXX-1234` (3 letras mayúsculas, guion, 3-4 dígitos)
- **Modelo**: Campo obligatorio, texto libre
- **Kilometraje**: Número entre 0 y 1,000,000

### Formulario de Actualización

- **Nuevo Kilometraje**: Debe ser mayor al kilometraje actual
- **Validación en tiempo real**: El input muestra error si el valor no es válido

## 🎯 Características UX

### Notificaciones Toast

- **Posición**: Superior derecha
- **Duración**: 3 segundos
- **Tipos**:
  - ✅ **Success**: Operación exitosa
  - ❌ **Error**: Operación fallida
  - ⚠️ **Warning**: Advertencias
  - ℹ️ **Info**: Información general

### Estados Visuales

- **Empty State**: Se muestra cuando no hay vehículos registrados
- **Badges de Alertas**:
  - 🟢 Verde: 0 alertas
  - 🟡 Naranja: 1-2 alertas
  - 🔴 Rojo: 3+ alertas
- **Hover Effects**: Tarjetas y botones responden al hover
- **Loading States**: Feedback visual durante operaciones async

## 📱 Responsive Design

- **Desktop**: Grid de 3 columnas (>1024px)
- **Tablet**: Grid de 2 columnas (768px - 1024px)
- **Mobile**: Columna única (<768px)
- **Modales**: Se adaptan al tamaño de pantalla (95% en mobile)

## 🐛 Troubleshooting

### Error CORS

**Problema**: `CORS policy: No 'Access-Control-Allow-Origin' header`

**Solución**: Verificar que el backend tenga CORS habilitado en `src/web/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Error 404 al cargar recursos

**Problema**: Archivos CSS/JS no se cargan

**Solución**: Verificar que el servidor HTTP esté corriendo desde el directorio `frontend/`

### Backend no responde

**Problema**: Fetch falla con `Failed to fetch`

**Solución**:
1. Verificar que el backend esté corriendo: `http://127.0.0.1:8000/docs`
2. Verificar que la URL en `js/api.js` sea correcta: `http://127.0.0.1:8000`

## 📚 Recursos Adicionales

- **Mockups**: Ver `docs/design/mockups/` para diseños de referencia
- **Especificaciones**: Ver `docs/design/DESIGN.md` para design system completo
- **API Docs**: http://127.0.0.1:8000/docs (cuando el backend esté corriendo)
- **Postman Collection**: Ver `docs/postman/` para tests de API

## 🔜 Próximos Pasos

1. **Repositorio Separado**: Mover frontend a `automotive-frontend/` repo
2. **Tests E2E**: Implementar con Playwright + Screenplay pattern
3. **CI/CD**: Configurar pipeline de deployment
4. **Optimización**: Minificación CSS/JS para producción

## 👨‍💻 Desarrollo

### Estructura del Código

- **api.js**: Capa de comunicación con el backend (fetch wrapper)
- **app.js**: Lógica de negocio y manejo de UI
- **styles.css**: Design system con CSS Variables

### Buenas Prácticas Implementadas

- ✅ Separación de concerns (API, UI, Styles)
- ✅ Validaciones client-side + server-side
- ✅ Manejo centralizado de errores
- ✅ Feedback inmediato al usuario
- ✅ Código comentado y documentado
- ✅ Naming conventions consistentes

---

**Versión**: 1.0.0
**Última actualización**: Enero 2026
**Licencia**: MIT
