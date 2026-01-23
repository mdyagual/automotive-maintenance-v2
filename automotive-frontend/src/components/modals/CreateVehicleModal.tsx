import { useState, FormEvent } from 'react';
import { Modal } from '../Modal';
import type { CreateVehicleRequest } from '../../types/vehicle';

interface CreateVehicleModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: CreateVehicleRequest) => Promise<void>;
}

export const CreateVehicleModal = ({ isOpen, onClose, onSubmit }: CreateVehicleModalProps) => {
  const [formData, setFormData] = useState<CreateVehicleRequest>({
    id: '',
    plate: '',
    model: '',
    initial_mileage: 0,
  });

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    await onSubmit({
      ...formData,
      plate: formData.plate.toUpperCase(),
    });
    setFormData({ id: '', plate: '', model: '', initial_mileage: 0 });
    onClose();
  };

  const handleClose = () => {
    setFormData({ id: '', plate: '', model: '', initial_mileage: 0 });
    onClose();
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={handleClose}
      title="Registrar Nuevo Vehículo"
      footer={
        <>
          <button type="button" className="btn btn-secondary" onClick={handleClose}>
            Cancelar
          </button>
          <button type="submit" form="createForm" className="btn btn-primary">
            Registrar
          </button>
        </>
      }
    >
      <form id="createForm" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="createId" className="form-label">
            ID del Vehículo
          </label>
          <input
            type="text"
            id="createId"
            className="form-input"
            placeholder="V-001"
            required
            pattern="V-\d{3}"
            value={formData.id}
            onChange={(e) => setFormData({ ...formData, id: e.target.value })}
          />
          <small className="form-hint">Formato: V-XXX (ejemplo: V-001)</small>
        </div>
        <div className="form-group">
          <label htmlFor="createPlate" className="form-label">
            Placa
          </label>
          <input
            type="text"
            id="createPlate"
            className="form-input"
            placeholder="ABC-123"
            required
            pattern="[A-Z]{3}-\d{3,4}"
            value={formData.plate}
            onChange={(e) => setFormData({ ...formData, plate: e.target.value.toUpperCase() })}
          />
          <small className="form-hint">Formato: XXX-123 o XXX-1234</small>
        </div>
        <div className="form-group">
          <label htmlFor="createModel" className="form-label">
            Modelo
          </label>
          <input
            type="text"
            id="createModel"
            className="form-input"
            placeholder="Toyota Corolla 2020"
            required
            value={formData.model}
            onChange={(e) => setFormData({ ...formData, model: e.target.value })}
          />
        </div>
        <div className="form-group">
          <label htmlFor="createMileage" className="form-label">
            Kilometraje Inicial
          </label>
          <input
            type="number"
            id="createMileage"
            className="form-input"
            placeholder="0"
            required
            min="0"
            max="1000000"
            value={formData.initial_mileage}
            onChange={(e) =>
              setFormData({ ...formData, initial_mileage: parseInt(e.target.value) || 0 })
            }
          />
          <small className="form-hint">Rango: 0 - 1,000,000 km</small>
        </div>
      </form>
    </Modal>
  );
};
