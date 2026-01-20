import { useState } from 'react';
import { Header } from './components/Header';
import { Stats } from './components/Stats';
import { VehicleGrid } from './components/VehicleGrid';
import { Toast } from './components/Toast';
import { CreateVehicleModal } from './components/modals/CreateVehicleModal';
import { DetailsModal } from './components/modals/DetailsModal';
import { UpdateMileageModal } from './components/modals/UpdateMileageModal';
import { AlertsModal } from './components/modals/AlertsModal';
import { DeleteModal } from './components/modals/DeleteModal';
import { useVehicles } from './hooks/useVehicles';
import { useToast } from './hooks/useToast';
import type { Vehicle, CreateVehicleRequest } from './types/vehicle';
import './App.css';

function App() {
  const { vehicles, loading, error, createVehicle, updateMileage, deleteVehicle } = useVehicles();
  const { toasts, showToast } = useToast();

  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isDetailsModalOpen, setIsDetailsModalOpen] = useState(false);
  const [isUpdateModalOpen, setIsUpdateModalOpen] = useState(false);
  const [isAlertsModalOpen, setIsAlertsModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [selectedVehicle, setSelectedVehicle] = useState<Vehicle | null>(null);

  const handleCreateVehicle = async (data: CreateVehicleRequest) => {
    try {
      await createVehicle(data);
      showToast('Vehículo registrado exitosamente', 'success');
    } catch (err) {
      showToast(`Error al registrar vehículo: ${err instanceof Error ? err.message : 'Error desconocido'}`, 'error');
    }
  };

  const handleUpdateMileage = async (vehicleId: string, newMileage: number) => {
    try {
      await updateMileage(vehicleId, { new_mileage: newMileage });
      showToast('Kilometraje actualizado exitosamente', 'success');
    } catch (err) {
      showToast(`Error al actualizar kilometraje: ${err instanceof Error ? err.message : 'Error desconocido'}`, 'error');
    }
  };

  const handleDeleteVehicle = async (vehicleId: string) => {
    try {
      await deleteVehicle(vehicleId);
      showToast('Vehículo eliminado exitosamente', 'success');
    } catch (err) {
      showToast(`Error al eliminar vehículo: ${err instanceof Error ? err.message : 'Error desconocido'}`, 'error');
    }
  };

  const openDetailsModal = (vehicleId: string) => {
    const vehicle = vehicles.find((v) => v.id === vehicleId);
    if (vehicle) {
      setSelectedVehicle(vehicle);
      setIsDetailsModalOpen(true);
    }
  };

  const openUpdateModal = (vehicleId: string) => {
    const vehicle = vehicles.find((v) => v.id === vehicleId);
    if (vehicle) {
      setSelectedVehicle(vehicle);
      setIsUpdateModalOpen(true);
    }
  };

  const openAlertsModal = (vehicleId: string) => {
    const vehicle = vehicles.find((v) => v.id === vehicleId);
    if (vehicle) {
      setSelectedVehicle(vehicle);
      setIsAlertsModalOpen(true);
    }
  };

  const openDeleteModal = (vehicleId: string) => {
    const vehicle = vehicles.find((v) => v.id === vehicleId);
    if (vehicle) {
      setSelectedVehicle(vehicle);
      setIsDeleteModalOpen(true);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner">Cargando...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error-message">Error: {error}</div>
      </div>
    );
  }

  return (
    <>
      <Header onNewVehicle={() => setIsCreateModalOpen(true)} />
      <main className="main-content">
        <div className="container">
          <Stats vehicles={vehicles} />
          <section className="vehicles-section">
            <h2 className="section-title">Vehículos</h2>
            <VehicleGrid
              vehicles={vehicles}
              onUpdate={openUpdateModal}
              onDetails={openDetailsModal}
              onDelete={openDeleteModal}
              onAlerts={openAlertsModal}
              onNewVehicle={() => setIsCreateModalOpen(true)}
            />
          </section>
        </div>
      </main>

      <CreateVehicleModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onSubmit={handleCreateVehicle}
      />

      <DetailsModal
        isOpen={isDetailsModalOpen}
        onClose={() => setIsDetailsModalOpen(false)}
        vehicle={selectedVehicle}
      />

      <UpdateMileageModal
        isOpen={isUpdateModalOpen}
        onClose={() => setIsUpdateModalOpen(false)}
        vehicle={selectedVehicle}
        onSubmit={handleUpdateMileage}
      />

      <AlertsModal
        isOpen={isAlertsModalOpen}
        onClose={() => setIsAlertsModalOpen(false)}
        vehicle={selectedVehicle}
      />

      <DeleteModal
        isOpen={isDeleteModalOpen}
        onClose={() => setIsDeleteModalOpen(false)}
        vehicle={selectedVehicle}
        onConfirm={handleDeleteVehicle}
      />

      <Toast toasts={toasts} onRemove={() => {}} />
    </>
  );
}

export default App;
