import type { Vehicle } from '../types/vehicle';
import { formatNumber, getAlertBadgeClass, getAlertIcon } from '../utils/formatters';

interface VehicleCardProps {
  vehicle: Vehicle;
  onUpdate: (vehicleId: string) => void;
  onDetails: (vehicleId: string) => void;
  onDelete: (vehicleId: string) => void;
  onAlerts: (vehicleId: string) => void;
}

export const VehicleCard = ({ vehicle, onUpdate, onDetails, onDelete, onAlerts }: VehicleCardProps) => {
  const alertCount = vehicle.alerts?.length || 0;
  const badgeClass = getAlertBadgeClass(alertCount);
  const badgeIcon = getAlertIcon(alertCount);

  return (
    <div className="vehicle-card">
      <div className="vehicle-header">
        <div>
          <div className="vehicle-id">{vehicle.id}</div>
          <div className="vehicle-plate">{vehicle.plate}</div>
        </div>
        <span className={`badge ${badgeClass}`} onClick={() => onAlerts(vehicle.id)}>
          {badgeIcon} {alertCount} {alertCount === 1 ? 'alerta' : 'alertas'}
        </span>
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
        <button className="btn btn-small btn-primary" onClick={() => onUpdate(vehicle.id)}>
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
