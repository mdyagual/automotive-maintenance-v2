/**
 * Tests for UpdateStatusModal Component - HU-005 Escenario 1
 *
 * Tests vehicle status update functionality
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '../../../test/test-utils';
import { UpdateStatusModal } from '../UpdateStatusModal';
import { mockVehicleWithAlerts } from '../../../test/mockData';
import userEvent from '@testing-library/user-event';
import type { Vehicle } from '../../../types/vehicle';

describe('UpdateStatusModal - HU-005 Escenario 1', () => {
  it('should display modal title', () => {
    render(
      <UpdateStatusModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={async () => {}}
      />
    );

    expect(screen.getByText('Actualizar Estado del Vehículo')).toBeInTheDocument();
  });

  it('should display vehicle information', () => {
    render(
      <UpdateStatusModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={async () => {}}
      />
    );

    expect(screen.getByText(/ABC-123 - Toyota Corolla/)).toBeInTheDocument();
    expect(screen.getByText(/Estado actual:/)).toBeInTheDocument();
    expect(screen.getByText(/Activo/)).toBeInTheDocument();
  });

  it('should display all status options in select', () => {
    render(
      <UpdateStatusModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={async () => {}}
      />
    );

    const select = screen.getByRole('combobox');
    const options = Array.from(select.querySelectorAll('option'));

    expect(options).toHaveLength(4);
    expect(options.map((o) => o.textContent)).toEqual([
      'Activo',
      'Inactivo',
      'En Mantenimiento',
      'Retirado',
    ]);
  });

  it('should display status descriptions', () => {
    render(
      <UpdateStatusModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={async () => {}}
      />
    );

    expect(screen.getByText(/Vehículo disponible para operaciones normales/)).toBeInTheDocument();
    expect(screen.getByText(/Vehículo temporalmente fuera de servicio/)).toBeInTheDocument();
    expect(screen.getByText(/Vehículo en proceso de mantenimiento/)).toBeInTheDocument();
    expect(screen.getByText(/permanentemente fuera de servicio/)).toBeInTheDocument();
  });

  it('should have Cancelar and Actualizar Estado buttons', () => {
    render(
      <UpdateStatusModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={async () => {}}
      />
    );

    expect(screen.getByRole('button', { name: /Cancelar/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Actualizar Estado/i })).toBeInTheDocument();
  });

  it('should call onClose when Cancelar button is clicked', async () => {
    const user = userEvent.setup();
    const mockOnClose = vi.fn();

    render(
      <UpdateStatusModal
        isOpen={true}
        onClose={mockOnClose}
        vehicle={mockVehicleWithAlerts}
        onSubmit={async () => {}}
      />
    );

    await user.click(screen.getByRole('button', { name: /Cancelar/i }));
    expect(mockOnClose).toHaveBeenCalled();
  });

  it('should submit form with selected status - HU-005 Escenario 1', async () => {
    const user = userEvent.setup();
    const mockOnSubmit = vi.fn().mockResolvedValue(undefined);
    const mockOnClose = vi.fn();

    render(
      <UpdateStatusModal
        isOpen={true}
        onClose={mockOnClose}
        vehicle={mockVehicleWithAlerts}
        onSubmit={mockOnSubmit}
      />
    );

    const select = screen.getByRole('combobox');
    await user.selectOptions(select, 'in_maintenance');
    await user.click(screen.getByRole('button', { name: /Actualizar Estado/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith('V-123', 'in_maintenance');
      expect(mockOnClose).toHaveBeenCalled();
    });
  });

  it('should close modal without submitting if status unchanged', async () => {
    const user = userEvent.setup();
    const mockOnSubmit = vi.fn();
    const mockOnClose = vi.fn();

    render(
      <UpdateStatusModal
        isOpen={true}
        onClose={mockOnClose}
        vehicle={mockVehicleWithAlerts}
        onSubmit={mockOnSubmit}
      />
    );

    // Don't change status (it's already 'active')
    await user.click(screen.getByRole('button', { name: /Actualizar Estado/i }));

    await waitFor(() => {
      expect(mockOnSubmit).not.toHaveBeenCalled();
      expect(mockOnClose).toHaveBeenCalled();
    });
  });

  it('should allow changing to inactive status', async () => {
    const user = userEvent.setup();
    const mockOnSubmit = vi.fn().mockResolvedValue(undefined);

    render(
      <UpdateStatusModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={mockOnSubmit}
      />
    );

    const select = screen.getByRole('combobox');
    await user.selectOptions(select, 'inactive');
    await user.click(screen.getByRole('button', { name: /Actualizar Estado/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith('V-123', 'inactive');
    });
  });

  it('should allow changing to retired status', async () => {
    const user = userEvent.setup();
    const mockOnSubmit = vi.fn().mockResolvedValue(undefined);

    render(
      <UpdateStatusModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={mockOnSubmit}
      />
    );

    const select = screen.getByRole('combobox');
    await user.selectOptions(select, 'retired');
    await user.click(screen.getByRole('button', { name: /Actualizar Estado/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith('V-123', 'retired');
    });
  });

  it('should disable buttons while submitting', async () => {
    const user = userEvent.setup();
    const mockOnSubmit = vi
      .fn()
      .mockImplementation(() => new Promise((resolve) => setTimeout(resolve, 100)));

    render(
      <UpdateStatusModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={mockOnSubmit}
      />
    );

    const select = screen.getByRole('combobox');
    await user.selectOptions(select, 'inactive');

    const submitButton = screen.getByRole('button', { name: /Actualizar Estado/i });
    await user.click(submitButton);

    // Buttons should be disabled during submission
    expect(submitButton).toBeDisabled();
    expect(screen.getByRole('button', { name: /Cancelar/i })).toBeDisabled();
    expect(submitButton).toHaveTextContent('Actualizando...');
  });

  it('should display current status for in_maintenance vehicle', () => {
    const maintenanceVehicle: Vehicle = {
      ...mockVehicleWithAlerts,
      status: 'in_maintenance',
    };

    render(
      <UpdateStatusModal
        isOpen={true}
        onClose={() => {}}
        vehicle={maintenanceVehicle}
        onSubmit={async () => {}}
      />
    );

    expect(screen.getByText(/En Mantenimiento/)).toBeInTheDocument();
  });

  it('should not render when modal is closed', () => {
    const { container } = render(
      <UpdateStatusModal
        isOpen={false}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={async () => {}}
      />
    );

    expect(container.firstChild).toBeNull();
  });

  it('should not render when vehicle is null', () => {
    const { container } = render(
      <UpdateStatusModal
        isOpen={true}
        onClose={() => {}}
        vehicle={null}
        onSubmit={async () => {}}
      />
    );

    expect(container.firstChild).toBeNull();
  });

  it('should have required attribute on select field', () => {
    render(
      <UpdateStatusModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={async () => {}}
      />
    );

    expect(screen.getByRole('combobox')).toBeRequired();
  });
});
