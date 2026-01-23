import { Modal } from '../Modal';
import type { Vehicle } from '../../types/vehicle';
import { formatNumber } from '../../utils/formatters';

interface DetailsModalProps {
  isOpen: boolean;
  onClose: () => void;
  vehicle: Vehicle | null;
}

const formatAlertType = (type: string): string => {
  const types: Record<string, string> = {
    BASIC: 'Mantenimiento Básico',
    MAJOR: 'Mantenimiento Mayor',
    CRITICAL: 'Mantenimiento Crítico',
  };
  return types[type] || type;
};

const formatDate = (timestamp: string): string => {
  const date = new Date(timestamp);
  return date.toLocaleDateString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

const getAlertTypeClass = (type: string): string => {
  const classes: Record<string, string> = {
    BASIC: 'alert-type-basic',
    MAJOR: 'alert-type-major',
    CRITICAL: 'alert-type-critical',
  };
  return classes[type] || 'alert-type-basic';
};

export const DetailsModal = ({ isOpen, onClose, vehicle }: DetailsModalProps) => {
  if (!vehicle) return null;

  const hasAlerts = vehicle.alerts && vehicle.alerts.length > 0;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Detalles del Vehículo"
      size="wide"
      footer={
        <button type="button" className="btn btn-secondary" onClick={onClose}>
          Cerrar
        </button>
      }
    >
      <div className="details-container">
        <div className="details-grid">
          <div className="detail-item">
            <span className="detail-label">ID:</span>
            <span className="detail-value">{vehicle.id}</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Placa:</span>
            <span className="detail-value">{vehicle.plate}</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Modelo:</span>
            <span className="detail-value">{vehicle.model}</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Kilometraje:</span>
            <span className="detail-value">{formatNumber(vehicle.current_mileage)} km</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Estado:</span>
            <span className="detail-value">{vehicle.status}</span>
          </div>
        </div>

        <div className="alerts-section">
          <h3 className="alerts-title">
            <span className="material-symbols-outlined">notifications</span>
            Alertas de Mantenimiento
          </h3>

          {hasAlerts ? (
            <div className="alerts-list">
              {vehicle.alerts.map((alert) => (
                <div
                  key={alert.id}
                  className={`alert-item ${getAlertTypeClass(alert.alert_type)}`}
                  data-testid={`alert-item-${alert.id}`}
                >
                  <div className="alert-header">
                    <span className="alert-type-badge">{formatAlertType(alert.alert_type)}</span>
                    <span className="alert-date">{formatDate(alert.timestamp)}</span>
                  </div>
                  <div className="alert-body">
                    <div className="alert-info">
                      <span className="material-symbols-outlined">speed</span>
                      <span className="alert-mileage">{formatNumber(alert.mileage)} km</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="alerts-empty">
              <span className="material-symbols-outlined">check_circle</span>
              <p>No hay alertas registradas para este vehículo</p>
            </div>
          )}
        </div>
      </div>
    </Modal>
  );
};
