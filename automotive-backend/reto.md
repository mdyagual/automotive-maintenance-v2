# **Reto Parcial 2 - Automotive: Gestión de Flota y Mantenimiento**

## **Objetivo**
Implementar el sistema **Automotive: Gestión de Flota y Mantenimiento** aplicando **TDD estricto**, **Arquitectura Limpia**, y principios **SOLID**, evidenciando claramente en el historial de Git que los tests fueron creados **ANTES o en conjunto con el código**, **no al final**.

---

## **Descripción del Sistema**
El sistema debe gestionar una flota de vehículos, monitoreando el kilometraje y generando alertas automáticas cuando se requiere mantenimiento. Debe implementar:

1. **Patrón Observer**: Para notificar automáticamente cuando un vehículo alcanza un umbral de kilometraje.
2. **Cobertura de pruebas >= 70%**.
3. **Arquitectura Limpia** con separación de capas (Domain, Application, Infrastructure, API).
4. **Principios SOLID** aplicados en todo el diseño.
5. **TDD estricto**: El historial de Git debe demostrar que se escribieron pruebas primero.

---

## **Requisitos Funcionales**

### **1. Gestión de Vehículos**
- Registrar vehículos con: `id`, `placa`, `modelo`, `kilometraje_actual`.
- Actualizar el kilometraje de un vehículo.
- **Validaciones** al actualizar kilometraje:
  - El nuevo kilometraje debe ser mayor al actual.
  - No puede ser negativo.
  - No puede ser cero si ya tiene kilometraje registrado.
  - No puede exceder un límite razonable (ej. 1,000,000 km).
  - No puede incrementarse más de 50,000 km de una sola vez (validación de negocio).

### **2. Sistema de Alertas (Patrón Observer)**
- Implementar un **EventBus** o **Observer Pattern** para notificar cuando:
  - Un vehículo alcanza un múltiplo de 10,000 km (ej. 10000, 20000, 30000...).
  - Un vehículo supera un umbral crítico (ej. 100,000 km).
- Las alertas deben registrarse con: `id`, `vehiculo_id`, `tipo_alerta`, `kilometraje`, `fecha`.

### **3. Reglas de Mantenimiento**
- Implementar una **Strategy Pattern** para definir reglas de mantenimiento:
  - **Mantenimiento básico**: cada 10,000 km.
  - **Mantenimiento mayor**: cada 50,000 km.
- Las reglas deben ser extensibles sin modificar el código existente (OCP - Open/Closed Principle).

---

## **Requisitos Técnicos**

### **Arquitectura Limpia**
Organizar el proyecto en capas:

```
src/
├── domain/            # Entidades, excepciones, contratos
├── application/       # Casos de uso, servicios
├── infrastructure/    # Implementaciones concretas (DB, EventBus, etc.)
└── api/              # Controladores/endpoints (FastAPI, Flask, etc.)
```

### **Principios SOLID**
- **SRP**: Cada clase tiene una única responsabilidad.
- **OCP**: Extensible sin modificar código existente (Strategy para reglas).
- **LSP**: Las implementaciones cumplen los contratos.
- **ISP**: Interfaces específicas (no interfaces gordas).
- **DIP**: Depender de abstracciones, no de implementaciones concretas.

### **TDD Estricto**
- **RED**: Escribir un test que falle.
- **GREEN**: Escribir el código mínimo para que pase.
- **REFACTOR**: Mejorar el código sin cambiar funcionalidad.
- **Git**: Commits frecuentes mostrando el ciclo RED → GREEN → REFACTOR.

### **Cobertura de Pruebas >= 70%**
- Usar `pytest` + `pytest-cov` (Python) o similar.
- Incluir:
  - **Pruebas unitarias**: Lógica de dominio, validaciones.
  - **Pruebas de integración**: EventBus, persistencia, endpoints.

---

## **Entregables**

### **1. Código Fuente**
- Repositorio Git con historial limpio.
- README con instrucciones de instalación y ejecución.

### **2. Evidencia de TDD**
- **Historial de Git** que muestre:
  - Commits de tests **antes** del código de producción.
  - Alternancia clara entre RED → GREEN → REFACTOR.
- **Ejemplo de mensaje de commit**:
  ```
  RED: Test para validar kilometraje negativo
  GREEN: Implementar validación de kilometraje
  REFACTOR: Extraer validaciones a método privado
  ```

### **3. Pruebas y Cobertura**
- Reporte de cobertura >= 70%.
- Comando para ejecutar pruebas: `pytest --cov=src`.

### **4. Documentación**
- README explicando:
  - Arquitectura del sistema.
  - Cómo ejecutar el proyecto.
  - Cómo ejecutar las pruebas.
  - Patrones aplicados (Observer, Strategy).
  - Principios SOLID implementados.

---

## **Criterios de Evaluación**

| **Criterio**                          | **Peso** |
|---------------------------------------|----------|
| TDD estricto (historial Git)          | 30%      |
| Arquitectura Limpia                   | 20%      |
| Principios SOLID                      | 20%      |
| Patrón Observer implementado          | 15%      |
| Cobertura de pruebas >= 70%           | 10%      |
| Documentación y claridad del código   | 5%       |

---

## **Notas Importantes**
- **No hacer trampa con TDD**: El historial de Git será revisado. Si se detecta que los tests fueron escritos al final, se penalizará severamente.
- **Usar buenas prácticas**: Nombres claros, código limpio, commits atómicos.
- **Extensibilidad**: El sistema debe poder agregar nuevas reglas de mantenimiento sin modificar código existente.

---

**¡Éxito en el reto!** 🚗⚙️
