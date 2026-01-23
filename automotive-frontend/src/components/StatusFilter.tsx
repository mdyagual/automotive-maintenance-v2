interface StatusFilterProps {
  currentFilter: 'all' | 'active' | 'inactive' | 'in_maintenance' | 'retired';
  onFilterChange: (filter: 'all' | 'active' | 'inactive' | 'in_maintenance' | 'retired') => void;
}

export const StatusFilter = ({ currentFilter, onFilterChange }: StatusFilterProps) => {
  const filters: Array<{
    value: 'all' | 'active' | 'inactive' | 'in_maintenance' | 'retired';
    label: string;
  }> = [
    { value: 'all', label: 'TODOS' },
    { value: 'active', label: 'ACTIVO' },
    { value: 'inactive', label: 'INACTIVO' },
    { value: 'in_maintenance', label: 'MANTENIMIENTO' },
    { value: 'retired', label: 'RETIRADO' },
  ];

  return (
    <div className="status-filter">
      <div className="filter-buttons">
        {filters.map((filter) => (
          <button
            key={filter.value}
            className={`filter-btn ${currentFilter === filter.value ? 'active' : ''}`}
            onClick={() => onFilterChange(filter.value)}
          >
            {filter.label}
          </button>
        ))}
      </div>
    </div>
  );
};
