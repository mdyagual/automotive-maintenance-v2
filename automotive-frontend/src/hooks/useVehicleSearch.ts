import { useState, useEffect, useCallback } from 'react';
import { vehicleApi } from '../services/api';
import type { Vehicle } from '../types/vehicle';

export const useVehicleSearch = (allVehicles: Vehicle[]) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState<Vehicle[]>(allVehicles);
  const [isSearching, setIsSearching] = useState(false);
  const [searchError, setSearchError] = useState<string | null>(null);

  // Debounce timer
  useEffect(() => {
    // If search term is empty, show all vehicles
    if (!searchTerm || searchTerm.trim() === '') {
      setSearchResults(allVehicles);

      // Show error if only whitespace
      if (searchTerm && searchTerm.trim() === '') {
        setSearchError('La placa de búsqueda no puede estar vacía');
      } else {
        setSearchError(null);
      }
      return;
    }

    // Debounce search
    const timeoutId = setTimeout(async () => {
      setIsSearching(true);
      setSearchError(null);

      try {
        const result = await vehicleApi.searchVehicleByPlate(searchTerm);

        // API can return single vehicle or array
        const resultsArray = Array.isArray(result) ? result : [result];
        setSearchResults(resultsArray);
      } catch (error) {
        // On error, keep showing all vehicles but display error message
        setSearchResults(allVehicles);
        setSearchError(error instanceof Error ? error.message : 'Error al buscar vehículo');
      } finally {
        setIsSearching(false);
      }
    }, 300); // 300ms debounce

    return () => clearTimeout(timeoutId);
  }, [searchTerm, allVehicles]);

  // Update search results when allVehicles changes (e.g., after CRUD operations)
  useEffect(() => {
    if (!searchTerm || searchTerm.trim() === '') {
      setSearchResults(allVehicles);
    }
  }, [allVehicles, searchTerm]);

  const clearSearch = useCallback(() => {
    setSearchTerm('');
    setSearchResults(allVehicles);
    setSearchError(null);
  }, [allVehicles]);

  return {
    searchTerm,
    setSearchTerm,
    searchResults,
    isSearching,
    searchError,
    clearSearch,
  };
};
