"""SQLAlchemy models for database persistence."""

from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.domain.entities.maintenance_alert import AlertType


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


class VehicleModel(Base):
    """SQLAlchemy model for Vehicle entity."""

    __tablename__ = "vehicles"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    plate: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    current_mileage: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationship to alerts
    alerts: Mapped[list["AlertModel"]] = relationship(
        "AlertModel", back_populates="vehicle", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """String representation of VehicleModel."""
        return f"<VehicleModel(id={self.id}, plate={self.plate}, mileage={self.current_mileage})>"


class AlertModel(Base):
    """SQLAlchemy model for MaintenanceAlert entity."""

    __tablename__ = "alerts"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    vehicle_id: Mapped[str] = mapped_column(
        String(50), ForeignKey("vehicles.id"), nullable=False
    )
    alert_type: Mapped[AlertType] = mapped_column(
        Enum(AlertType), nullable=False
    )
    mileage: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Relationship to vehicle
    vehicle: Mapped["VehicleModel"] = relationship("VehicleModel", back_populates="alerts")

    def __repr__(self) -> str:
        """String representation of AlertModel."""
        return (
            f"<AlertModel(id={self.id}, vehicle_id={self.vehicle_id}, "
            f"type={self.alert_type.value})>"
        )
