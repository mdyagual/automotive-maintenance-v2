"""SQLite implementation of AlertRepository - Infrastructure layer."""

from sqlalchemy.orm import Session

from src.domain.entities.maintenance_alert import MaintenanceAlert
from src.domain.ports.alert_repository import AlertRepository
from src.infrastructure.database.models import AlertModel


class SqliteAlertRepository(AlertRepository):
    """SQLite implementation of AlertRepository using SQLAlchemy."""

    def __init__(self, db_session: Session) -> None:
        """
        Initialize repository with database session.

        Args:
            db_session: SQLAlchemy database session
        """
        self._db = db_session

    def _to_entity(self, alert_model: AlertModel) -> MaintenanceAlert:
        """
        Convert AlertModel to MaintenanceAlert entity.

        Args:
            alert_model: SQLAlchemy model instance

        Returns:
            MaintenanceAlert domain entity
        """
        return MaintenanceAlert(
            id=alert_model.id,
            vehicle_id=alert_model.vehicle_id,
            alert_type=alert_model.alert_type,
            mileage=alert_model.mileage,
            timestamp=alert_model.timestamp,
        )

    def _to_model(self, alert: MaintenanceAlert) -> AlertModel:
        """
        Convert MaintenanceAlert entity to AlertModel.

        Args:
            alert: MaintenanceAlert domain entity

        Returns:
            AlertModel instance for persistence
        """
        return AlertModel(
            id=alert.id,
            vehicle_id=alert.vehicle_id,
            alert_type=alert.alert_type,
            mileage=alert.mileage,
            timestamp=alert.timestamp,
        )

    def _to_entities(self, alert_models: list[AlertModel]) -> list[MaintenanceAlert]:
        """
        Convert list of AlertModel to list of MaintenanceAlert entities.

        Args:
            alert_models: List of SQLAlchemy model instances

        Returns:
            List of MaintenanceAlert domain entities
        """
        return [self._to_entity(model) for model in alert_models]

    def save(self, alert: MaintenanceAlert) -> None:
        """
        Save alert to SQLite database.

        Args:
            alert: MaintenanceAlert entity to save
        """
        alert_model = self._to_model(alert)
        self._db.merge(alert_model)
        self._db.commit()

    def get_all(self) -> list[MaintenanceAlert]:
        """
        Get all alerts from database ordered by timestamp descending.

        Returns:
            List of all MaintenanceAlert entities (most recent first)
        """
        alert_models = self._db.query(AlertModel)\
            .order_by(AlertModel.timestamp.desc())\
            .all()
        return self._to_entities(alert_models)

    def get_by_vehicle_id(self, vehicle_id: str) -> list[MaintenanceAlert]:
        """
        Get all alerts for a specific vehicle ordered by timestamp descending.

        Args:
            vehicle_id: Unique identifier of the vehicle

        Returns:
            List of MaintenanceAlert entities for the vehicle (most recent first)
        """
        alert_models = self._db.query(AlertModel)\
            .filter_by(vehicle_id=vehicle_id)\
            .order_by(AlertModel.timestamp.desc())\
            .all()
        return self._to_entities(alert_models)
