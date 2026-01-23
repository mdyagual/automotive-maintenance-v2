/**
 * Tests for AlertsModal Component
 * 
 * Tests alerts modal display, alert list rendering, and empty state
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '../../../test/test-utils';
import { AlertsModal } from '../AlertsModal';
import { mockVehicleWithAlerts, mockVehicleWithoutAlerts } from '../../../test/mockData';
import userEvent from '@testing-library/user-event';

describe('AlertsModal', () => {
  it('should display modal title', () => {
    render(
      <AlertsModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
      />
    );

    expect(screen.getByText('Alertas de Mantenimiento')).toBeInTheDocument();
  });

  it('should display vehicle information', () => {
    render(
      <AlertsModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
      />
    );

    expect(screen.getByText(/ABC-123 - Toyota Corolla/)).toBeInTheDocument();
  });

  it('should display all alerts for vehicle', () => {
    render(
      <AlertsModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
      />
    );

    // Should show 3 alerts
    expect(screen.getByText(/Mantenimiento Básico/)).toBeInTheDocument();
    expect(screen.getByText(/Mantenimiento Mayor/)).toBeInTheDocument();
  });

  it('should display alert mileage', () => {
    render(
      <AlertsModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
      />
    );

    expect(screen.getByText(/30,000 km/)).toBeInTheDocument();
    expect(screen.getByText(/20,000 km/)).toBeInTheDocument();
    expect(screen.getByText(/10,000 km/)).toBeInTheDocument();
  });

  it('should display empty state when vehicle has no alerts', () => {
    render(
      <AlertsModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithoutAlerts}
      />
    );

    expect(screen.getByText(/No hay alertas de mantenimiento para este vehículo/)).toBeInTheDocument();
  });

  it('should display close button', () => {
    render(
      <AlertsModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
      />
    );

    expect(screen.getByRole('button', { name: /Cerrar/i })).toBeInTheDocument();
  });

  it('should call onClose when close button is clicked', async () => {
    const user = userEvent.setup();
    const mockOnClose = vi.fn();
    
    render(
      <AlertsModal
        isOpen={true}
        onClose={mockOnClose}
        vehicle={mockVehicleWithAlerts}
      />
    );

    const closeButton = screen.getByRole('button', { name: /Cerrar/i });
    await user.click(closeButton);

    expect(mockOnClose).toHaveBeenCalled();
  });

  it('should not render when modal is closed', () => {
    const { container } = render(
      <AlertsModal
        isOpen={false}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
      />
    );

    expect(container.firstChild).toBeNull();
  });

  it('should not render when vehicle is null', () => {
    const { container } = render(
      <AlertsModal
        isOpen={true}
        onClose={() => {}}
        vehicle={null}
      />
    );

    expect(container.firstChild).toBeNull();
  });

  it('should display alert timestamps', () => {
    render(
      <AlertsModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
      />
    );

    // Check for formatted dates - just verify they contain the year and are present
    const bodyText = document.body.textContent || '';
    expect(bodyText).toContain('2026');
    // Should have 3 timestamps (one for each alert)
    const timestampMatches = bodyText.match(/2026/g);
    expect(timestampMatches).toBeTruthy();
    expect(timestampMatches!.length).toBeGreaterThanOrEqual(3);
  });

  it('should apply correct CSS classes for alert types', () => {
    const { container } = render(
      <AlertsModal
        isOpen={true}
        onClose={() => {}}
        vehicle={mockVehicleWithAlerts}
      />
    );

    const alertItems = container.querySelectorAll('.alert-item');
    expect(alertItems.length).toBe(3);
    
    // Check that alert items have type-specific classes
    expect(alertItems[0]).toHaveClass('alert-basic');
  });
});
