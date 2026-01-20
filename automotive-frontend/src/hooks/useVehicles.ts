import { useState, useEffect, useCallback } from 'react';
import { vehicleApi } from '../services/api';
import type { Vehicle, CreateVehicleRequest, UpdateMileageRequest } from '../types/vehicle';

export const useVehicles = () => {
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadVehicles = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await vehicleApi.getAllVehicles();
      setVehicles(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al cargar vehículos');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadVehicles();
  }, [loadVehicles]);

  const createVehicle = async (vehicleData: CreateVehicleRequest) => {
    await vehicleApi.createVehicle(vehicleData);
    await loadVehicles();
  };

  const updateMileage = async (vehicleId: string, data: UpdateMileageRequest) => {
    await vehicleApi.updateMileage(vehicleId, data);
    await loadVehicles();
  };

  const deleteVehicle = async (vehicleId: string) => {
    await vehicleApi.deleteVehicle(vehicleId);
    await loadVehicles();
  };

  return {
    vehicles,
    loading,
    error,
    loadVehicles,
    createVehicle,
    updateMileage,
    deleteVehicle,
  };
};
