/**
 * Tests for Stats Component - HU-005
 * 
 * Tests statistics display including total fleet, active vehicles, in maintenance, and alerts
 */

import { describe, it, expect } from 'vitest';
import { render, screen } from '../../test/test-utils';
import { Stats } from '../Stats';
import { mockVehicles } from '../../test/mockData';
import type { Vehicle } from '../../types/vehicle';

describe('Stats - HU-005', () => {
  it('should display total fleet count', () => {
    render(<Stats vehicles={mockVehicles} />);

    expect(screen.getByText('Total Flota')).toBeInTheDocument();
    expect(screen.getByText('3')).toBeInTheDocument();
  });

  it('should display active vehicles count', () => {
    render(<Stats vehicles={mockVehicles} />);

    expect(screen.getByText('En Ruta')).toBeInTheDocument();
    // mockVehicles has 2 active vehicles (V-123 and V-456)
    const statValues = screen.getAllByText('2');
    expect(statValues.length).toBeGreaterThan(0);
  });

  it('should display in maintenance vehicles count', () => {
    render(<Stats vehicles={mockVehicles} />);

    expect(screen.getByText('En Taller')).toBeInTheDocument();
    // mockVehicles has 1 in_maintenance vehicle (V-789)
    const statValues = screen.getAllByText('1');
    expect(statValues.length).toBeGreaterThan(0);
  });

  it('should display total alerts count', () => {
    render(<Stats vehicles={mockVehicles} />);

    expect(screen.getByText('Alertas')).toBeInTheDocument();
    // mockVehicles has 4 total alerts (3 + 0 + 1)
    expect(screen.getByText('4')).toBeInTheDocument();
  });

  it('should show zero for all stats when no vehicles exist', () => {
    render(<Stats vehicles={[]} />);

    expect(screen.getByText('Total Flota')).toBeInTheDocument();
    const zeroValues = screen.getAllByText('0');
    expect(zeroValues.length).toBe(4); // All 4 stats should be 0
  });

  it('should correctly count vehicles by status', () => {
    const testVehicles: Vehicle[] = [
      { id: 'V-001', plate: 'AAA-001', model: 'Car 1', current_mileage: 1000, status: 'active', alerts: [] },
      { id: 'V-002', plate: 'AAA-002', model: 'Car 2', current_mileage: 2000, status: 'active', alerts: [] },
      { id: 'V-003', plate: 'AAA-003', model: 'Car 3', current_mileage: 3000, status: 'in_maintenance', alerts: [] },
      { id: 'V-004', plate: 'AAA-004', model: 'Car 4', current_mileage: 4000, status: 'in_maintenance', alerts: [] },
      { id: 'V-005', plate: 'AAA-005', model: 'Car 5', current_mileage: 5000, status: 'inactive', alerts: [] },
      { id: 'V-006', plate: 'AAA-006', model: 'Car 6', current_mileage: 6000, status: 'retired', alerts: [] },
    ];

    render(<Stats vehicles={testVehicles} />);

    // Total fleet: 6
    expect(screen.getByText('6')).toBeInTheDocument();
    
    // Active (En Ruta): 2
    const twoValues = screen.getAllByText('2');
    expect(twoValues.length).toBeGreaterThan(0);
  });

  it('should correctly sum all alerts across vehicles', () => {
    const vehiclesWithAlerts: Vehicle[] = [
      {
        id: 'V-001',
        plate: 'AAA-001',
        model: 'Car 1',
        current_mileage: 10000,
        status: 'active',
        alerts: [
          { id: 'a1', vehicle_id: 'V-001', alert_type: 'BASIC', mileage: 10000, timestamp: '2026-01-01T00:00:00' },
          { id: 'a2', vehicle_id: 'V-001', alert_type: 'BASIC', mileage: 20000, timestamp: '2026-01-02T00:00:00' },
        ],
      },
      {
        id: 'V-002',
        plate: 'AAA-002',
        model: 'Car 2',
        current_mileage: 30000,
        status: 'active',
        alerts: [
          { id: 'a3', vehicle_id: 'V-002', alert_type: 'MAJOR', mileage: 30000, timestamp: '2026-01-03T00:00:00' },
        ],
      },
    ];

    render(<Stats vehicles={vehiclesWithAlerts} />);

    // Total alerts: 3
    expect(screen.getByText('3')).toBeInTheDocument();
  });

  it('should handle vehicles with undefined alerts array', () => {
    const vehiclesWithUndefinedAlerts: Vehicle[] = [
      {
        id: 'V-001',
        plate: 'AAA-001',
        model: 'Car 1',
        current_mileage: 1000,
        status: 'active',
        alerts: undefined as any,
      },
    ];

    render(<Stats vehicles={vehiclesWithUndefinedAlerts} />);

    // Should not crash and show 0 alerts
    expect(screen.getByText('Alertas')).toBeInTheDocument();
    const zeroValues = screen.getAllByText('0');
    expect(zeroValues.length).toBeGreaterThan(0);
  });
});
