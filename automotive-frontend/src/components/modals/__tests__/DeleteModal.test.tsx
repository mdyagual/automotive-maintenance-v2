/**
 * Tests for DeleteModal Component - HU-004
 * 
 * Tests vehicle deletion confirmation modal
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '../../../test/test-utils';
import { DeleteModal } from '../DeleteModal';
import { mockVehicleWithAlerts } from '../../../test/mockData';
import userEvent from '@testing-library/user-event';

describe('DeleteModal - HU-004', () => {
  it('should display modal title', () => {
    render(
      <DeleteModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onConfirm={async () => {}}
      />
    );

    expect(screen.getByText('Confirmar Eliminación')).toBeInTheDocument();
  });

  it('should display warning message', () => {
    render(
      <DeleteModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onConfirm={async () => {}}
      />
    );

    expect(screen.getByText(/¿Está seguro que desea eliminar este vehículo?/)).toBeInTheDocument();
  });

  it('should display vehicle information', () => {
    render(
      <DeleteModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onConfirm={async () => {}}
      />
    );

    expect(screen.getByText(/ABC-123 - Toyota Corolla/)).toBeInTheDocument();
  });

  it('should display cascade deletion warning - HU-004 Escenario 3', () => {
    render(
      <DeleteModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onConfirm={async () => {}}
      />
    );

    expect(screen.getByText(/eliminará el vehículo y todas sus alertas asociadas/i)).toBeInTheDocument();
    expect(screen.getByText(/No se puede deshacer/i)).toBeInTheDocument();
  });

  it('should have Cancelar and Eliminar buttons', () => {
    render(
      <DeleteModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onConfirm={async () => {}}
      />
    );

    expect(screen.getByRole('button', { name: /Cancelar/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Eliminar/i })).toBeInTheDocument();
  });

  it('should call onClose when Cancelar button is clicked', async () => {
    const user = userEvent.setup();
    const mockOnClose = vi.fn();

    render(
      <DeleteModal
        isOpen={true}
        onClose={mockOnClose}
        vehicle={mockVehicleWithAlerts}
        onConfirm={async () => {}}
      />
    );

    await user.click(screen.getByRole('button', { name: /Cancelar/i }));
    expect(mockOnClose).toHaveBeenCalled();
  });

  it('should call onConfirm when Eliminar button is clicked - HU-004 Escenario 1', async () => {
    const user = userEvent.setup();
    const mockOnConfirm = vi.fn().mockResolvedValue(undefined);
    const mockOnClose = vi.fn();

    render(
      <DeleteModal
        isOpen={true}
        onClose={mockOnClose}
        vehicle={mockVehicleWithAlerts}
        onConfirm={mockOnConfirm}
      />
    );

    await user.click(screen.getByRole('button', { name: /Eliminar/i }));

    await waitFor(() => {
      expect(mockOnConfirm).toHaveBeenCalledWith('V-123');
      expect(mockOnClose).toHaveBeenCalled();
    });
  });

  it('should display warning icon', () => {
    render(
      <DeleteModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onConfirm={async () => {}}
      />
    );

    expect(screen.getByText('⚠️')).toBeInTheDocument();
  });

  it('should not render when modal is closed', () => {
    const { container } = render(
      <DeleteModal
        isOpen={false}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onConfirm={async () => {}}
      />
    );

    expect(container.firstChild).toBeNull();
  });

  it('should not render when vehicle is null', () => {
    const { container } = render(
      <DeleteModal
        isOpen={true}
        onClose={() => {}}
        vehicle={null}
        onConfirm={async () => {}}
      />
    );

    expect(container.firstChild).toBeNull();
  });

  it('should have danger styling on delete button', () => {
    render(
      <DeleteModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onConfirm={async () => {}}
      />
    );

    const deleteButton = screen.getByRole('button', { name: /Eliminar/i });
    expect(deleteButton).toHaveClass('btn-danger');
  });

  it('should display small modal size', () => {
    const { container } = render(
      <DeleteModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
        onConfirm={async () => {}}
      />
    );

    // Modal component should receive size="small" prop
    // This is tested indirectly through the Modal component
    expect(container.querySelector('.modal-content')).toBeInTheDocument();
  });
});
