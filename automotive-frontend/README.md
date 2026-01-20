# 🚗 Frontend React - Sistema de Gestión de Flota Vehicular

Interfaz web moderna construida con React + TypeScript para la gestión de flota vehicular con monitoreo de mantenimiento preventivo.

## 📋 Características

- ✅ Dashboard con estadísticas en tiempo real
- ✅ Registro de nuevos vehículos
- ✅ Actualización de kilometraje
- ✅ Visualización de alertas de mantenimiento
- ✅ Eliminación de vehículos
- ✅ Interfaz responsive y moderna
- ✅ Validaciones en tiempo real
- ✅ Notificaciones toast
- ✅ TypeScript para type safety
- ✅ Hooks personalizados para lógica reutilizable

## 🛠️ Tecnologías

- **React 19**: Biblioteca UI
- **TypeScript**: Type safety
- **Vite**: Build tool y dev server
- **CSS3**: Diseño moderno con CSS Variables
- **Fetch API**: Comunicación con backend

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
automotive-frontend/
├── src/
│   ├── components/          # Componentes React
│   │   ├── modals/         # Componentes de modales
│   │   ├── Header.tsx
│   │   ├── Stats.tsx
│   │   ├── VehicleCard.tsx
│   │   ├── VehicleGrid.tsx
│   │   ├── Modal.tsx
│   │   └── Toast.tsx
│   ├── hooks/              # Custom hooks
│   │   ├── useVehicles.ts
│   │   └── useToast.ts
│   ├── services/           # API services
│   │   └── api.ts
│   ├── types/              # TypeScript types
│   │   └── vehicle.ts
│   ├── utils/              # Utilidades
│   │   └── formatters.ts
│   ├── App.tsx             # Componente principal
│   ├── App.css             # Estilos globales
│   └── main.tsx            # Entry point
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## 🚀 Instalación y Uso

### Prerrequisitos

- Node.js 18+ y npm
- Backend FastAPI corriendo en `http://127.0.0.1:8000`

### Instalación

```bash
# Instalar dependencias
npm install
```

### Desarrollo

```bash
# Iniciar servidor de desarrollo
npm run dev
```

La aplicación estará disponible en `http://localhost:5173`

### Producción

```bash
# Construir para producción
npm run build

# Preview de build de producción
npm run preview
```

## 🔌 Conexión con Backend

El frontend se conecta al backend FastAPI en `http://127.0.0.1:8000`.

### Endpoints utilizados:

- `GET /vehicles` - Obtener todos los vehículos
- `GET /vehicles/{id}` - Obtener un vehículo
- `POST /vehicles` - Crear vehículo
- `PUT /vehicles/{id}/mileage` - Actualizar kilometraje
- `DELETE /vehicles/{id}` - Eliminar vehículo

### Configurar URL del backend:

Editar `src/services/api.ts`:

```typescript
const API_BASE_URL = 'http://127.0.0.1:8000'; // Cambiar según entorno
```

## 🧩 Componentes Principales

### Hooks Personalizados

- **useVehicles**: Maneja el estado y operaciones CRUD de vehículos
- **useToast**: Maneja notificaciones toast

### Componentes

- **Header**: Barra de navegación con botón de registro
- **Stats**: Tarjetas de estadísticas
- **VehicleCard**: Tarjeta individual de vehículo
- **VehicleGrid**: Grid de vehículos con estado vacío
- **Modal**: Componente modal reutilizable
- **Toast**: Sistema de notificaciones

### Modales

- **CreateVehicleModal**: Formulario de registro
- **DetailsModal**: Detalles del vehículo
- **UpdateMileageModal**: Actualizar kilometraje
- **AlertsModal**: Ver alertas de mantenimiento
- **DeleteModal**: Confirmar eliminación

## 🐛 Troubleshooting

### Error: "Failed to fetch"

**Problema**: No se puede conectar al backend

**Solución**:
1. Verificar que el backend esté corriendo: `http://127.0.0.1:8000/docs`
2. Verificar CORS en el backend (debe permitir `http://localhost:5173`)
3. Verificar la URL en `src/services/api.ts`

### Error: CORS

**Problema**: Política CORS bloquea las peticiones

**Solución**: Asegurar que el backend tenga configurado CORS para permitir el origen del frontend:

```python
# En el backend (main.py)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📚 Recursos Adicionales

- **Mockups**: Ver `../automotive-backend/docs/design/mockups/`
- **Especificaciones**: Ver `../automotive-backend/docs/design/DESIGN.md`
- **API Docs**: http://127.0.0.1:8000/docs
- **Postman Collection**: Ver `../automotive-backend/docs/postman/`

## 🔜 Próximos Pasos

1. **Tests**: Implementar tests con Vitest + React Testing Library
2. **E2E Tests**: Implementar con Playwright
3. **CI/CD**: Configurar pipeline de deployment
4. **Optimización**: Code splitting y lazy loading
5. **PWA**: Convertir en Progressive Web App

## 👨‍💻 Desarrollo

### Scripts disponibles

- `npm run dev` - Servidor de desarrollo
- `npm run build` - Build de producción
- `npm run preview` - Preview del build
- `npm run lint` - Linter ESLint

### Convenciones de código

- Componentes en PascalCase
- Hooks con prefijo `use`
- Tipos en archivos `.ts` separados
- CSS con metodología BEM implícita

---

**Versión:** 1.0  
**Última actualización:** Enero 2026  
**Migrado de:** Vanilla JS a React + TypeScript
