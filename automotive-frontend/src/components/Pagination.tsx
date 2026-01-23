interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

export const Pagination = ({ currentPage, totalPages, onPageChange }: PaginationProps) => {
  // Calculate which page numbers to show
  const getPageNumbers = () => {
    const pages: (number | string)[] = [];
    const maxVisible = 3;

    if (totalPages <= maxVisible + 2) {
      // Show all pages if total is small
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      // Show pages with ellipsis for large page counts
      if (currentPage <= 2) {
        // Near start
        pages.push(1, 2, 3, '...', totalPages);
      } else if (currentPage >= totalPages - 1) {
        // Near end
        pages.push(1, '...', totalPages - 2, totalPages - 1, totalPages);
      } else {
        // In middle
        pages.push(1, '...', currentPage - 1, currentPage, currentPage + 1, '...', totalPages);
      }
    }

    return pages;
  };

  const handlePrevious = () => {
    if (currentPage > 1) {
      onPageChange(currentPage - 1);
    }
  };

  const handleNext = () => {
    if (currentPage < totalPages) {
      onPageChange(currentPage + 1);
    }
  };

  const handlePageClick = (page: number | string) => {
    if (typeof page === 'number') {
      onPageChange(page);
    }
  };

  const pageNumbers = getPageNumbers();

  return (
    <div className="pagination">
      <span className="pagination-info">
        Página {currentPage} de {totalPages}
      </span>
      <div className="pagination-controls">
        <button
          className="pagination-btn"
          disabled={currentPage === 1}
          onClick={handlePrevious}
          aria-label="chevron_left"
        >
          <span className="material-symbols-outlined">chevron_left</span>
        </button>
        <div className="pagination-numbers">
          {pageNumbers.map((page, index) => (
            <button
              key={`${page}-${index}`}
              className={`pagination-btn ${page === currentPage ? 'active' : ''}`}
              onClick={() => handlePageClick(page)}
              disabled={typeof page === 'string'}
            >
              {page}
            </button>
          ))}
        </div>
        <button
          className="pagination-btn"
          disabled={currentPage === totalPages}
          onClick={handleNext}
          aria-label="chevron_right"
        >
          <span className="material-symbols-outlined">chevron_right</span>
        </button>
      </div>
    </div>
  );
};
