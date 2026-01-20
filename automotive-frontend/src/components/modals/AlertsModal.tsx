import { Modal } from '../Modal';
import type { Vehicle } from '../../types/vehicle';
import { formatNumber, formatDate, getAlertTypeText, getAlertItemClass, getAlertItemIcon } from '../../utils/formatters';

interface AlertsModalProps {
  isOpen: boolean;
  onClose: () => void;
  vehicle: Vehicle | null;
}

export const AlertsModal = ({ isOpen, onClose, vehicle }: AlertsModalProps) => {
  if (!vehicle) return null;

  const hasAlerts = vehicle.alerts && vehicle.alerts.length > 0;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Alertas de Mantenimiento"
      size="wide"
      footer={
        <button type="button" className="btn btn-secondary" onClick={onClose}>
          Cerrar
        </button>
      }
    >
      <div className="info-box">
        <p>
          <strong>Vehículo:</strong> {vehicle.plate} - {vehicle.model}
        </p>
      </div>
      {!hasAlerts ? (
        <div className="no-alerts">
          <div className="no-alerts-icon">✅</div>
          <p>No hay alertas de mantenimiento para este vehículo</p>
        </div>
      ) : (
        <div className="alerts-list">
          {vehicle.alerts.map((alert) => (
            <div key={alert.id} className={`alert-item ${getAlertItemClass(alert.alert_type)}`}>
              <div className="alert-icon">{getAlertItemIcon(alert.alert_type)}</div>
              <div className="alert-content">
                <div className="alert-type">{getAlertTypeText(alert.alert_type)}</div>
                <div className="alert-mileage">Generada a los {formatNumber(alert.mileage)} km</div>
                <div className="alert-timestamp">{formatDate(alert.timestamp)}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </Modal>
  );
};
