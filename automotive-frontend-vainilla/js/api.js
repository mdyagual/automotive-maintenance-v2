/**
 * API Service - Wrapper para comunicación con el backend
 * Base URL del backend: http://127.0.0.1:8000
 */

const API_BASE_URL = 'http://127.0.0.1:8000';

/**
 * Manejo centralizado de errores HTTP
 * @param {Response} response - Respuesta fetch
 * @returns {Promise<any>} - Datos parseados o error
 */
async function handleResponse(response) {
    if (!response.ok) {
        let errorMessage = `Error ${response.status}: ${response.statusText}`;

        try {
            const errorData = await response.json();
            if (errorData.detail) {
                errorMessage = errorData.detail;
            }
        } catch (e) {
            // Si no se puede parsear el error, usar mensaje por defecto
        }

        throw new Error(errorMessage);
    }

    // 204 No Content no tiene body
    if (response.status === 204) {
        return null;
    }

    return response.json();
}

/**
 * API Service Object
 */
const API = {
    /**
     * Obtener todos los vehículos con sus alertas
     * GET /vehicles
     * @returns {Promise<Array>} - Lista de vehículos con alertas
     */
    async getAllVehicles() {
        const response = await fetch(`${API_BASE_URL}/vehicles`);
        return handleResponse(response);
    },

    /**
     * Obtener un vehículo por ID
     * GET /vehicles/{vehicle_id}
     * @param {string} vehicleId - ID del vehículo
     * @returns {Promise<Object>} - Datos del vehículo
     */
    async getVehicle(vehicleId) {
        const response = await fetch(`${API_BASE_URL}/vehicles/${vehicleId}`);
        return handleResponse(response);
    },

    /**
     * Crear un nuevo vehículo
     * POST /vehicles
     * @param {Object} vehicleData - Datos del vehículo
     * @param {string} vehicleData.id - ID del vehículo (formato V-XXX)
     * @param {string} vehicleData.plate - Placa (formato XXX-123)
     * @param {string} vehicleData.model - Modelo del vehículo
     * @param {number} vehicleData.initial_mileage - Kilometraje inicial
     * @returns {Promise<Object>} - Vehículo creado
     */
    async createVehicle(vehicleData) {
        const response = await fetch(`${API_BASE_URL}/vehicles`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(vehicleData),
        });
        return handleResponse(response);
    },

    /**
     * Actualizar kilometraje de un vehículo
     * PUT /vehicles/{vehicle_id}/mileage
     * @param {string} vehicleId - ID del vehículo
     * @param {number} newMileage - Nuevo kilometraje
     * @returns {Promise<Object>} - Vehículo actualizado
     */
    async updateMileage(vehicleId, newMileage) {
        const response = await fetch(`${API_BASE_URL}/vehicles/${vehicleId}/mileage`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ new_mileage: newMileage }),
        });
        return handleResponse(response);
    },

    /**
     * Eliminar un vehículo
     * DELETE /vehicles/{vehicle_id}
     * @param {string} vehicleId - ID del vehículo
     * @returns {Promise<null>} - 204 No Content
     */
    async deleteVehicle(vehicleId) {
        const response = await fetch(`${API_BASE_URL}/vehicles/${vehicleId}`, {
            method: 'DELETE',
        });
        return handleResponse(response);
    },

    /**
     * Obtener alertas de un vehículo
     * GET /vehicles/{vehicle_id}/alerts
     * @param {string} vehicleId - ID del vehículo
     * @returns {Promise<Array>} - Lista de alertas
     */
    async getVehicleAlerts(vehicleId) {
        const response = await fetch(`${API_BASE_URL}/vehicles/${vehicleId}/alerts`);
        return handleResponse(response);
    },
};

// Exportar para uso en otros scripts
window.API = API;
