import type { VehicleStatus } from '../types/vehicle';

interface StatusFilterProps {
  currentFilter: VehicleStatus | 'all';
  onFilterChange: (filter: VehicleStatus | 'all') => void;
}

export const StatusFilter = ({ currentFilter, onFilterChange }: StatusFilterProps) => {
  const filters: Array<{ value: VehicleStatus | 'all'; label: string }> = [
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
