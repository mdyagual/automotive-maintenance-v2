import { useState, useMemo, useEffect } from 'react';

interface UsePaginationReturn<T> {
  currentPage: number;
  totalPages: number;
  paginatedItems: T[];
  startIndex: number;
  endIndex: number;
  goToPage: (page: number) => void;
  nextPage: () => void;
  previousPage: () => void;
}

/**
 * Custom hook for pagination logic
 * @param items - Array of items to paginate
 * @param itemsPerPage - Number of items per page
 * @returns Pagination state and controls
 */
export function usePagination<T>(
  items: T[],
  itemsPerPage: number
): UsePaginationReturn<T> {
  const [currentPage, setCurrentPage] = useState(1);

  // Calculate total pages
  const totalPages = useMemo(() => {
    if (items.length === 0) return 0;
    return Math.ceil(items.length / itemsPerPage);
  }, [items.length, itemsPerPage]);

  // Calculate start and end indices
  const startIndex = useMemo(() => {
    return (currentPage - 1) * itemsPerPage;
  }, [currentPage, itemsPerPage]);

  const endIndex = useMemo(() => {
    return Math.min(startIndex + itemsPerPage, items.length);
  }, [startIndex, itemsPerPage, items.length]);

  // Get paginated items
  const paginatedItems = useMemo(() => {
    return items.slice(startIndex, endIndex);
  }, [items, startIndex, endIndex]);

  // Reset to page 1 when items change
  useEffect(() => {
    setCurrentPage(1);
  }, [items]);

  // Navigation functions
  const goToPage = (page: number) => {
    const pageNumber = Math.max(1, Math.min(page, totalPages));
    setCurrentPage(pageNumber);
  };

  const nextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage((prev) => prev + 1);
    }
  };

  const previousPage = () => {
    if (currentPage > 1) {
      setCurrentPage((prev) => prev - 1);
    }
  };

  return {
    currentPage,
    totalPages,
    paginatedItems,
    startIndex,
    endIndex,
    goToPage,
    nextPage,
    previousPage,
  };
}
