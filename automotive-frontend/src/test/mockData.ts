import type { Vehicle } from '../types/vehicle';

export const mockVehicleWithAlerts: Vehicle = {
  id: 'V-123',
  plate: 'ABC-123',
  model: 'Toyota Corolla',
  current_mileage: 35000,
  status: 'active',
  alerts: [
    {
      id: 'alert-3',
      vehicle_id: 'V-123',
      alert_type: 'BASIC',
      mileage: 30000,
      timestamp: '2026-01-20T09:15:00',
    },
    {
      id: 'alert-2',
      vehicle_id: 'V-123',
      alert_type: 'MAJOR',
      mileage: 20000,
      timestamp: '2026-01-15T14:30:00',
    },
    {
      id: 'alert-1',
      vehicle_id: 'V-123',
      alert_type: 'BASIC',
      mileage: 10000,
      timestamp: '2026-01-10T10:00:00',
    },
  ],
};

export const mockVehicleWithoutAlerts: Vehicle = {
  id: 'V-456',
  plate: 'XYZ-456',
  model: 'Honda Civic',
  current_mileage: 5000,
  status: 'active',
  alerts: [],
};

export const mockVehicles: Vehicle[] = [
  mockVehicleWithAlerts,
  mockVehicleWithoutAlerts,
  {
    id: 'V-789',
    plate: 'DEF-789',
    model: 'Mazda 3',
    current_mileage: 15000,
    status: 'in_maintenance',
    alerts: [
      {
        id: 'alert-4',
        vehicle_id: 'V-789',
        alert_type: 'BASIC',
        mileage: 10000,
        timestamp: '2026-01-18T12:00:00',
      },
    ],
  },
];
