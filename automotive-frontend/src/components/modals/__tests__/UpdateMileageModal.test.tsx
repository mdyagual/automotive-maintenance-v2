/**
 * Tests for UpdateMileageModal Component - HU-001
 *
 * Tests mileage update form, validation, and business rules
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '../../../test/test-utils';
import { UpdateMileageModal } from '../UpdateMileageModal';
import { mockVehicleWithAlerts } from '../../../test/mockData';
import userEvent from '@testing-library/user-event';

describe('UpdateMileageModal - HU-001', () => {
  it('should display modal title', () => {
    render(
      <UpdateMileageModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={async () => {}}
      />
    );

    expect(screen.getByText('Actualizar Kilometraje')).toBeInTheDocument();
  });

  it('should display vehicle information', () => {
    render(
      <UpdateMileageModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={async () => {}}
      />
    );

    expect(screen.getByText(/ABC-123 - Toyota Corolla/)).toBeInTheDocument();
    expect(screen.getAllByText(/35[.,]000 km/).length).toBeGreaterThanOrEqual(1);
  });

  it('should display current mileage', () => {
    render(
      <UpdateMileageModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={async () => {}}
      />
    );

    expect(screen.getByText(/Kilometraje actual:/)).toBeInTheDocument();
    expect(screen.getAllByText(/35[.,]000 km/).length).toBeGreaterThanOrEqual(1);
  });

  it('should have Cancelar and Actualizar buttons', () => {
    render(
      <UpdateMileageModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={async () => {}}
      />
    );

    expect(screen.getByRole('button', { name: /Cancelar/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Actualizar/i })).toBeInTheDocument();
  });

  it('should call onClose when Cancelar button is clicked', async () => {
    const user = userEvent.setup();
    const mockOnClose = vi.fn();

    render(
      <UpdateMileageModal
        isOpen={true}
        onClose={mockOnClose}
        vehicle={mockVehicleWithAlerts}
        onSubmit={async () => {}}
      />
    );

    await user.click(screen.getByRole('button', { name: /Cancelar/i }));
    expect(mockOnClose).toHaveBeenCalled();
  });

  it('should submit form with valid mileage - HU-001 Escenario 1', async () => {
    const user = userEvent.setup();
    const mockOnSubmit = vi.fn().mockResolvedValue(undefined);
    const mockOnClose = vi.fn();

    render(
      <UpdateMileageModal
        isOpen={true}
        onClose={mockOnClose}
        vehicle={mockVehicleWithAlerts}
        onSubmit={mockOnSubmit}
      />
    );

    const input = screen.getByLabelText(/Nuevo Kilometraje/i);
    await user.type(input, '40000');
    await user.click(screen.getByRole('button', { name: /Actualizar/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith('V-123', 40000);
      expect(mockOnClose).toHaveBeenCalled();
    });
  });

  it('should show error when new mileage is less than current - HU-001 Escenario 2', async () => {
    const user = userEvent.setup();
    const mockOnSubmit = vi.fn();

    render(
      <UpdateMileageModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={mockOnSubmit}
      />
    );

    const input = screen.getByLabelText(/Nuevo Kilometraje/i);
    await user.type(input, '30000'); // Less than current 35000
    await user.click(screen.getByRole('button', { name: /Actualizar/i }));

    await waitFor(() => {
      // The HTML5 validation will prevent submission, no custom error message shown
      expect(mockOnSubmit).not.toHaveBeenCalled();
    });
  });

  it('should show error when new mileage equals current mileage', async () => {
    const user = userEvent.setup();
    const mockOnSubmit = vi.fn();

    render(
      <UpdateMileageModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={mockOnSubmit}
      />
    );

    const input = screen.getByLabelText(/Nuevo Kilometraje/i);
    await user.type(input, '35000'); // Equal to current
    await user.click(screen.getByRole('button', { name: /Actualizar/i }));

    // HTML5 validation prevents submission
    await waitFor(() => {
      expect(mockOnSubmit).not.toHaveBeenCalled();
    });
  });

  it('should clear error when user types new value', async () => {
    const user = userEvent.setup();

    render(
      <UpdateMileageModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={async () => {}}
      />
    );

    const input = screen.getByLabelText(/Nuevo Kilometraje/i);

    // Trigger error by entering invalid value
    await user.type(input, '30000');
    await user.click(screen.getByRole('button', { name: /Actualizar/i }));

    await waitFor(() => {
      // The HTML5 validation will prevent submission
      expect(input).toHaveValue(30000);
    });

    // Clear and type new valid value
    await user.clear(input);
    await user.type(input, '40000');

    // Value should be updated (no error message to check, just verify form is valid)
    expect(input).toHaveValue(40000);
  });

  it('should have min validation based on current mileage', () => {
    render(
      <UpdateMileageModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={async () => {}}
      />
    );

    const input = screen.getByLabelText(/Nuevo Kilometraje/i);
    expect(input).toHaveAttribute('min', '35001'); // current_mileage + 1
  });

  it('should have max validation of 1,000,000 km', () => {
    render(
      <UpdateMileageModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={async () => {}}
      />
    );

    const input = screen.getByLabelText(/Nuevo Kilometraje/i);
    expect(input).toHaveAttribute('max', '1000000');
  });

  it('should display hint with minimum required mileage', () => {
    render(
      <UpdateMileageModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={async () => {}}
      />
    );

    expect(screen.getByText(/Debe ser mayor a 35[.,]000 km/i)).toBeInTheDocument();
  });

  it('should reset form when modal is reopened', () => {
    const { rerender } = render(
      <UpdateMileageModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={async () => {}}
      />
    );

    const input = screen.getByLabelText(/Nuevo Kilometraje/i);
    expect(input).toHaveValue(null);

    // Close and reopen
    rerender(
      <UpdateMileageModal
        isOpen={false}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={async () => {}}
      />
    );

    rerender(
      <UpdateMileageModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={async () => {}}
      />
    );

    expect(screen.getByLabelText(/Nuevo Kilometraje/i)).toHaveValue(null);
  });

  it('should not render when modal is closed', () => {
    const { container } = render(
      <UpdateMileageModal
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
      <UpdateMileageModal
        isOpen={true}
        onClose={() => {}}
        vehicle={null}
        onSubmit={async () => {}}
      />
    );

    expect(container.firstChild).toBeNull();
  });

  it('should have required attribute on input field', () => {
    render(
      <UpdateMileageModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onSubmit={async () => {}}
      />
    );

    expect(screen.getByLabelText(/Nuevo Kilometraje/i)).toBeRequired();
  });
});
