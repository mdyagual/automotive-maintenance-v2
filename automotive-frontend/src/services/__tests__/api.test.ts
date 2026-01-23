import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { vehicleApi } from '../api';
import type { VehicleStatus } from '../../types/vehicle';

describe('vehicleApi', () => {
  beforeEach(() => {
    // Mock fetch globally
    global.fetch = vi.fn();
  });

  afterEach(() => {
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

      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockVehicles,
      });

      // Act
      const status: VehicleStatus = 'active';
      await vehicleApi.getVehiclesByStatus(status);

      // Assert
      expect(global.fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/vehicles?status=active');
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

      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockVehicles,
      });

      // Act
      const status: VehicleStatus = 'in_maintenance';
      const result = await vehicleApi.getVehiclesByStatus(status);

      // Assert
      expect(result).toEqual(mockVehicles);
      expect(global.fetch).toHaveBeenCalledWith(
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

      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockVehicles,
      });

      // Act
      const status: VehicleStatus = 'inactive';
      const result = await vehicleApi.getVehiclesByStatus(status);

      // Assert
      expect(result).toEqual(mockVehicles);
      expect(global.fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/vehicles?status=inactive');
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

      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockVehicles,
      });

      // Act
      const status: VehicleStatus = 'retired';
      const result = await vehicleApi.getVehiclesByStatus(status);

      // Assert
      expect(result).toEqual(mockVehicles);
      expect(global.fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/vehicles?status=retired');
    });

    it('should return empty array when no vehicles match the status', async () => {
      // Arrange
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
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
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: false,
        status: 400,
        statusText: 'Bad Request',
        json: async () => ({
          detail: "Estado inválido 'broken'. Estados válidos: active, inactive, in_maintenance, retired",
        }),
      });

      // Act & Assert
      await expect(vehicleApi.getVehiclesByStatus('broken' as VehicleStatus)).rejects.toThrow(
        "Estado inválido 'broken'"
      );
    });

    it('should throw error when API returns 500', async () => {
      // Arrange
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
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

      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockVehicles,
      });

      // Act
      await vehicleApi.getAllVehicles();

      // Assert
      expect(global.fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/vehicles');
    });
  });
});
