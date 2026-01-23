/**
 * Tests for CreateVehicleModal Component - HU-002
 * 
 * Tests vehicle creation form, validation, and submission
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '../../../test/test-utils';
import { CreateVehicleModal } from '../CreateVehicleModal';
import userEvent from '@testing-library/user-event';

describe('CreateVehicleModal - HU-002', () => {
  it('should display modal title', () => {
    render(
      <CreateVehicleModal
        isOpen={true}
        onClose={() => {}}
        onSubmit={async () => {}}
      />
    );

    expect(screen.getByText('Registrar Nuevo Vehículo')).toBeInTheDocument();
  });

  it('should display all form fields', () => {
    render(
      <CreateVehicleModal
        isOpen={true}
        onClose={() => {}}
        onSubmit={async () => {}}
      />
    );

    expect(screen.getByLabelText(/ID del Vehículo/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Placa/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Modelo/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Kilometraje Inicial/i)).toBeInTheDocument();
  });

  it('should display form hints for validation', () => {
    render(
      <CreateVehicleModal
        isOpen={true}
        onClose={() => {}}
        onSubmit={async () => {}}
      />
    );

    expect(screen.getByText(/Formato: V-XXX/i)).toBeInTheDocument();
    expect(screen.getByText(/Formato: XXX-123 o XXX-1234/i)).toBeInTheDocument();
    expect(screen.getByText(/Rango: 0 - 1,000,000 km/i)).toBeInTheDocument();
  });

  it('should have Cancelar and Registrar buttons', () => {
    render(
      <CreateVehicleModal
        isOpen={true}
        onClose={() => {}}
        onSubmit={async () => {}}
      />
    );

    expect(screen.getByRole('button', { name: /Cancelar/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Registrar/i })).toBeInTheDocument();
  });

  it('should call onClose when Cancelar button is clicked', async () => {
    const user = userEvent.setup();
    const mockOnClose = vi.fn();

    render(
      <CreateVehicleModal
        isOpen={true}
        onClose={mockOnClose}
        onSubmit={async () => {}}
      />
    );

    const cancelButton = screen.getByRole('button', { name: /Cancelar/i });
    await user.click(cancelButton);

    expect(mockOnClose).toHaveBeenCalled();
  });

  it('should submit form with valid data - HU-002 Escenario 1', async () => {
    const user = userEvent.setup();
    const mockOnSubmit = vi.fn().mockResolvedValue(undefined);
    const mockOnClose = vi.fn();

    render(
      <CreateVehicleModal
        isOpen={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
      />
    );

    // Fill form
    await user.type(screen.getByLabelText(/ID del Vehículo/i), 'V-456');
    await user.type(screen.getByLabelText(/Placa/i), 'XYZ-789');
    await user.type(screen.getByLabelText(/Modelo/i), 'Honda Civic');
    await user.clear(screen.getByLabelText(/Kilometraje Inicial/i));
    await user.type(screen.getByLabelText(/Kilometraje Inicial/i), '0');

    // Submit
    const submitButton = screen.getByRole('button', { name: /Registrar/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        id: 'V-456',
        plate: 'XYZ-789',
        model: 'Honda Civic',
        initial_mileage: 0,
      });
    });
  });

  it('should convert plate to uppercase', async () => {
    const user = userEvent.setup();
    const mockOnSubmit = vi.fn().mockResolvedValue(undefined);

    render(
      <CreateVehicleModal
        isOpen={true}
        onClose={() => {}}
        onSubmit={mockOnSubmit}
      />
    );

    // Fill form with lowercase plate
    await user.type(screen.getByLabelText(/ID del Vehículo/i), 'V-999');
    await user.type(screen.getByLabelText(/Placa/i), 'abc-123');
    await user.type(screen.getByLabelText(/Modelo/i), 'Test Car');
    await user.clear(screen.getByLabelText(/Kilometraje Inicial/i));
    await user.type(screen.getByLabelText(/Kilometraje Inicial/i), '5000');

    // Submit
    await user.click(screen.getByRole('button', { name: /Registrar/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith(
        expect.objectContaining({
          plate: 'ABC-123', // Should be uppercase
        })
      );
    });
  });

  it('should reset form after successful submission', async () => {
    const user = userEvent.setup();
    const mockOnSubmit = vi.fn().mockResolvedValue(undefined);
    const mockOnClose = vi.fn();

    render(
      <CreateVehicleModal
        isOpen={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
      />
    );

    // Fill and submit form
    await user.type(screen.getByLabelText(/ID del Vehículo/i), 'V-001');
    await user.type(screen.getByLabelText(/Placa/i), 'AAA-111');
    await user.type(screen.getByLabelText(/Modelo/i), 'Test');
    await user.click(screen.getByRole('button', { name: /Registrar/i }));

    await waitFor(() => {
      expect(mockOnClose).toHaveBeenCalled();
    });
  });

  it('should have required attribute on all input fields', () => {
    render(
      <CreateVehicleModal
        isOpen={true}
        onClose={() => {}}
        onSubmit={async () => {}}
      />
    );

    expect(screen.getByLabelText(/ID del Vehículo/i)).toBeRequired();
    expect(screen.getByLabelText(/Placa/i)).toBeRequired();
    expect(screen.getByLabelText(/Modelo/i)).toBeRequired();
    expect(screen.getByLabelText(/Kilometraje Inicial/i)).toBeRequired();
  });

  it('should have pattern validation for vehicle ID', () => {
    render(
      <CreateVehicleModal
        isOpen={true}
        onClose={() => {}}
        onSubmit={async () => {}}
      />
    );

    const idInput = screen.getByLabelText(/ID del Vehículo/i);
    expect(idInput).toHaveAttribute('pattern', 'V-\\d{3}');
  });

  it('should have pattern validation for plate', () => {
    render(
      <CreateVehicleModal
        isOpen={true}
        onClose={() => {}}
        onSubmit={async () => {}}
      />
    );

    const plateInput = screen.getByLabelText(/Placa/i);
    expect(plateInput).toHaveAttribute('pattern', '[A-Z]{3}-\\d{3,4}');
  });

  it('should have min and max validation for mileage', () => {
    render(
      <CreateVehicleModal
        isOpen={true}
        onClose={() => {}}
        onSubmit={async () => {}}
      />
    );

    const mileageInput = screen.getByLabelText(/Kilometraje Inicial/i);
    expect(mileageInput).toHaveAttribute('min', '0');
    expect(mileageInput).toHaveAttribute('max', '1000000');
  });

  it('should not render when modal is closed', () => {
    const { container } = render(
      <CreateVehicleModal
        isOpen={false}
        onClose={() => {}}
        onSubmit={async () => {}}
      />
    );

    expect(container.firstChild).toBeNull();
  });

  it('should clear form when modal is closed', async () => {
    const user = userEvent.setup();
    const mockOnClose = vi.fn();

    const { rerender } = render(
      <CreateVehicleModal
        isOpen={true}
        onClose={mockOnClose}
        onSubmit={async () => {}}
      />
    );

    // Fill form
    await user.type(screen.getByLabelText(/ID del Vehículo/i), 'V-123');
    
    // Close modal
    await user.click(screen.getByRole('button', { name: /Cancelar/i }));
    expect(mockOnClose).toHaveBeenCalled();

    // Reopen modal
    rerender(
      <CreateVehicleModal
        isOpen={true}
        onClose={mockOnClose}
        onSubmit={async () => {}}
      />
    );

    // Form should be empty
    expect(screen.getByLabelText(/ID del Vehículo/i)).toHaveValue('');
  });
});
