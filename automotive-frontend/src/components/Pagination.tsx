interface PaginationProps {
  currentPage?: number;
  totalPages?: number;
}

export const Pagination = ({ currentPage = 1, totalPages = 6 }: PaginationProps) => {
  return (
    <div className="pagination">
      <span className="pagination-info">
        Página {currentPage} de {totalPages}
      </span>
      <div className="pagination-controls">
        <button className="pagination-btn" disabled={currentPage === 1}>
          <span className="material-symbols-outlined">chevron_left</span>
        </button>
        <div className="pagination-numbers">
          <button className={`pagination-btn ${currentPage === 1 ? 'active' : ''}`}>1</button>
          <button className={`pagination-btn ${currentPage === 2 ? 'active' : ''}`}>2</button>
          <button className={`pagination-btn ${currentPage === 3 ? 'active' : ''}`}>3</button>
        </div>
        <button className="pagination-btn" disabled={currentPage === totalPages}>
          <span className="material-symbols-outlined">chevron_right</span>
        </button>
      </div>
    </div>
  );
};
