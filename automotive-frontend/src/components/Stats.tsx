import type { Vehicle } from '../types/vehicle';

interface StatsProps {
  vehicles: Vehicle[];
}

export const Stats = ({ vehicles }: StatsProps) => {
  const totalVehicles = vehicles.length;
  const totalAlerts = vehicles.reduce((sum, v) => sum + (v.alerts?.length || 0), 0);

  return (
    <section className="stats-section">
      <div className="stat-card">
        <h3 className="stat-value">{totalVehicles}</h3>
        <p className="stat-label">Vehículos Registrados</p>
      </div>
      <div className="stat-card">
        <h3 className="stat-value stat-warning">{totalAlerts}</h3>
        <p className="stat-label">Alertas Activas</p>
      </div>
    </section>
  );
};
