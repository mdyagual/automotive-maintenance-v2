interface HeaderProps {
  onNewVehicle: () => void;
}

export const Header = ({ onNewVehicle }: HeaderProps) => {
  return (
    <header className="header">
      <div className="container">
        <div className="header-logo">
          <div className="header-icon">
            <span className="material-symbols-outlined header-icon-text">local_taxi</span>
          </div>
          <div className="header-title-wrapper">
            <h1 className="header-title">
              Sistema <span className="header-title-accent">Gestor</span> de Flota
            </h1>
            <p className="header-subtitle">Dashboard</p>
          </div>
        </div>
        <div className="header-actions">
          <div className="header-search">
            <input className="header-search-input" placeholder="Buscar vehículo..." type="text" />
            <span className="material-symbols-outlined header-search-icon">search</span>
          </div>
          <button className="btn btn-primary" onClick={onNewVehicle}>
            <span className="material-symbols-outlined btn-icon">add</span>
            <span className="hidden sm:inline">Nuevo Vehículo</span>
          </button>
        </div>
      </div>
    </header>
  );
};
