/**
 * Tests for VehicleCard Component
 *
 * Tests vehicle card display, status badges, action buttons, and retired vehicle restrictions
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '../../test/test-utils';
import { VehicleCard } from '../VehicleCard';
import { mockVehicleWithAlerts, mockVehicleWithoutAlerts } from '../../test/mockData';
import type { Vehicle } from '../../types/vehicle';
import userEvent from '@testing-library/user-event';

describe('VehicleCard', () => {
  const mockHandlers = {
    onUpdate: vi.fn(),
    onDetails: vi.fn(),
    onDelete: vi.fn(),
    onAlerts: vi.fn(),
    onUpdateStatus: vi.fn(),
  };

  it('should display vehicle information correctly', () => {
    render(<VehicleCard vehicle={mockVehicleWithAlerts} {...mockHandlers} />);

    expect(screen.getByText('ID: V-123')).toBeInTheDocument();
    expect(screen.getByText('ABC-123')).toBeInTheDocument();
    expect(screen.getByText('Toyota Corolla')).toBeInTheDocument();
    expect(screen.getByText('35,000')).toBeInTheDocument();
  });

  it('should display status badge with correct text', () => {
    render(<VehicleCard vehicle={mockVehicleWithAlerts} {...mockHandlers} />);

    expect(screen.getByText('Activo')).toBeInTheDocument();
  });

  it('should apply has-alert class when vehicle has alerts', () => {
    const { container } = render(<VehicleCard vehicle={mockVehicleWithAlerts} {...mockHandlers} />);

    const card = container.querySelector('.vehicle-card');
    expect(card).toHaveClass('has-alert');
  });

  it('should not apply has-alert class when vehicle has no alerts', () => {
    const { container } = render(
      <VehicleCard vehicle={mockVehicleWithoutAlerts} {...mockHandlers} />
    );

    const card = container.querySelector('.vehicle-card');
    expect(card).not.toHaveClass('has-alert');
  });

  it('should call onDetails when Detalles button is clicked', async () => {
    const user = userEvent.setup();
    render(<VehicleCard vehicle={mockVehicleWithAlerts} {...mockHandlers} />);

    const detailsButton = screen.getByRole('button', { name: /Detalles/i });
    await user.click(detailsButton);

    expect(mockHandlers.onDetails).toHaveBeenCalledWith('V-123');
  });

  it('should call onDelete when Eliminar button is clicked', async () => {
    const user = userEvent.setup();
    render(<VehicleCard vehicle={mockVehicleWithAlerts} {...mockHandlers} />);

    const deleteButton = screen.getByRole('button', { name: /Eliminar/i });
    await user.click(deleteButton);

    expect(mockHandlers.onDelete).toHaveBeenCalledWith('V-123');
  });

  it('should call onUpdate when Actualizar KM button is clicked', async () => {
    const user = userEvent.setup();
    render(<VehicleCard vehicle={mockVehicleWithAlerts} {...mockHandlers} />);

    const updateButton = screen.getByRole('button', { name: /Actualizar KM/i });
    await user.click(updateButton);

    expect(mockHandlers.onUpdate).toHaveBeenCalledWith('V-123');
  });

  it('should call onUpdateStatus when status badge is clicked', async () => {
    const user = userEvent.setup();
    render(<VehicleCard vehicle={mockVehicleWithAlerts} {...mockHandlers} />);

    const statusBadge = screen.getByText('Activo');
    await user.click(statusBadge);

    expect(mockHandlers.onUpdateStatus).toHaveBeenCalledWith('V-123');
  });

  it('should disable Actualizar KM button for retired vehicles - HU-005 Escenario 5', () => {
    const retiredVehicle: Vehicle = {
      ...mockVehicleWithAlerts,
      status: 'retired',
    };

    render(<VehicleCard vehicle={retiredVehicle} {...mockHandlers} />);

    const updateButton = screen.getByRole('button', { name: /Actualizar KM/i });
    expect(updateButton).toBeDisabled();
    expect(updateButton).toHaveAttribute(
      'title',
      'No se puede actualizar kilometraje de vehículos retirados'
    );
  });

  it('should enable Actualizar KM button for active vehicles', () => {
    render(<VehicleCard vehicle={mockVehicleWithAlerts} {...mockHandlers} />);

    const updateButton = screen.getByRole('button', { name: /Actualizar KM/i });
    expect(updateButton).not.toBeDisabled();
  });

  it('should display correct status badge for in_maintenance status', () => {
    const maintenanceVehicle: Vehicle = {
      ...mockVehicleWithAlerts,
      status: 'in_maintenance',
    };

    render(<VehicleCard vehicle={maintenanceVehicle} {...mockHandlers} />);

    expect(screen.getByText('En Mantenimiento')).toBeInTheDocument();
  });

  it('should display correct status badge for inactive status', () => {
    const inactiveVehicle: Vehicle = {
      ...mockVehicleWithAlerts,
      status: 'inactive',
    };

    render(<VehicleCard vehicle={inactiveVehicle} {...mockHandlers} />);

    expect(screen.getByText('Inactivo')).toBeInTheDocument();
  });

  it('should display correct status badge for retired status', () => {
    const retiredVehicle: Vehicle = {
      ...mockVehicleWithAlerts,
      status: 'retired',
    };

    render(<VehicleCard vehicle={retiredVehicle} {...mockHandlers} />);

    expect(screen.getByText('Retirado')).toBeInTheDocument();
  });
});
