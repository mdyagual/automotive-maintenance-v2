/**
 * Tests for StatusFilter Component - HU-005 Escenario 2
 *
 * Tests status filter functionality for filtering vehicles by operational status
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '../../test/test-utils';
import { StatusFilter } from '../StatusFilter';
import userEvent from '@testing-library/user-event';

describe('StatusFilter - HU-005 Escenario 2', () => {
  it('should render all filter buttons', () => {
    const mockOnFilterChange = vi.fn();
    render(<StatusFilter currentFilter="all" onFilterChange={mockOnFilterChange} />);

    expect(screen.getByRole('button', { name: 'TODOS' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'ACTIVO' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'INACTIVO' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'MANTENIMIENTO' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'RETIRADO' })).toBeInTheDocument();
  });

  it('should highlight active filter button', () => {
    const mockOnFilterChange = vi.fn();
    render(<StatusFilter currentFilter="active" onFilterChange={mockOnFilterChange} />);

    const activeButton = screen.getByRole('button', { name: 'ACTIVO' });
    expect(activeButton).toHaveClass('active');
  });

  it('should highlight all filter button when selected', () => {
    const mockOnFilterChange = vi.fn();
    render(<StatusFilter currentFilter="all" onFilterChange={mockOnFilterChange} />);

    const allButton = screen.getByRole('button', { name: 'TODOS' });
    expect(allButton).toHaveClass('active');
  });

  it('should call onFilterChange when filter button is clicked', async () => {
    const user = userEvent.setup();
    const mockOnFilterChange = vi.fn();
    render(<StatusFilter currentFilter="all" onFilterChange={mockOnFilterChange} />);

    const activeButton = screen.getByRole('button', { name: 'ACTIVO' });
    await user.click(activeButton);

    expect(mockOnFilterChange).toHaveBeenCalledWith('active');
  });

  it('should call onFilterChange with correct status for each button', async () => {
    const user = userEvent.setup();
    const mockOnFilterChange = vi.fn();
    render(<StatusFilter currentFilter="all" onFilterChange={mockOnFilterChange} />);

    // Test TODOS button
    await user.click(screen.getByRole('button', { name: 'TODOS' }));
    expect(mockOnFilterChange).toHaveBeenCalledWith('all');

    // Test ACTIVO button
    await user.click(screen.getByRole('button', { name: 'ACTIVO' }));
    expect(mockOnFilterChange).toHaveBeenCalledWith('active');

    // Test INACTIVO button
    await user.click(screen.getByRole('button', { name: 'INACTIVO' }));
    expect(mockOnFilterChange).toHaveBeenCalledWith('inactive');

    // Test MANTENIMIENTO button
    await user.click(screen.getByRole('button', { name: 'MANTENIMIENTO' }));
    expect(mockOnFilterChange).toHaveBeenCalledWith('in_maintenance');

    // Test RETIRADO button
    await user.click(screen.getByRole('button', { name: 'RETIRADO' }));
    expect(mockOnFilterChange).toHaveBeenCalledWith('retired');
  });

  it('should only highlight one filter at a time', () => {
    const mockOnFilterChange = vi.fn();
    render(<StatusFilter currentFilter="in_maintenance" onFilterChange={mockOnFilterChange} />);

    const maintenanceButton = screen.getByRole('button', { name: 'MANTENIMIENTO' });
    const activeButton = screen.getByRole('button', { name: 'ACTIVO' });
    const allButton = screen.getByRole('button', { name: 'TODOS' });

    expect(maintenanceButton).toHaveClass('active');
    expect(activeButton).not.toHaveClass('active');
    expect(allButton).not.toHaveClass('active');
  });

  it('should handle retired filter selection', () => {
    const mockOnFilterChange = vi.fn();
    render(<StatusFilter currentFilter="retired" onFilterChange={mockOnFilterChange} />);

    const retiredButton = screen.getByRole('button', { name: 'RETIRADO' });
    expect(retiredButton).toHaveClass('active');
  });

  it('should handle inactive filter selection', () => {
    const mockOnFilterChange = vi.fn();
    render(<StatusFilter currentFilter="inactive" onFilterChange={mockOnFilterChange} />);

    const inactiveButton = screen.getByRole('button', { name: 'INACTIVO' });
    expect(inactiveButton).toHaveClass('active');
  });
});
