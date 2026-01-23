/**
 * Tests for VehicleGrid Component
 *
 * Tests vehicle grid display, empty state, and vehicle card rendering
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '../../test/test-utils';
import { VehicleGrid } from '../VehicleGrid';
import { mockVehicles } from '../../test/mockData';
import userEvent from '@testing-library/user-event';

describe('VehicleGrid', () => {
  const mockHandlers = {
    onUpdate: vi.fn(),
    onDetails: vi.fn(),
    onDelete: vi.fn(),
    onUpdateStatus: vi.fn(),
    onNewVehicle: vi.fn(),
  };

  it('should render all vehicles in grid', () => {
    render(<VehicleGrid vehicles={mockVehicles} {...mockHandlers} />);

    expect(screen.getByText('ABC-123')).toBeInTheDocument();
    expect(screen.getByText('XYZ-456')).toBeInTheDocument();
    expect(screen.getByText('DEF-789')).toBeInTheDocument();
  });

  it('should display empty state when no vehicles exist', () => {
    render(<VehicleGrid vehicles={[]} {...mockHandlers} />);

    expect(screen.getByText('No hay vehículos registrados')).toBeInTheDocument();
    expect(screen.getByText('Comienza registrando tu primer vehículo')).toBeInTheDocument();
  });

  it('should show Registrar Vehículo button in empty state', () => {
    render(<VehicleGrid vehicles={[]} {...mockHandlers} />);

    const registerButton = screen.getByRole('button', { name: /Registrar Vehículo/i });
    expect(registerButton).toBeInTheDocument();
  });

  it('should call onNewVehicle when Registrar Vehículo button is clicked', async () => {
    const user = userEvent.setup();
    render(<VehicleGrid vehicles={[]} {...mockHandlers} />);

    const registerButton = screen.getByRole('button', { name: /Registrar Vehículo/i });
    await user.click(registerButton);

    expect(mockHandlers.onNewVehicle).toHaveBeenCalled();
  });

  it('should render correct number of vehicle cards', () => {
    const { container } = render(<VehicleGrid vehicles={mockVehicles} {...mockHandlers} />);

    const vehicleCards = container.querySelectorAll('.vehicle-card');
    expect(vehicleCards).toHaveLength(3);
  });

  it('should pass correct props to VehicleCard components', () => {
    render(<VehicleGrid vehicles={mockVehicles} {...mockHandlers} />);

    // Verify first vehicle data is rendered
    expect(screen.getByText('ID: V-123')).toBeInTheDocument();
    expect(screen.getByText('Toyota Corolla')).toBeInTheDocument();

    // Verify second vehicle data is rendered
    expect(screen.getByText('ID: V-456')).toBeInTheDocument();
    expect(screen.getByText('Honda Civic')).toBeInTheDocument();

    // Verify third vehicle data is rendered
    expect(screen.getByText('ID: V-789')).toBeInTheDocument();
    expect(screen.getByText('Mazda 3')).toBeInTheDocument();
  });

  it('should not render empty state when vehicles exist', () => {
    render(<VehicleGrid vehicles={mockVehicles} {...mockHandlers} />);

    expect(screen.queryByText('No hay vehículos registrados')).not.toBeInTheDocument();
  });
});
