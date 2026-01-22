import type { Vehicle, VehicleStatus } from '../types/vehicle';

interface StatsProps {
  vehicles: Vehicle[];
}

export const Stats = ({ vehicles }: StatsProps) => {
  const totalVehicles = vehicles.length;
  const totalAlerts = vehicles.reduce((sum, v) => sum + (v.alerts?.length || 0), 0);
  
  // HU-005: Count vehicles by status
  const activeVehicles = vehicles.filter(v => v.status === 'active').length;
  const inMaintenanceVehicles = vehicles.filter(v => v.status === 'in_maintenance').length;

  return (
    <section className="stats-section">
      <div className="stat-card">
        <h3 className="stat-value">{totalVehicles}</h3>
        <p className="stat-label">Vehículos Registrados</p>
      </div>
      <div className="stat-card">
        <h3 className="stat-value stat-success">{activeVehicles}</h3>
        <p className="stat-label">Vehículos Activos</p>
      </div>
      <div className="stat-card">
        <h3 className="stat-value stat-warning">{inMaintenanceVehicles}</h3>
        <p className="stat-label">En Mantenimiento</p>
      </div>
      <div className="stat-card">
        <h3 className="stat-value stat-error">{totalAlerts}</h3>
        <p className="stat-label">Alertas Activas</p>
      </div>
    </section>
  );
};
