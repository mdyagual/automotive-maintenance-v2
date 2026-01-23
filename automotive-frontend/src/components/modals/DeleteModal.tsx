import { Modal } from '../Modal';
import type { Vehicle } from '../../types/vehicle';

interface DeleteModalProps {
  isOpen: boolean;
  onClose: () => void;
  vehicle: Vehicle | null;
  onConfirm: (vehicleId: string) => Promise<void>;
}

export const DeleteModal = ({ isOpen, onClose, vehicle, onConfirm }: DeleteModalProps) => {
  if (!vehicle) return null;

  const handleConfirm = async () => {
    await onConfirm(vehicle.id);
    onClose();
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Confirmar Eliminación"
      size="small"
      footer={
        <>
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            Cancelar
          </button>
          <button type="button" className="btn btn-danger" onClick={handleConfirm}>
            Eliminar
          </button>
        </>
      }
    >
      <div className="warning-box">
        <div className="warning-icon">⚠️</div>
        <p>¿Está seguro que desea eliminar este vehículo?</p>
        <p>
          <strong>
            {vehicle.plate} - {vehicle.model}
          </strong>
        </p>
        <p className="text-small">
          Esta acción eliminará el vehículo y todas sus alertas asociadas. No se puede deshacer.
        </p>
      </div>
    </Modal>
  );
};
