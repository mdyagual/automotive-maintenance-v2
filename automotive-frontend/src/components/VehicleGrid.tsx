import type { Vehicle } from '../types/vehicle';
import { VehicleCard } from './VehicleCard';

interface VehicleGridProps {
  vehicles: Vehicle[];
  onUpdate: (vehicleId: string) => void;
  onDetails: (vehicleId: string) => void;
  onDelete: (vehicleId: string) => void;
  onUpdateStatus: (vehicleId: string) => void;
  onNewVehicle: () => void;
}

export const VehicleGrid = ({
  vehicles,
  onUpdate,
  onDetails,
  onDelete,
  onUpdateStatus,
  onNewVehicle,
}: VehicleGridProps) => {
  if (vehicles.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-icon">📋</div>
        <h3>No hay vehículos registrados</h3>
        <p>Comienza registrando tu primer vehículo</p>
        <button className="btn btn-primary" onClick={onNewVehicle}>
          Registrar Vehículo
        </button>
      </div>
    );
  }

  return (
    <div className="vehicles-grid">
      {vehicles.map((vehicle) => (
        <VehicleCard
          key={vehicle.id}
          vehicle={vehicle}
          onUpdate={onUpdate}
          onDetails={onDetails}
          onDelete={onDelete}
          onUpdateStatus={onUpdateStatus}
        />
      ))}
    </div>
  );
};
