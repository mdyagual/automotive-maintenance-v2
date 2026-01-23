import { useState } from 'react';
import { Header } from './components/Header';
import { Stats } from './components/Stats';
import { StatusFilter } from './components/StatusFilter';
import { VehicleGrid } from './components/VehicleGrid';
import { Pagination } from './components/Pagination';
import { Toast } from './components/Toast';
import { CreateVehicleModal } from './components/modals/CreateVehicleModal';
import { DetailsModal } from './components/modals/DetailsModal';
import { UpdateMileageModal } from './components/modals/UpdateMileageModal';
import { UpdateStatusModal } from './components/modals/UpdateStatusModal';
import { AlertsModal } from './components/modals/AlertsModal';
import { DeleteModal } from './components/modals/DeleteModal';
import { useVehicles } from './hooks/useVehicles';
import { useToast } from './hooks/useToast';
import { usePagination } from './hooks/usePagination';
import type { Vehicle, CreateVehicleRequest, VehicleStatus } from './types/vehicle';
import './App.css';

function App() {
  const {
    vehicles,
    loading,
    error,
    statusFilter,
    setStatusFilter,
    createVehicle,
    updateMileage,
    updateStatus,
    deleteVehicle,
  } = useVehicles();
  const { toasts, showToast } = useToast();

  // Pagination: 8 vehicles per page
  const ITEMS_PER_PAGE = 8;
  const {
    currentPage,
    totalPages,
    paginatedItems: paginatedVehicles,
    goToPage,
  } = usePagination(vehicles, ITEMS_PER_PAGE);

  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isDetailsModalOpen, setIsDetailsModalOpen] = useState(false);
  const [isUpdateModalOpen, setIsUpdateModalOpen] = useState(false);
  const [isUpdateStatusModalOpen, setIsUpdateStatusModalOpen] = useState(false);
  const [isAlertsModalOpen, setIsAlertsModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [selectedVehicle, setSelectedVehicle] = useState<Vehicle | null>(null);

  const handleCreateVehicle = async (data: CreateVehicleRequest) => {
    try {
      await createVehicle(data);
      showToast('Vehículo registrado exitosamente', 'success');
    } catch (err) {
      showToast(
        `Error al registrar vehículo: ${err instanceof Error ? err.message : 'Error desconocido'}`,
        'error'
      );
    }
  };

  const handleUpdateMileage = async (vehicleId: string, newMileage: number) => {
    try {
      await updateMileage(vehicleId, { new_mileage: newMileage });
      showToast('Kilometraje actualizado exitosamente', 'success');
    } catch (err) {
      showToast(
        `Error al actualizar kilometraje: ${err instanceof Error ? err.message : 'Error desconocido'}`,
        'error'
      );
    }
  };

  const handleUpdateStatus = async (vehicleId: string, newStatus: VehicleStatus) => {
    try {
      await updateStatus(vehicleId, { new_status: newStatus });
      showToast('Estado actualizado exitosamente', 'success');
    } catch (err) {
      showToast(
        `Error al actualizar estado: ${err instanceof Error ? err.message : 'Error desconocido'}`,
        'error'
      );
    }
  };

  const handleDeleteVehicle = async (vehicleId: string) => {
    try {
      await deleteVehicle(vehicleId);
      showToast('Vehículo eliminado exitosamente', 'success');
    } catch (err) {
      showToast(
        `Error al eliminar vehículo: ${err instanceof Error ? err.message : 'Error desconocido'}`,
        'error'
      );
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
      if (vehicle.status === 'retired') {
        showToast('No se puede actualizar el kilometraje de vehículos retirados', 'warning');
        return;
      }
      setSelectedVehicle(vehicle);
      setIsUpdateModalOpen(true);
    }
  };

  const openUpdateStatusModal = (vehicleId: string) => {
    const vehicle = vehicles.find((v) => v.id === vehicleId);
    if (vehicle) {
      setSelectedVehicle(vehicle);
      setIsUpdateStatusModalOpen(true);
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
            <div className="section-header">
              <h2 className="section-title">Listado de Vehículos</h2>
              <StatusFilter currentFilter={statusFilter} onFilterChange={setStatusFilter} />
            </div>

            <VehicleGrid
              vehicles={paginatedVehicles}
              onUpdate={openUpdateModal}
              onDetails={openDetailsModal}
              onDelete={openDeleteModal}
              onUpdateStatus={openUpdateStatusModal}
              onNewVehicle={() => setIsCreateModalOpen(true)}
            />

            {totalPages > 0 && (
              <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={goToPage}
              />
            )}
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

      <UpdateStatusModal
        isOpen={isUpdateStatusModalOpen}
        onClose={() => setIsUpdateStatusModalOpen(false)}
        vehicle={selectedVehicle}
        onSubmit={handleUpdateStatus}
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

      <Toast toasts={toasts} />
    </>
  );
}

export default App;
