import type { Vehicle } from '../types/vehicle';

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
        <div className="stat-icon-wrapper">
          <span className="material-symbols-outlined">local_shipping</span>
        </div>
        <div className="stat-content">
          <div className="stat-label">Total Flota</div>
          <div className="stat-value">{totalVehicles}</div>
        </div>
      </div>
      <div className="stat-card">
        <div className="stat-icon-wrapper">
          <span className="material-symbols-outlined">verified</span>
        </div>
        <div className="stat-content">
          <div className="stat-label">En Ruta</div>
          <div className="stat-value">{activeVehicles}</div>
        </div>
      </div>
      <div className="stat-card">
        <div className="stat-icon-wrapper">
          <span className="material-symbols-outlined">build_circle</span>
        </div>
        <div className="stat-content">
          <div className="stat-label">En Taller</div>
          <div className="stat-value">{inMaintenanceVehicles}</div>
        </div>
      </div>
      <div className="stat-card">
        <div className="stat-icon-wrapper">
          <span className="material-symbols-outlined">error</span>
        </div>
        <div className="stat-content">
          <div className="stat-label">Alertas</div>
          <div className="stat-value">{totalAlerts}</div>
        </div>
      </div>
    </section>
  );
};
