/**
 * Tests for usePagination Hook
 *
 * Tests pagination logic, page calculations, and data slicing
 */

import { describe, it, expect } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { usePagination } from '../usePagination';

describe('usePagination', () => {
  const mockItems = Array.from({ length: 20 }, (_, i) => ({
    id: `V-${i + 1}`,
    name: `Vehicle ${i + 1}`,
  }));

  it('should initialize with page 1', () => {
    const { result } = renderHook(() => usePagination(mockItems, 8));

    expect(result.current.currentPage).toBe(1);
  });

  it('should calculate total pages correctly', () => {
    const { result } = renderHook(() => usePagination(mockItems, 8));

    // 20 items / 8 per page = 3 pages (rounded up)
    expect(result.current.totalPages).toBe(3);
  });

  it('should return correct items for first page', () => {
    const { result } = renderHook(() => usePagination(mockItems, 8));

    expect(result.current.paginatedItems).toHaveLength(8);
    expect(result.current.paginatedItems[0].id).toBe('V-1');
    expect(result.current.paginatedItems[7].id).toBe('V-8');
  });

  it('should return correct items for second page', () => {
    const { result } = renderHook(() => usePagination(mockItems, 8));

    act(() => {
      result.current.goToPage(2);
    });

    expect(result.current.paginatedItems).toHaveLength(8);
    expect(result.current.paginatedItems[0].id).toBe('V-9');
    expect(result.current.paginatedItems[7].id).toBe('V-16');
  });

  it('should return correct items for last page with fewer items', () => {
    const { result } = renderHook(() => usePagination(mockItems, 8));

    act(() => {
      result.current.goToPage(3);
    });

    // Last page should have 4 items (20 % 8 = 4)
    expect(result.current.paginatedItems).toHaveLength(4);
    expect(result.current.paginatedItems[0].id).toBe('V-17');
    expect(result.current.paginatedItems[3].id).toBe('V-20');
  });

  it('should go to next page', () => {
    const { result } = renderHook(() => usePagination(mockItems, 8));

    act(() => {
      result.current.nextPage();
    });

    expect(result.current.currentPage).toBe(2);
  });

  it('should go to previous page', () => {
    const { result } = renderHook(() => usePagination(mockItems, 8));

    act(() => {
      result.current.goToPage(3);
    });

    act(() => {
      result.current.previousPage();
    });

    expect(result.current.currentPage).toBe(2);
  });

  it('should not go below page 1', () => {
    const { result } = renderHook(() => usePagination(mockItems, 8));

    act(() => {
      result.current.previousPage();
    });

    expect(result.current.currentPage).toBe(1);
  });

  it('should not go above total pages', () => {
    const { result } = renderHook(() => usePagination(mockItems, 8));

    act(() => {
      result.current.goToPage(3);
    });

    act(() => {
      result.current.nextPage();
    });

    expect(result.current.currentPage).toBe(3);
  });

  it('should reset to page 1 when items change', () => {
    const { result, rerender } = renderHook(({ items }) => usePagination(items, 8), {
      initialProps: { items: mockItems },
    });

    act(() => {
      result.current.goToPage(3);
    });

    expect(result.current.currentPage).toBe(3);

    // Change items
    const newItems = mockItems.slice(0, 10);
    rerender({ items: newItems });

    expect(result.current.currentPage).toBe(1);
  });

  it('should handle empty items array', () => {
    const { result } = renderHook(() => usePagination([], 8));

    expect(result.current.totalPages).toBe(0);
    expect(result.current.paginatedItems).toHaveLength(0);
  });

  it('should handle items less than page size', () => {
    const fewItems = mockItems.slice(0, 3);
    const { result } = renderHook(() => usePagination(fewItems, 8));

    expect(result.current.totalPages).toBe(1);
    expect(result.current.paginatedItems).toHaveLength(3);
  });

  it('should calculate correct start and end indices', () => {
    const { result } = renderHook(() => usePagination(mockItems, 8));

    act(() => {
      result.current.goToPage(2);
    });

    expect(result.current.startIndex).toBe(8);
    expect(result.current.endIndex).toBe(16);
  });
});
