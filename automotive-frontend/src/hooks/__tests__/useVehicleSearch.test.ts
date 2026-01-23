import { describe, it, expect, beforeEach, vi } from 'vitest';
import { renderHook, act, waitFor } from '@testing-library/react';
import { useVehicleSearch } from '../useVehicleSearch';
import { vehicleApi } from '../../services/api';
import type { Vehicle } from '../../types/vehicle';

// Mock the API
vi.mock('../../services/api');

describe('useVehicleSearch', () => {
  const mockVehicles: Vehicle[] = [
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
      current_mileage: 10000,
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

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should initialize with empty search term and no results', () => {
    // Act
    const { result } = renderHook(() => useVehicleSearch(mockVehicles));

    // Assert
    expect(result.current.searchTerm).toBe('');
    expect(result.current.searchResults).toEqual(mockVehicles);
    expect(result.current.isSearching).toBe(false);
    expect(result.current.searchError).toBeNull();
  });

  it('should return all vehicles when search term is empty', () => {
    // Arrange
    const { result } = renderHook(() => useVehicleSearch(mockVehicles));

    // Act
    act(() => {
      result.current.setSearchTerm('');
    });

    // Assert
    expect(result.current.searchResults).toEqual(mockVehicles);
    expect(result.current.searchError).toBeNull();
  });

  it('should show error message when search term is only whitespace', () => {
    // Arrange
    const { result } = renderHook(() => useVehicleSearch(mockVehicles));

    // Act
    act(() => {
      result.current.setSearchTerm('   ');
    });

    // Assert
    expect(result.current.searchResults).toEqual(mockVehicles);
    expect(result.current.searchError).toBe('La placa de búsqueda no puede estar vacía');
  });

  it('should search and return single vehicle when exact match found', async () => {
    // Arrange
    const mockSingleVehicle = mockVehicles[0];
    vi.mocked(vehicleApi.searchVehicleByPlate).mockResolvedValueOnce(mockSingleVehicle);

    const { result } = renderHook(() => useVehicleSearch(mockVehicles));

    // Act
    act(() => {
      result.current.setSearchTerm('ABC-123');
    });

    // Assert - Wait for async operation
    await waitFor(() => {
      expect(result.current.searchResults).toEqual([mockSingleVehicle]);
    });

    expect(result.current.searchError).toBeNull();
    expect(vehicleApi.searchVehicleByPlate).toHaveBeenCalledWith('ABC-123');
  });

  it('should search and return multiple vehicles when partial match found', async () => {
    // Arrange
    const mockPartialResults = [mockVehicles[0], mockVehicles[2]];
    vi.mocked(vehicleApi.searchVehicleByPlate).mockResolvedValueOnce(mockPartialResults);

    const { result } = renderHook(() => useVehicleSearch(mockVehicles));

    // Act
    act(() => {
      result.current.setSearchTerm('ABC');
    });

    // Assert - Wait for async operation
    await waitFor(() => {
      expect(result.current.searchResults).toEqual(mockPartialResults);
    });

    expect(result.current.searchError).toBeNull();
    expect(vehicleApi.searchVehicleByPlate).toHaveBeenCalledWith('ABC');
  });

  it('should handle 404 error when no vehicles found', async () => {
    // Arrange
    const errorMessage = "No se encontraron vehículos con placa que contenga 'ZZZ-999'";
    vi.mocked(vehicleApi.searchVehicleByPlate).mockRejectedValueOnce(new Error(errorMessage));

    const { result } = renderHook(() => useVehicleSearch(mockVehicles));

    // Act
    act(() => {
      result.current.setSearchTerm('ZZZ-999');
    });

    // Assert - Wait for async operation
    await waitFor(() => {
      expect(result.current.searchError).toBe(errorMessage);
    });

    expect(result.current.searchResults).toEqual(mockVehicles);
  });

  it('should be case-insensitive when searching', async () => {
    // Arrange
    const mockSingleVehicle = mockVehicles[0];
    vi.mocked(vehicleApi.searchVehicleByPlate).mockResolvedValueOnce(mockSingleVehicle);

    const { result } = renderHook(() => useVehicleSearch(mockVehicles));

    // Act
    act(() => {
      result.current.setSearchTerm('abc-123');
    });

    // Assert - Wait for async operation
    await waitFor(() => {
      expect(result.current.searchResults).toEqual([mockSingleVehicle]);
    });

    expect(vehicleApi.searchVehicleByPlate).toHaveBeenCalledWith('abc-123');
  });

  it('should debounce search requests', async () => {
    // Arrange
    const mockSingleVehicle = mockVehicles[0];
    vi.mocked(vehicleApi.searchVehicleByPlate).mockResolvedValue(mockSingleVehicle);

    const { result } = renderHook(() => useVehicleSearch(mockVehicles));

    // Act - Type quickly (simulating fast typing)
    act(() => {
      result.current.setSearchTerm('A');
    });

    // Wait a bit but not enough to trigger debounce
    await new Promise((resolve) => setTimeout(resolve, 100));

    act(() => {
      result.current.setSearchTerm('AB');
    });

    await new Promise((resolve) => setTimeout(resolve, 100));

    act(() => {
      result.current.setSearchTerm('ABC');
    });

    // Wait for debounce to complete (300ms + buffer)
    await waitFor(
      () => {
        expect(vehicleApi.searchVehicleByPlate).toHaveBeenCalled();
      },
      { timeout: 1000 }
    );

    // Assert - Should only call API once with final value
    expect(vehicleApi.searchVehicleByPlate).toHaveBeenCalledTimes(1);
    expect(vehicleApi.searchVehicleByPlate).toHaveBeenCalledWith('ABC');
  });

  it('should clear search and return all vehicles', () => {
    // Arrange
    const { result } = renderHook(() => useVehicleSearch(mockVehicles));

    act(() => {
      result.current.setSearchTerm('ABC-123');
    });

    // Act
    act(() => {
      result.current.clearSearch();
    });

    // Assert
    expect(result.current.searchTerm).toBe('');
    expect(result.current.searchResults).toEqual(mockVehicles);
    expect(result.current.searchError).toBeNull();
  });

  it('should update search results when vehicles prop changes', () => {
    // Arrange
    const { result, rerender } = renderHook(({ vehicles }) => useVehicleSearch(vehicles), {
      initialProps: { vehicles: mockVehicles },
    });

    // Act - Update vehicles prop
    const newVehicles = [
      ...mockVehicles,
      {
        id: 'V-004',
        plate: 'NEW-001',
        model: 'New Vehicle',
        current_mileage: 0,
        status: 'active' as const,
        alerts: [],
      },
    ];

    rerender({ vehicles: newVehicles });

    // Assert
    expect(result.current.searchResults).toEqual(newVehicles);
  });
});
