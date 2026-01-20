# 🚀 Quick Start Guide

## Paso 1: Instalar Dependencias

```bash
cd automotive-frontend
npm install
```

## Paso 2: Iniciar el Backend

En una terminal separada, inicia el backend FastAPI:

```bash
cd ../automotive-backend
python -m uvicorn src.web.main:app --reload
```

Verifica que el backend esté corriendo en: http://127.0.0.1:8000/docs

## Paso 3: Iniciar el Frontend

```bash
npm run dev
```

La aplicación estará disponible en: http://localhost:5173

## Paso 4: Probar la Aplicación

1. Abre http://localhost:5173 en tu navegador
2. Haz clic en "Registrar Vehículo"
3. Completa el formulario:
   - ID: V-001
   - Placa: ABC-123
   - Modelo: Toyota Corolla 2020
   - Kilometraje: 5000
4. Haz clic en "Registrar"
5. El vehículo aparecerá en el dashboard

## Funcionalidades Disponibles

- ✅ Ver todos los vehículos
- ✅ Registrar nuevo vehículo
- ✅ Actualizar kilometraje
- ✅ Ver detalles del vehículo
- ✅ Ver alertas de mantenimiento
- ✅ Eliminar vehículo

## Troubleshooting

### El frontend no se conecta al backend

1. Verifica que el backend esté corriendo: http://127.0.0.1:8000/docs
2. Verifica que no haya errores de CORS en la consola del navegador
3. Verifica que la URL en `src/services/api.ts` sea correcta

### Error de compilación TypeScript

```bash
# Limpia node_modules y reinstala
rm -rf node_modules package-lock.json
npm install
```

### Puerto 5173 ya está en uso

```bash
# Mata el proceso en el puerto 5173
# Windows:
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# O cambia el puerto en vite.config.js:
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000
  }
})
```

## Estructura del Proyecto

```
automotive-frontend/
├── src/
│   ├── components/          # Componentes React
│   ├── hooks/              # Custom hooks
│   ├── services/           # API services
│   ├── types/              # TypeScript types
│   ├── utils/              # Utilidades
│   ├── App.tsx             # Componente principal
│   └── main.tsx            # Entry point
├── index.html
└── package.json
```

## Próximos Pasos

- Explora el código en `src/`
- Revisa los componentes en `src/components/`
- Modifica los estilos en `src/App.css`
- Agrega nuevas funcionalidades

¡Disfruta desarrollando! 🚗✨
