# Especificaciones de Diseño UI/UX
## Sistema de Gestión de Flota Vehicular

---

## 📋 Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Paleta de Colores](#paleta-de-colores)
3. [Tipografía](#tipografía)
4. [Componentes UI](#componentes-ui)
5. [Mockups](#mockups)
6. [Responsividad](#responsividad)
7. [Interacciones y Estados](#interacciones-y-estados)
8. [Accesibilidad](#accesibilidad)

---

## Visión General

Sistema web de gestión de flota vehicular enfocado en monitoreo de mantenimiento preventivo. Diseñado para administradores/gestores de flota con énfasis en:

- **Claridad visual:** Información crítica destacada (alertas, kilometraje)
- **Eficiencia:** Flujos cortos para tareas frecuentes (actualizar KM, consultar alertas)
- **Feedback inmediato:** Validaciones en tiempo real, notificaciones claras
- **Profesionalismo:** Paleta corporativa, diseño clean y moderno

**Target:** Desktop-first (gestores usan principalmente computadoras de escritorio)

---

## Paleta de Colores

### Colores Principales

```css
/* Primario - Acciones principales */
--primary-600: #2563EB;        /* Botones primarios, links */
--primary-700: #1D4ED8;        /* Hover primario */
--primary-100: #DBEAFE;        /* Backgrounds sutiles */

/* Secundario - Elementos neutrales */
--gray-900: #111827;           /* Texto principal */
--gray-700: #374151;           /* Texto secundario */
--gray-500: #6B7280;           /* Helper text */
--gray-300: #D1D5DB;           /* Bordes */
--gray-100: #F3F4F6;           /* Backgrounds */
--gray-50: #F9FAFB;            /* Background principal */

/* Estados y Alertas */
--success-600: #10B981;        /* Éxito, sin alertas */
--success-100: #D1FAE5;        /* Background éxito */

--warning-600: #F59E0B;        /* Advertencias, alertas MAJOR */
--warning-100: #FEF3C7;        /* Background advertencia */

--error-600: #EF4444;          /* Errores, alertas CRITICAL */
--error-700: #DC2626;          /* Hover destructivo */
--error-100: #FEE2E2;          /* Background error */

--info-600: #3B82F6;           /* Alertas BASIC, información */
--info-100: #DBEAFE;           /* Background info */
```

### Uso por Contexto

| Elemento | Color | Hex |
|----------|-------|-----|
| Botón primario | Primary | #2563EB |
| Botón destructivo | Error | #EF4444 |
| Badge "Sin alertas" | Success | #10B981 |
| Badge "1-2 alertas" | Warning | #F59E0B |
| Badge "3+ alertas" | Error | #EF4444 |
| Alerta BASIC | Info | #3B82F6 |
| Alerta MAJOR | Warning | #F59E0B |
| Alerta CRITICAL | Error | #EF4444 |

---

## Tipografía

### Fuente

**Inter** (Google Fonts)
- Versatil, legible, profesional
- Excelente para interfaces web modernas
- Soporta números tabulares (importante para kilometrajes)

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### Escalas de Texto

```css
/* Títulos principales */
--text-3xl: 32px;              /* H1 - Títulos de página */
--text-2xl: 24px;              /* H2 - Secciones principales */
--text-xl: 20px;               /* H3 - Subtítulos */

/* Cuerpo */
--text-base: 16px;             /* Texto estándar */
--text-sm: 14px;               /* Texto secundario */
--text-xs: 12px;               /* Helper text, timestamps */

/* Pesos */
--font-normal: 400;            /* Cuerpo regular */
--font-medium: 500;            /* Énfasis leve */
--font-semibold: 600;          /* Subtítulos, labels */
--font-bold: 700;              /* Títulos, números destacados */
```

### Aplicación

| Elemento | Tamaño | Peso | Color |
|----------|--------|------|-------|
| Título de página | 32px | Bold (700) | Gray-900 |
| Título de modal | 24px | Semibold (600) | Gray-900 |
| Placa de vehículo | 24px | Bold (700) | Gray-900 |
| Kilometraje destacado | 20px | Bold (700) | Primary-600 |
| Label de formulario | 14px | Medium (500) | Gray-700 |
| Cuerpo de texto | 16px | Regular (400) | Gray-700 |
| Helper text | 12px | Regular (400) | Gray-500 |
| Timestamp | 12px | Regular (400) | Gray-500 |

---

## Componentes UI

### Botones

#### Botón Primario
```
Background: Primary-600 (#2563EB)
Texto: Blanco, 14px, Semibold
Padding: 12px 24px
Border-radius: 8px
Hover: Primary-700 (#1D4ED8)
Active: Escala 98%
Shadow: 0 1px 2px rgba(0,0,0,0.05)
```

#### Botón Destructivo
```
Background: Error-600 (#EF4444)
Texto: Blanco, 14px, Semibold
Padding: 12px 24px
Border-radius: 8px
Hover: Error-700 (#DC2626)
Active: Escala 98%
```

#### Botón Secundario
```
Background: Transparente
Texto: Gray-700, 14px, Semibold
Border: 1px solid Gray-300
Padding: 12px 24px
Border-radius: 8px
Hover: Background Gray-100
```

#### Estado Deshabilitado
```
Opacity: 0.5
Cursor: not-allowed
```

---

### Inputs

```
Altura: 48px
Padding: 12px 16px
Border: 1px solid Gray-300
Border-radius: 8px
Font-size: 16px
Color: Gray-900

Focus:
  Border: 2px solid Primary-600
  Shadow: 0 0 0 3px Primary-100

Error:
  Border: 2px solid Error-600
  Shadow: 0 0 0 3px Error-100

Success:
  Border: 2px solid Success-600
  Shadow: 0 0 0 3px Success-100
```

**Label:**
- Font-size: 14px, Medium (500)
- Color: Gray-700
- Margin-bottom: 6px

**Helper Text:**
- Font-size: 12px, Regular (400)
- Color: Gray-500 (normal) / Error-600 (error)
- Margin-top: 4px

---

### Cards

```
Background: White
Border: 1px solid Gray-200
Border-radius: 12px
Padding: 20px
Shadow: 0 1px 3px rgba(0,0,0,0.1)

Hover (interactivas):
  Shadow: 0 4px 6px rgba(0,0,0,0.1)
  Transform: translateY(-2px)
  Transition: all 0.2s ease
```

---

### Badges

#### Badge de Estado
```
Padding: 4px 12px
Border-radius: 12px (píldora)
Font-size: 12px, Semibold

Verde (Sin alertas):
  Background: Success-100
  Color: Success-700

Amarillo (1-2 alertas):
  Background: Warning-100
  Color: Warning-700

Rojo (3+ alertas):
  Background: Error-100
  Color: Error-700
```

#### Badge de ID de Vehículo
```
Padding: 6px 12px
Border-radius: 6px
Font-size: 14px, Bold
Background: Primary-100
Color: Primary-700
```

---

### Modales

```
Backdrop:
  Background: rgba(0, 0, 0, 0.5)
  Backdrop-filter: blur(4px)

Modal:
  Max-width: 600px
  Background: White
  Border-radius: 16px
  Padding: 32px
  Shadow: 0 20px 25px rgba(0,0,0,0.15)

Header:
  Margin-bottom: 24px
  Título: 24px, Semibold

Footer:
  Margin-top: 32px
  Display: flex, justify-content: flex-end
  Gap: 12px entre botones
```

---

### Toasts / Notificaciones

```
Posición: Top-right, fixed
Width: 400px
Background: White
Border-left: 4px solid (Success/Error/Warning)
Border-radius: 8px
Padding: 16px 20px
Shadow: 0 4px 6px rgba(0,0,0,0.1)
Duración: 3 segundos
Animación: Slide-in desde derecha

Iconos:
  Success: ✓ (Check circle)
  Error: ✕ (X circle)
  Warning: ⚠ (Alert triangle)
```

---

### Tablas / Cards de Vehículos

```
Grid de Cards (Desktop):
  Display: grid
  Grid-template-columns: repeat(auto-fill, minmax(320px, 1fr))
  Gap: 24px

Card de Vehículo:
  Padding: 24px
  Display: flex, flex-direction: column
  Gap: 12px

  Header:
    ID Badge + Indicador de alertas
  
  Body:
    Placa (grande, destacada)
    Modelo (secundario)
    Kilometraje con icono
  
  Footer:
    Botones de acción (icónicos)
    Gap: 8px
```

---

## Mockups

Los mockups están organizados por flujo de usuario:

### 1. Dashboard Principal
**Archivo:** `mockups/01-dashboard.png`

**Elementos clave:**
- Grid de cards de vehículos
- Filtros y búsqueda
- Botón CTA "Registrar Nuevo Vehículo"
- Estado vacío ilustrado

### 2. Modal: Registrar Nuevo Vehículo
**Archivo:** `mockups/02-modal-registro-vehiculo.png`

**Elementos clave:**
- Formulario de 4 campos con validaciones
- Helper texts instructivos
- Estados de error inline
- Botones primario/secundario

### 3. Detalle de Vehículo
**Archivo:** `mockups/03-detalle-vehiculo.png`

**Elementos clave:**
- Header con información principal
- Card de información general con barras de progreso
- Lista de alertas cronológica
- Botones de acción destacados

### 4. Modal: Actualizar Kilometraje
**Archivo:** `mockups/04-modal-actualizar-km.png`

**Elementos clave:**
- Input con validaciones en tiempo real
- Información contextual (km actual)
- Banner de advertencia si generará alertas
- Mensaje de éxito con acción secundaria

### 5. Modal: Confirmar Eliminación
**Archivo:** `mockups/05-modal-confirmar-eliminacion.png`

**Elementos clave:**
- Icono de advertencia prominente
- Resumen de lo que se eliminará
- Checkbox de confirmación (patrón destructivo)
- Botón destructivo deshabilitado por defecto

---

## Responsividad

### Breakpoints

```css
/* Desktop (diseño principal) */
@media (min-width: 1024px) {
  /* Grid de 3-4 columnas */
  /* Modales 600px ancho */
}

/* Tablet */
@media (min-width: 768px) and (max-width: 1023px) {
  /* Grid de 2 columnas */
  /* Modales 500px ancho */
}

/* Mobile */
@media (max-width: 767px) {
  /* Stack vertical */
  /* Modales full-width con margin lateral */
  /* Botones full-width */
}
```

### Adaptaciones Mobile

- **Dashboard:** Cards apiladas verticalmente
- **Tabla de acciones:** Iconos más grandes (touch-friendly)
- **Modales:** Ocupan 90% del ancho de pantalla
- **Inputs:** Altura aumentada a 52px
- **Header:** Logo más pequeño, menú hamburguesa

---

## Interacciones y Estados

### Estados de UI

#### Loading
```
Spinners: Primary-600
Ubicación: Dentro de botones o centrado
Skeleton screens para carga inicial de datos
```

#### Empty States
```
Ilustración centrada (icono SVG simple)
Título: Gray-900, 20px, Semibold
Descripción: Gray-500, 14px
CTA button debajo
```

#### Error States
```
Color: Error-600
Icono: X circle o alert triangle
Mensaje descriptivo (no técnico)
Acción sugerida cuando aplique
```

#### Success States
```
Toast notification verde
Icono: Check circle
Mensaje confirmatorio
Auto-dismiss en 3s
```

### Transiciones

```css
/* Botones */
transition: all 0.2s ease;

/* Cards hover */
transition: transform 0.2s ease, box-shadow 0.2s ease;

/* Modales */
transition: opacity 0.3s ease, transform 0.3s ease;

/* Inputs focus */
transition: border-color 0.2s ease, box-shadow 0.2s ease;
```

### Animaciones

- **Modal entrada:** Fade-in + Scale up (0.95 → 1)
- **Toast entrada:** Slide-in desde derecha
- **Cards hover:** Translate-Y(-2px)
- **Botones activos:** Scale(0.98)

---

## Accesibilidad

### Contraste

Todos los textos cumplen WCAG 2.1 AA:
- Gray-900 sobre blanco: 17.7:1 ✅
- Gray-700 sobre blanco: 10.5:1 ✅
- Primary-600 sobre blanco: 5.9:1 ✅
- Texto blanco sobre Primary-600: 5.9:1 ✅

### Navegación por Teclado

- **Tab order:** Lógico, secuencial
- **Focus visible:** Border Primary-600 + shadow
- **Esc:** Cierra modales
- **Enter:** Confirma acciones

### Semántica HTML

```html
<!-- Botones de acción -->
<button type="button">Actualizar</button>

<!-- Links de navegación -->
<a href="/vehicles/V-123">Ver Detalles</a>

<!-- Labels asociados -->
<label for="vehicle-id">ID del Vehículo</label>
<input id="vehicle-id" type="text" />

<!-- Alertas -->
<div role="alert" aria-live="polite">
  Vehículo registrado exitosamente
</div>
```

### Screen Readers

- Textos alternativos en iconos
- ARIA labels en botones icónicos
- Mensajes de error asociados a inputs (`aria-describedby`)
- Estados de carga anunciados (`aria-busy`, `aria-live`)

---

## Referencias Técnicas

### Integración con API

La UI consume estos endpoints (ver [README.md](../../README.md)):

| Endpoint | Método | Pantalla |
|----------|--------|----------|
| `/vehicles` | POST | Modal registro |
| `/vehicles` | GET | Dashboard |
| `/vehicles/{id}` | GET | Detalle vehículo |
| `/vehicles/{id}/mileage` | PUT | Modal actualizar KM |
| `/vehicles/{id}` | DELETE | Modal confirmar eliminación |

### Validaciones Frontend (coinciden con backend)

Implementar validaciones del lado del cliente que coincidan con reglas de negocio (ver [USER_STORIES.md](../../USER_STORIES.md)):

- **RN-001:** Kilometraje siempre mayor al actual
- **RN-002:** Kilometraje no negativo
- **RN-003:** Kilometraje máximo 1,000,000 km
- **RN-004:** Incremento máximo 50,000 km
- **RN-008:** ID único (validar con backend)
- **RN-009:** Placa única (validar con backend)
- **RN-010:** Formato placa XXX-### o XXX-####
- **RN-011:** Formato ID V-XXX

---

## Próximos Pasos

1. ✅ Generar mockups en Stitch usando este documento
2. ⏳ Colocar mockups en `docs/design/mockups/`
3. ⏳ Implementar frontend con React/Vue/Angular
4. ⏳ Validar usabilidad con usuarios reales
5. ⏳ Iterar basado en feedback

---

**Versión:** 1.0  
**Última actualización:** Enero 2026  
**Autor:** Equipo de Desarrollo - Automotive Fleet Manager
