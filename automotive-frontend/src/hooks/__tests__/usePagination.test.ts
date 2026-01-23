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
    const { result } = renderHook(() => usePagination(mockItems, 6));

    expect(result.current.currentPage).toBe(1);
  });

  it('should calculate total pages correctly', () => {
    const { result } = renderHook(() => usePagination(mockItems, 6));

    // 20 items / 6 per page = 4 pages (rounded up)
    expect(result.current.totalPages).toBe(4);
  });

  it('should return correct items for first page', () => {
    const { result } = renderHook(() => usePagination(mockItems, 6));

    expect(result.current.paginatedItems).toHaveLength(6);
    expect(result.current.paginatedItems[0].id).toBe('V-1');
    expect(result.current.paginatedItems[5].id).toBe('V-6');
  });

  it('should return correct items for second page', () => {
    const { result } = renderHook(() => usePagination(mockItems, 6));

    act(() => {
      result.current.goToPage(2);
    });

    expect(result.current.paginatedItems).toHaveLength(6);
    expect(result.current.paginatedItems[0].id).toBe('V-7');
    expect(result.current.paginatedItems[5].id).toBe('V-12');
  });

  it('should return correct items for last page with fewer items', () => {
    const { result } = renderHook(() => usePagination(mockItems, 6));

    act(() => {
      result.current.goToPage(4);
    });

    // Last page should have 2 items (20 % 6 = 2)
    expect(result.current.paginatedItems).toHaveLength(2);
    expect(result.current.paginatedItems[0].id).toBe('V-19');
    expect(result.current.paginatedItems[1].id).toBe('V-20');
  });

  it('should go to next page', () => {
    const { result } = renderHook(() => usePagination(mockItems, 6));

    act(() => {
      result.current.nextPage();
    });

    expect(result.current.currentPage).toBe(2);
  });

  it('should go to previous page', () => {
    const { result } = renderHook(() => usePagination(mockItems, 6));

    act(() => {
      result.current.goToPage(3);
    });

    act(() => {
      result.current.previousPage();
    });

    expect(result.current.currentPage).toBe(2);
  });

  it('should not go below page 1', () => {
    const { result } = renderHook(() => usePagination(mockItems, 6));

    act(() => {
      result.current.previousPage();
    });

    expect(result.current.currentPage).toBe(1);
  });

  it('should not go above total pages', () => {
    const { result } = renderHook(() => usePagination(mockItems, 6));

    act(() => {
      result.current.goToPage(4);
    });

    act(() => {
      result.current.nextPage();
    });

    expect(result.current.currentPage).toBe(4);
  });

  it('should reset to page 1 when items change', () => {
    const { result, rerender } = renderHook(({ items }) => usePagination(items, 6), {
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
    const { result } = renderHook(() => usePagination([], 6));

    expect(result.current.totalPages).toBe(0);
    expect(result.current.paginatedItems).toHaveLength(0);
  });

  it('should handle items less than page size', () => {
    const fewItems = mockItems.slice(0, 3);
    const { result } = renderHook(() => usePagination(fewItems, 6));

    expect(result.current.totalPages).toBe(1);
    expect(result.current.paginatedItems).toHaveLength(3);
  });

  it('should calculate correct start and end indices', () => {
    const { result } = renderHook(() => usePagination(mockItems, 6));

    act(() => {
      result.current.goToPage(2);
    });

    expect(result.current.startIndex).toBe(6);
    expect(result.current.endIndex).toBe(12);
  });
});
