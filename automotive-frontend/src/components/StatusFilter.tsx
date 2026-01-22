import type { VehicleStatus } from '../types/vehicle';
import { getStatusText, getStatusIcon } from '../utils/formatters';

interface StatusFilterProps {
  currentFilter: VehicleStatus | 'all';
  onFilterChange: (filter: VehicleStatus | 'all') => void;
}

export const StatusFilter = ({ currentFilter, onFilterChange }: StatusFilterProps) => {
  const filters: Array<{ value: VehicleStatus | 'all'; label: string; icon: string }> = [
    { value: 'all', label: 'Todos', icon: '📋' },
    { value: 'active', label: getStatusText('active'), icon: getStatusIcon('active') },
    { value: 'inactive', label: getStatusText('inactive'), icon: getStatusIcon('inactive') },
    { value: 'in_maintenance', label: getStatusText('in_maintenance'), icon: getStatusIcon('in_maintenance') },
    { value: 'retired', label: getStatusText('retired'), icon: getStatusIcon('retired') },
  ];

  return (
    <div className="status-filter">
      <label className="filter-label">Filtrar por estado:</label>
      <div className="filter-buttons">
        {filters.map((filter) => (
          <button
            key={filter.value}
            className={`filter-btn ${currentFilter === filter.value ? 'active' : ''}`}
            onClick={() => onFilterChange(filter.value)}
          >
            <span className="filter-icon">{filter.icon}</span>
            {filter.label}
          </button>
        ))}
      </div>
    </div>
  );
};
