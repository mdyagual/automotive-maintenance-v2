import { Modal } from '../Modal';
import type { Vehicle } from '../../types/vehicle';
import { formatNumber } from '../../utils/formatters';

interface DetailsModalProps {
  isOpen: boolean;
  onClose: () => void;
  vehicle: Vehicle | null;
}

export const DetailsModal = ({ isOpen, onClose, vehicle }: DetailsModalProps) => {
  if (!vehicle) return null;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Detalles del Vehículo"
      footer={
        <button type="button" className="btn btn-secondary" onClick={onClose}>
          Cerrar
        </button>
      }
    >
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
      </div>
    </Modal>
  );
};
