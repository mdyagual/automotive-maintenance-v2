import type { Vehicle } from '../types/vehicle';
import {
  formatNumber,
  getAlertBadgeClass,
  getAlertIcon,
  getStatusText,
  getStatusBadgeClass,
  getStatusIcon,
} from '../utils/formatters';

interface VehicleCardProps {
  vehicle: Vehicle;
  onUpdate: (vehicleId: string) => void;
  onDetails: (vehicleId: string) => void;
  onDelete: (vehicleId: string) => void;
  onAlerts: (vehicleId: string) => void;
  onUpdateStatus: (vehicleId: string) => void;
}

export const VehicleCard = ({
  vehicle,
  onUpdate,
  onDetails,
  onDelete,
  onAlerts,
  onUpdateStatus,
}: VehicleCardProps) => {
  const alertCount = vehicle.alerts?.length || 0;
  const badgeClass = getAlertBadgeClass(alertCount);
  const badgeIcon = getAlertIcon(alertCount);
  const statusBadgeClass = getStatusBadgeClass(vehicle.status);
  const statusIcon = getStatusIcon(vehicle.status);
  const statusText = getStatusText(vehicle.status);
  const isRetired = vehicle.status === 'retired';
  const hasAlert = alertCount > 0;

  return (
    <div className={`vehicle-card ${hasAlert ? 'has-alert' : ''}`}>
      <div className="vehicle-header">
        <div className="vehicle-info">
          <div className="vehicle-id">ID: {vehicle.id}</div>
          <h3 className="vehicle-plate">{vehicle.plate}</h3>
          <p className="vehicle-model">{vehicle.model}</p>
        </div>
        <div className="vehicle-badges">
          <span
            className={`status-badge ${statusBadgeClass}`}
            onClick={() => onUpdateStatus(vehicle.id)}
          >
            {statusText}
          </span>
        </div>
      </div>

      <div className="vehicle-mileage">
        <span className="mileage-value">{formatNumber(vehicle.current_mileage)}</span>
        <span className="mileage-label">Kilómetros totales</span>
      </div>

      <div className="vehicle-actions">
        <button className="btn btn-small btn-secondary" onClick={() => onDetails(vehicle.id)}>
          <span className="material-symbols-outlined btn-icon">visibility</span> Detalles
        </button>
        <button className="btn btn-small btn-danger" onClick={() => onDelete(vehicle.id)}>
          <span className="material-symbols-outlined btn-icon">delete</span> Eliminar
        </button>
        <button
          className="btn btn-small btn-primary btn-update-km"
          onClick={() => onUpdate(vehicle.id)}
          disabled={isRetired}
          title={
            isRetired
              ? 'No se puede actualizar kilometraje de vehículos retirados'
              : 'Actualizar kilometraje'
          }
        >
          <span className="material-symbols-outlined btn-icon">speed</span> Actualizar KM
        </button>
      </div>
    </div>
  );
};
