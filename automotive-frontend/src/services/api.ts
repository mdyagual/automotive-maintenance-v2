import type {
  Vehicle,
  CreateVehicleRequest,
  UpdateMileageRequest,
  UpdateStatusRequest,
  VehicleStatus,
} from '../types/vehicle';

const API_BASE_URL = 'http://127.0.0.1:8000';

async function handleResponse<T>(response: Response): Promise<T | null> {
  if (!response.ok) {
    let errorMessage = `Error ${response.status}: ${response.statusText}`;

    try {
      const errorData = await response.json();
      if (errorData.detail) {
        errorMessage = errorData.detail;
      }
    } catch (e) {
      // Use default error message
    }

    throw new Error(errorMessage);
  }

  // 204 No Content
  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export const vehicleApi = {
  async getAllVehicles(): Promise<Vehicle[]> {
    const response = await fetch(`${API_BASE_URL}/vehicles`);
    return handleResponse<Vehicle[]>(response) as Promise<Vehicle[]>;
  },

  async getVehiclesByStatus(status: VehicleStatus): Promise<Vehicle[]> {
    const response = await fetch(`${API_BASE_URL}/vehicles?status=${status}`);
    return handleResponse<Vehicle[]>(response) as Promise<Vehicle[]>;
  },

  async getVehicle(vehicleId: string): Promise<Vehicle> {
    const response = await fetch(`${API_BASE_URL}/vehicles/${vehicleId}`);
    return handleResponse<Vehicle>(response) as Promise<Vehicle>;
  },

  async createVehicle(vehicleData: CreateVehicleRequest): Promise<Vehicle> {
    const response = await fetch(`${API_BASE_URL}/vehicles`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(vehicleData),
    });
    return handleResponse<Vehicle>(response) as Promise<Vehicle>;
  },

  async updateMileage(vehicleId: string, data: UpdateMileageRequest): Promise<Vehicle> {
    const response = await fetch(`${API_BASE_URL}/vehicles/${vehicleId}/mileage`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return handleResponse<Vehicle>(response) as Promise<Vehicle>;
  },

  async updateStatus(vehicleId: string, data: UpdateStatusRequest): Promise<Vehicle> {
    const response = await fetch(`${API_BASE_URL}/vehicles/${vehicleId}/status`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return handleResponse<Vehicle>(response) as Promise<Vehicle>;
  },

  async deleteVehicle(vehicleId: string): Promise<null> {
    const response = await fetch(`${API_BASE_URL}/vehicles/${vehicleId}`, {
      method: 'DELETE',
    });
    return handleResponse<null>(response);
  },

  async searchVehicleByPlate(plate: string): Promise<Vehicle | Vehicle[]> {
    const response = await fetch(
      `${API_BASE_URL}/vehicles/search?plate=${encodeURIComponent(plate)}`
    );
    return handleResponse<Vehicle | Vehicle[]>(response) as Promise<Vehicle | Vehicle[]>;
  },
};
