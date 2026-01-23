/**
 * Tests for HU-003 Escenario 6: Vehicle details with alerts visualization
 * 
 * Given existe un vehículo 'V-123' con 3 alertas de mantenimiento
 * When el usuario hace clic en el botón "Detalles" del vehículo
 * Then el sistema debe mostrar un modal con la información del vehículo
 * And el modal debe incluir una sección de "Alertas de Mantenimiento"
 * And debe mostrar las 3 alertas ordenadas cronológicamente (más reciente primero)
 * And cada alerta debe mostrar: tipo, mensaje, kilometraje y fecha de generación
 */

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { DetailsModal } from '../DetailsModal';
import type { Vehicle } from '../../../types/vehicle';

describe('DetailsModal - HU-003 Escenario 6', () => {
  const mockVehicleWithAlerts: Vehicle = {
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

  const mockVehicleWithoutAlerts: Vehicle = {
    id: 'V-456',
    plate: 'XYZ-456',
    model: 'Honda Civic',
    current_mileage: 5000,
    status: 'active',
    alerts: [],
  };

  it('should display vehicle information in modal', () => {
    // Given: A vehicle with alerts exists
    // When: The modal is opened
    render(
      <DetailsModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
      />
    );

    // Then: Should show vehicle information
    expect(screen.getByText('Detalles del Vehículo')).toBeInTheDocument();
    expect(screen.getByText('V-123')).toBeInTheDocument();
    expect(screen.getByText('ABC-123')).toBeInTheDocument();
    expect(screen.getByText('Toyota Corolla')).toBeInTheDocument();
    expect(screen.getByText(/35,000/)).toBeInTheDocument();
  });

  it('should include maintenance alerts section', () => {
    // Given: A vehicle 'V-123' with 3 maintenance alerts
    // When: The details modal is displayed
    render(
      <DetailsModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
      />
    );

    // Then: Should include a "Maintenance Alerts" section
    expect(screen.getByText(/Alertas de Mantenimiento/i)).toBeInTheDocument();
  });

  it('should display 3 alerts ordered chronologically (most recent first)', () => {
    // Given: A vehicle with 3 alerts
    // When: The modal is displayed
    render(
      <DetailsModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
      />
    );

    // Then: Should show 3 alerts
    const alertElements = screen.getAllByTestId(/alert-item/);
    expect(alertElements).toHaveLength(3);

    // And: Alerts should be ordered chronologically (most recent first)
    // Most recent: alert-3 (2026-01-20)
    expect(alertElements[0]).toHaveTextContent('30,000');
    expect(alertElements[0]).toHaveTextContent('20/01/2026');

    // Middle: alert-2 (2026-01-15)
    expect(alertElements[1]).toHaveTextContent('20,000');
    expect(alertElements[1]).toHaveTextContent('15/01/2026');

    // Oldest: alert-1 (2026-01-10)
    expect(alertElements[2]).toHaveTextContent('10,000');
    expect(alertElements[2]).toHaveTextContent('10/01/2026');
  });

  it('should display alert type, mileage, and timestamp for each alert', () => {
    // Given: A vehicle with alerts
    // When: The modal is displayed
    render(
      <DetailsModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
      />
    );

    // Then: Each alert should show type, mileage, and timestamp
    const alerts = screen.getAllByTestId(/alert-item/);

    // First alert (most recent)
    expect(alerts[0]).toHaveTextContent(/Básico|BASIC/i);
    expect(alerts[0]).toHaveTextContent('30,000');
    expect(alerts[0]).toHaveTextContent('20/01/2026');

    // Second alert
    expect(alerts[1]).toHaveTextContent(/Mayor|MAJOR/i);
    expect(alerts[1]).toHaveTextContent('20,000');
    expect(alerts[1]).toHaveTextContent('15/01/2026');

    // Third alert
    expect(alerts[2]).toHaveTextContent(/Básico|BASIC/i);
    expect(alerts[2]).toHaveTextContent('10,000');
    expect(alerts[2]).toHaveTextContent('10/01/2026');
  });

  it('should display empty state when vehicle has no alerts', () => {
    // Given: A vehicle without alerts
    // When: The modal is displayed
    render(
      <DetailsModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithoutAlerts}
      />
    );

    // Then: Should show empty state message
    expect(screen.getByText(/No hay alertas registradas/i)).toBeInTheDocument();
  });

  it('should not render when modal is closed', () => {
    // Given: Modal is closed
    // When: isOpen is false
    const { container } = render(
      <DetailsModal
        isOpen={false}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
      />
    );

    // Then: Should not render anything
    expect(container.firstChild).toBeNull();
  });

  it('should not render when vehicle is null', () => {
    // Given: No vehicle selected
    // When: vehicle is null
    const { container } = render(
      <DetailsModal
        isOpen={true}
        onClose={() => {}}
        vehicle={null}
      />
    );

    // Then: Should not render anything
    expect(container.firstChild).toBeNull();
  });
});
