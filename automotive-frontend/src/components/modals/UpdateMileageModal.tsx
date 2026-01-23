import { useState, FormEvent, useEffect } from 'react';
import { Modal } from '../Modal';
import type { Vehicle } from '../../types/vehicle';
import { formatNumber } from '../../utils/formatters';

interface UpdateMileageModalProps {
  isOpen: boolean;
  onClose: () => void;
  vehicle: Vehicle | null;
  onSubmit: (vehicleId: string, newMileage: number) => Promise<void>;
}

export const UpdateMileageModal = ({
  isOpen,
  onClose,
  vehicle,
  onSubmit,
}: UpdateMileageModalProps) => {
  const [newMileage, setNewMileage] = useState<number>(0);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    if (vehicle) {
      setNewMileage(0);
      setError('');
    }
  }, [vehicle]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!vehicle) return;

    if (newMileage <= vehicle.current_mileage) {
      setError('El nuevo kilometraje debe ser mayor al actual');
      return;
    }

    await onSubmit(vehicle.id, newMileage);
    setNewMileage(0);
    setError('');
    onClose();
  };

  const handleClose = () => {
    setNewMileage(0);
    setError('');
    onClose();
  };

  if (!vehicle) return null;

  return (
    <Modal
      isOpen={isOpen}
      onClose={handleClose}
      title="Actualizar Kilometraje"
      footer={
        <>
          <button type="button" className="btn btn-secondary" onClick={handleClose}>
            Cancelar
          </button>
          <button type="submit" form="updateForm" className="btn btn-primary">
            Actualizar
          </button>
        </>
      }
    >
      <form id="updateForm" onSubmit={handleSubmit}>
        <div className="info-box">
          <p>
            <strong>Vehículo:</strong> {vehicle.plate} - {vehicle.model}
          </p>
          <p>
            <strong>Kilometraje actual:</strong> {formatNumber(vehicle.current_mileage)} km
          </p>
        </div>
        <div className="form-group">
          <label htmlFor="updateNewMileage" className="form-label">
            Nuevo Kilometraje
          </label>
          <input
            type="number"
            id="updateNewMileage"
            className="form-input"
            placeholder="0"
            required
            min={vehicle.current_mileage + 1}
            max="1000000"
            value={newMileage || ''}
            onChange={(e) => {
              setNewMileage(parseInt(e.target.value) || 0);
              setError('');
            }}
          />
          <small className="form-hint">
            Debe ser mayor a {formatNumber(vehicle.current_mileage)} km
          </small>
          {error && (
            <small className="form-hint" style={{ color: 'var(--error-600)' }}>
              {error}
            </small>
          )}
        </div>
      </form>
    </Modal>
  );
};
