interface HeaderProps {
  onNewVehicle: () => void;
}

export const Header = ({ onNewVehicle }: HeaderProps) => {
  return (
    <header className="header">
      <div className="container">
        <h1 className="header-title">🚗 Sistema de Gestión de Flota Vehicular</h1>
        <button className="btn btn-primary" onClick={onNewVehicle}>
          <span className="btn-icon">+</span>
          Registrar Vehículo
        </button>
      </div>
    </header>
  );
};
