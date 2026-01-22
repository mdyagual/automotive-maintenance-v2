import type { Vehicle } from '../types/vehicle';
import { formatNumber, getAlertBadgeClass, getAlertIcon, getStatusText, getStatusBadgeClass, getStatusIcon } from '../utils/formatters';

interface VehicleCardProps {
  vehicle: Vehicle;
  onUpdate: (vehicleId: string) => void;
  onDetails: (vehicleId: string) => void;
  onDelete: (vehicleId: string) => void;
  onAlerts: (vehicleId: string) => void;
  onUpdateStatus: (vehicleId: string) => void;
}

export const VehicleCard = ({ vehicle, onUpdate, onDetails, onDelete, onAlerts, onUpdateStatus }: VehicleCardProps) => {
  const alertCount = vehicle.alerts?.length || 0;
  const badgeClass = getAlertBadgeClass(alertCount);
  const badgeIcon = getAlertIcon(alertCount);
  const statusBadgeClass = getStatusBadgeClass(vehicle.status);
  const statusIcon = getStatusIcon(vehicle.status);
  const statusText = getStatusText(vehicle.status);
  const isRetired = vehicle.status === 'retired';

  return (
    <div className="vehicle-card">
      <div className="vehicle-header">
        <div>
          <div className="vehicle-id">{vehicle.id}</div>
          <div className="vehicle-plate">{vehicle.plate}</div>
        </div>
        <div className="vehicle-badges">
          <span className={`status-badge ${statusBadgeClass}`} onClick={() => onUpdateStatus(vehicle.id)}>
            {statusIcon} {statusText}
          </span>
          <span className={`badge ${badgeClass}`} onClick={() => onAlerts(vehicle.id)}>
            {badgeIcon} {alertCount}
          </span>
        </div>
      </div>

      <div className="vehicle-model">{vehicle.model}</div>

      <div className="vehicle-mileage">
        <span className="mileage-icon">📊</span>
        <div>
          <div className="mileage-value">{formatNumber(vehicle.current_mileage)} km</div>
          <div className="mileage-label">Kilometraje actual</div>
        </div>
      </div>

      <div className="vehicle-actions">
        <button 
          className="btn btn-small btn-primary" 
          onClick={() => onUpdate(vehicle.id)}
          disabled={isRetired}
          title={isRetired ? 'No se puede actualizar kilometraje de vehículos retirados' : 'Actualizar kilometraje'}
        >
          Actualizar KM
        </button>
        <button className="btn btn-small btn-secondary" onClick={() => onDetails(vehicle.id)}>
          Ver Detalles
        </button>
        <button className="btn btn-small btn-danger" onClick={() => onDelete(vehicle.id)}>
          Eliminar
        </button>
      </div>
    </div>
  );
};
