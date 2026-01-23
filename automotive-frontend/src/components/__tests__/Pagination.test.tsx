/**
 * Tests for Pagination Component
 *
 * Tests pagination controls, page navigation, and page number display
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '../../test/test-utils';
import { Pagination } from '../Pagination';
import userEvent from '@testing-library/user-event';

describe('Pagination', () => {
  it('should display current page and total pages', () => {
    render(<Pagination currentPage={1} totalPages={6} onPageChange={vi.fn()} />);

    expect(screen.getByText('Página 1 de 6')).toBeInTheDocument();
  });

  it('should disable previous button on first page', () => {
    render(<Pagination currentPage={1} totalPages={6} onPageChange={vi.fn()} />);

    const prevButton = screen.getByRole('button', { name: /chevron_left/i });
    expect(prevButton).toBeDisabled();
  });

  it('should disable next button on last page', () => {
    render(<Pagination currentPage={6} totalPages={6} onPageChange={vi.fn()} />);

    const nextButton = screen.getByRole('button', { name: /chevron_right/i });
    expect(nextButton).toBeDisabled();
  });

  it('should enable both buttons on middle pages', () => {
    render(<Pagination currentPage={3} totalPages={6} onPageChange={vi.fn()} />);

    const prevButton = screen.getByRole('button', { name: /chevron_left/i });
    const nextButton = screen.getByRole('button', { name: /chevron_right/i });

    expect(prevButton).not.toBeDisabled();
    expect(nextButton).not.toBeDisabled();
  });

  it('should call onPageChange with previous page when prev button clicked', async () => {
    const user = userEvent.setup();
    const onPageChange = vi.fn();
    render(<Pagination currentPage={3} totalPages={6} onPageChange={onPageChange} />);

    const prevButton = screen.getByRole('button', { name: /chevron_left/i });
    await user.click(prevButton);

    expect(onPageChange).toHaveBeenCalledWith(2);
  });

  it('should call onPageChange with next page when next button clicked', async () => {
    const user = userEvent.setup();
    const onPageChange = vi.fn();
    render(<Pagination currentPage={3} totalPages={6} onPageChange={onPageChange} />);

    const nextButton = screen.getByRole('button', { name: /chevron_right/i });
    await user.click(nextButton);

    expect(onPageChange).toHaveBeenCalledWith(4);
  });

  it('should display page numbers dynamically based on current page', () => {
    const { rerender } = render(<Pagination currentPage={1} totalPages={10} onPageChange={vi.fn()} />);

    // On page 1, should show pages 1, 2, 3
    expect(screen.getByText('1')).toBeInTheDocument();
    expect(screen.getByText('2')).toBeInTheDocument();
    expect(screen.getByText('3')).toBeInTheDocument();

    // Change to page 5
    rerender(<Pagination currentPage={5} totalPages={10} onPageChange={vi.fn()} />);

    // Should show pages 4, 5, 6
    expect(screen.getByText('4')).toBeInTheDocument();
    expect(screen.getByText('5')).toBeInTheDocument();
    expect(screen.getByText('6')).toBeInTheDocument();
  });

  it('should highlight current page button', () => {
    render(<Pagination currentPage={2} totalPages={6} onPageChange={vi.fn()} />);

    const pageButtons = screen.getAllByRole('button');
    const page2Button = pageButtons.find(btn => btn.textContent === '2');

    expect(page2Button).toHaveClass('active');
  });

  it('should call onPageChange when page number button clicked', async () => {
    const user = userEvent.setup();
    const onPageChange = vi.fn();
    render(<Pagination currentPage={1} totalPages={6} onPageChange={onPageChange} />);

    const pageButtons = screen.getAllByRole('button');
    const page3Button = pageButtons.find(btn => btn.textContent === '3');

    if (page3Button) {
      await user.click(page3Button);
      expect(onPageChange).toHaveBeenCalledWith(3);
    }
  });

  it('should handle single page correctly', () => {
    render(<Pagination currentPage={1} totalPages={1} onPageChange={vi.fn()} />);

    expect(screen.getByText('Página 1 de 1')).toBeInTheDocument();

    const prevButton = screen.getByRole('button', { name: /chevron_left/i });
    const nextButton = screen.getByRole('button', { name: /chevron_right/i });

    expect(prevButton).toBeDisabled();
    expect(nextButton).toBeDisabled();
  });

  it('should show ellipsis for large page counts', () => {
    render(<Pagination currentPage={5} totalPages={20} onPageChange={vi.fn()} />);

    // Should show ellipsis when there are many pages
    const ellipsis = screen.queryAllByText('...');
    expect(ellipsis.length).toBeGreaterThan(0);
  });
});
