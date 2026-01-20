# Automotive Maintenance API - Colección Postman

Esta colección de Postman cubre todos los endpoints y escenarios del reto de mantenimiento automotriz, incluyendo lógica de negocio, historias de usuario y validaciones de alertas. Está lista para importar y ejecutar.

## Instrucciones de uso

1. **Arranca el backend**
   - Asegúrate de tener el backend corriendo en `http://localhost:8000`.
   - Si usas FastAPI:
     ```bash
     uvicorn src.web.main:app --reload
     ```

2. **Importa la colección en Postman**
   - Abre Postman.
   - Haz clic en `Import` > `Upload Files` y selecciona el archivo:
     - `postman/automotive-maintenance.postman_collection.json`

3. **Ejecuta los requests**
   - Cada request está documentado y cubre una historia de usuario o escenario de negocio:
     - Registrar vehículo
     - Obtener todos los vehículos
     - Actualizar kilometraje
     - Eliminar vehículo
     - Obtener alertas
     - Casos de error (placa duplicada, kilometraje inválido)
   - Puedes ejecutar los requests uno por uno o en orden para simular los flujos completos.

4. **Validación de alertas**
   - Al actualizar el kilometraje, revisa el endpoint de alertas para validar que se generen según la lógica de negocio y la imagen de referencia.

5. **Notas**
   - Modifica los datos de ejemplo (placa, kilometraje, etc.) si necesitas probar otros escenarios.
   - Si tienes dudas sobre los endpoints, revisa la documentación OpenAPI en `http://localhost:8000/docs`.

---

**Cubre todas las historias de usuario y reglas del reto.**

- Si necesitas agregar más escenarios, duplica y ajusta los requests en la colección.
- Para pruebas automáticas, puedes usar la pestaña `Tests` de Postman para validar respuestas.

¡Listo para importar y usar!
