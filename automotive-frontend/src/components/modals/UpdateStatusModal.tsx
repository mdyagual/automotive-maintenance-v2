import { useState } from 'react';
import { Modal } from '../Modal';
import type { Vehicle, VehicleStatus } from '../../types/vehicle';
import { getStatusText } from '../../utils/formatters';

interface UpdateStatusModalProps {
  isOpen: boolean;
  onClose: () => void;
  vehicle: Vehicle | null;
  onSubmit: (vehicleId: string, newStatus: VehicleStatus) => Promise<void>;
}

export const UpdateStatusModal = ({ isOpen, onClose, vehicle, onSubmit }: UpdateStatusModalProps) => {
  const [selectedStatus, setSelectedStatus] = useState<VehicleStatus>('active');
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!vehicle) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (selectedStatus === vehicle.status) {
      onClose();
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit(vehicle.id, selectedStatus);
      onClose();
    } catch (error) {
      // Error handling is done in parent component
    } finally {
      setIsSubmitting(false);
    }
  };

  const statusOptions: VehicleStatus[] = ['active', 'inactive', 'in_maintenance', 'retired'];

  const footer = (
    <>
      <button type="button" className="btn btn-secondary" onClick={onClose} disabled={isSubmitting}>
        Cancelar
      </button>
      <button type="submit" form="update-status-form" className="btn btn-primary" disabled={isSubmitting}>
        {isSubmitting ? 'Actualizando...' : 'Actualizar Estado'}
      </button>
    </>
  );

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Actualizar Estado del Vehículo" footer={footer}>
      <form id="update-status-form" onSubmit={handleSubmit}>
        <div className="info-box">
          <p><strong>Vehículo:</strong> {vehicle.plate} - {vehicle.model}</p>
          <p><strong>Estado actual:</strong> {getStatusText(vehicle.status)}</p>
        </div>

        <div className="form-group">
          <label className="form-label">Nuevo Estado</label>
          <select
            className="form-input"
            value={selectedStatus}
            onChange={(e) => setSelectedStatus(e.target.value as VehicleStatus)}
            required
          >
            {statusOptions.map((status) => (
              <option key={status} value={status}>
                {getStatusText(status)}
              </option>
            ))}
          </select>
          <span className="form-hint">
            Selecciona el nuevo estado operativo del vehículo
          </span>
        </div>

        <div className="status-descriptions">
          <div className="status-description">
            <strong>✓ Activo:</strong> Vehículo disponible para operaciones normales
          </div>
          <div className="status-description">
            <strong>⏸ Inactivo:</strong> Vehículo temporalmente fuera de servicio
          </div>
          <div className="status-description">
            <strong>🔧 En Mantenimiento:</strong> Vehículo en proceso de mantenimiento
          </div>
          <div className="status-description">
            <strong>🚫 Retirado:</strong> Vehículo permanentemente fuera de servicio (no se puede actualizar kilometraje)
          </div>
        </div>
      </form>
    </Modal>
  );
};
