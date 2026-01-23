import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { vehicleApi } from '../api';
import type { VehicleStatus } from '../../types/vehicle';

describe('vehicleApi', () => {
  const mockFetch = vi.fn();

  beforeEach(() => {
    // Mock fetch globally
    vi.stubGlobal('fetch', mockFetch);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  describe('getVehiclesByStatus', () => {
    it('should call the correct endpoint with status query parameter', async () => {
      // Arrange
      const mockVehicles = [
        {
          id: 'V-001',
          plate: 'ABC-123',
          model: 'Toyota Corolla',
          current_mileage: 5000,
          status: 'active',
          alerts: [],
        },
        {
          id: 'V-002',
          plate: 'XYZ-456',
          model: 'Honda Civic',
          current_mileage: 8000,
          status: 'active',
          alerts: [],
        },
      ];

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockVehicles,
      });

      // Act
      const status: VehicleStatus = 'active';
      await vehicleApi.getVehiclesByStatus(status);

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('http://127.0.0.1:8000/vehicles?status=active');
    });

    it('should return filtered vehicles for "in_maintenance" status', async () => {
      // Arrange
      const mockVehicles = [
        {
          id: 'V-003',
          plate: 'DEF-789',
          model: 'Ford Focus',
          current_mileage: 15000,
          status: 'in_maintenance',
          alerts: [],
        },
      ];

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockVehicles,
      });

      // Act
      const status: VehicleStatus = 'in_maintenance';
      const result = await vehicleApi.getVehiclesByStatus(status);

      // Assert
      expect(result).toEqual(mockVehicles);
      expect(mockFetch).toHaveBeenCalledWith(
        'http://127.0.0.1:8000/vehicles?status=in_maintenance'
      );
    });

    it('should return filtered vehicles for "inactive" status', async () => {
      // Arrange
      const mockVehicles = [
        {
          id: 'V-004',
          plate: 'GHI-012',
          model: 'Mazda 3',
          current_mileage: 20000,
          status: 'inactive',
          alerts: [],
        },
      ];

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockVehicles,
      });

      // Act
      const status: VehicleStatus = 'inactive';
      const result = await vehicleApi.getVehiclesByStatus(status);

      // Assert
      expect(result).toEqual(mockVehicles);
      expect(mockFetch).toHaveBeenCalledWith('http://127.0.0.1:8000/vehicles?status=inactive');
    });

    it('should return filtered vehicles for "retired" status', async () => {
      // Arrange
      const mockVehicles = [
        {
          id: 'V-005',
          plate: 'JKL-345',
          model: 'Nissan Sentra',
          current_mileage: 250000,
          status: 'retired',
          alerts: [],
        },
      ];

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockVehicles,
      });

      // Act
      const status: VehicleStatus = 'retired';
      const result = await vehicleApi.getVehiclesByStatus(status);

      // Assert
      expect(result).toEqual(mockVehicles);
      expect(mockFetch).toHaveBeenCalledWith('http://127.0.0.1:8000/vehicles?status=retired');
    });

    it('should return empty array when no vehicles match the status', async () => {
      // Arrange
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => [],
      });

      // Act
      const status: VehicleStatus = 'retired';
      const result = await vehicleApi.getVehiclesByStatus(status);

      // Assert
      expect(result).toEqual([]);
    });

    it('should throw error when API returns 400 for invalid status', async () => {
      // Arrange
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
        statusText: 'Bad Request',
        json: async () => ({
          detail:
            "Estado inválido 'broken'. Estados válidos: active, inactive, in_maintenance, retired",
        }),
      });

      // Act & Assert
      await expect(vehicleApi.getVehiclesByStatus('broken' as VehicleStatus)).rejects.toThrow(
        "Estado inválido 'broken'"
      );
    });

    it('should throw error when API returns 500', async () => {
      // Arrange
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        json: async () => ({}),
      });

      // Act & Assert
      await expect(vehicleApi.getVehiclesByStatus('active')).rejects.toThrow(
        'Error 500: Internal Server Error'
      );
    });
  });

  describe('getAllVehicles', () => {
    it('should call the endpoint without status parameter', async () => {
      // Arrange
      const mockVehicles = [
        {
          id: 'V-001',
          plate: 'ABC-123',
          model: 'Toyota Corolla',
          current_mileage: 5000,
          status: 'active',
          alerts: [],
        },
      ];

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockVehicles,
      });

      // Act
      await vehicleApi.getAllVehicles();

      // Assert
      expect(mockFetch).toHaveBeenCalledWith('http://127.0.0.1:8000/vehicles');
    });
  });

  describe('searchVehicleByPlate', () => {
    it('should return a single vehicle when exact plate match is found', async () => {
      // Arrange
      const mockVehicle = {
        id: 'V-001',
        plate: 'ABC-123',
        model: 'Toyota Corolla',
        current_mileage: 5000,
        status: 'active',
        alerts: [],
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockVehicle,
      });

      // Act
      const result = await vehicleApi.searchVehicleByPlate('ABC-123');

      // Assert
      expect(result).toEqual(mockVehicle);
      expect(mockFetch).toHaveBeenCalledWith('http://127.0.0.1:8000/vehicles/search?plate=ABC-123');
    });

    it('should return multiple vehicles when partial plate match is found', async () => {
      // Arrange
      const mockVehicles = [
        {
          id: 'V-001',
          plate: 'ABC-123',
          model: 'Toyota Corolla',
          current_mileage: 5000,
          status: 'active',
          alerts: [],
        },
        {
          id: 'V-003',
          plate: 'ABC-789',
          model: 'Mazda 3',
          current_mileage: 15000,
          status: 'active',
          alerts: [],
        },
      ];

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockVehicles,
      });

      // Act
      const result = await vehicleApi.searchVehicleByPlate('ABC');

      // Assert
      expect(result).toEqual(mockVehicles);
      expect(mockFetch).toHaveBeenCalledWith('http://127.0.0.1:8000/vehicles/search?plate=ABC');
    });

    it('should be case-insensitive when searching', async () => {
      // Arrange
      const mockVehicle = {
        id: 'V-001',
        plate: 'ABC-123',
        model: 'Toyota Corolla',
        current_mileage: 5000,
        status: 'active',
        alerts: [],
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockVehicle,
      });

      // Act
      const result = await vehicleApi.searchVehicleByPlate('abc-123');

      // Assert
      expect(result).toEqual(mockVehicle);
      expect(mockFetch).toHaveBeenCalledWith('http://127.0.0.1:8000/vehicles/search?plate=abc-123');
    });

    it('should throw error when no vehicles found (404)', async () => {
      // Arrange
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
        statusText: 'Not Found',
        json: async () => ({
          detail: "No se encontraron vehículos con placa que contenga 'ZZZ-999'",
        }),
      });

      // Act & Assert
      await expect(vehicleApi.searchVehicleByPlate('ZZZ-999')).rejects.toThrow(
        "No se encontraron vehículos con placa que contenga 'ZZZ-999'"
      );
    });

    it('should throw error when searching with empty plate', async () => {
      // Arrange
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
        statusText: 'Not Found',
        json: async () => ({
          detail: 'La placa de búsqueda no puede estar vacía',
        }),
      });

      // Act & Assert
      await expect(vehicleApi.searchVehicleByPlate('')).rejects.toThrow(
        'La placa de búsqueda no puede estar vacía'
      );
    });

    it('should encode special characters in plate search', async () => {
      // Arrange
      const mockVehicle = {
        id: 'V-001',
        plate: 'ABC-123',
        model: 'Toyota Corolla',
        current_mileage: 5000,
        status: 'active',
        alerts: [],
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockVehicle,
      });

      // Act
      await vehicleApi.searchVehicleByPlate('ABC 123');

      // Assert
      expect(mockFetch).toHaveBeenCalledWith(
        'http://127.0.0.1:8000/vehicles/search?plate=ABC%20123'
      );
    });
  });
});
