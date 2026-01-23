"""FastAPI application - Web layer."""

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field

from src.application.dtos.vehicle_dtos import (
    DeleteVehicleCommand,
    RegisterVehicleCommand,
    UpdateMileageCommand,
)
from src.application.use_cases.delete_vehicle_use_case import DeleteVehicleUseCase
from src.application.use_cases.get_all_vehicles_use_case import GetAllVehiclesUseCase
from src.application.use_cases.get_vehicle_alerts_use_case import GetVehicleAlertsUseCase
from src.application.use_cases.get_vehicle_use_case import GetVehicleUseCase
from src.application.use_cases.register_vehicle_use_case import RegisterVehicleUseCase
from src.application.use_cases.update_vehicle_mileage_use_case import (
    UpdateVehicleMileageUseCase,
)
from src.domain.entities.maintenance_alert import MaintenanceAlert
from src.domain.exceptions.duplicate_vehicle_exception import DuplicateVehicleException
from src.domain.exceptions.invalid_mileage_exception import InvalidMileageException
from src.domain.exceptions.vehicle_not_found_exception import (
    VehicleNotFoundException,
)
from src.infrastructure.factories.observer_factory_impl import ObserverFactoryImpl
from src.infrastructure.repositories.sqlite_alert_repository import SqliteAlertRepository
from src.infrastructure.repositories.sqlite_vehicle_repository import SqliteVehicleRepository
from src.web.dependencies import (
    get_alert_repository,
    get_observer_factory,
    get_vehicle_repository,
)


# DTOs
class CreateVehicleRequest(BaseModel):
    """Request model for creating a new vehicle."""

    id: str = Field(..., description="Unique vehicle identifier")
    plate: str = Field(..., description="License plate number")
    model: str = Field(..., description="Vehicle model")
    initial_mileage: int = Field(..., description="Initial mileage value", ge=0)


class UpdateMileageRequest(BaseModel):
    """Request model for updating vehicle mileage."""

    new_mileage: int = Field(..., description="New mileage value", ge=0)


class VehicleResponse(BaseModel):
    """Response model for vehicle data."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    plate: str
    model: str
    current_mileage: int
    status: str


class AlertResponse(BaseModel):
    """Response model for maintenance alert."""

    id: str
    vehicle_id: str
    alert_type: str
    mileage: int
    timestamp: str


class VehicleWithAlertsResponse(BaseModel):
    """Response model for vehicle with its alerts."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    plate: str
    model: str
    current_mileage: int
    status: str
    alerts: list[AlertResponse]


# Create app
app = FastAPI(
    title="Automotive Fleet Management API",
    description="API for managing vehicle fleet and maintenance alerts",
    version="1.0.0",
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O restringe a ["http://127.0.0.1:8080"] si prefieres
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Helper functions for DTO mapping
def _map_alert_to_response(alert: MaintenanceAlert) -> AlertResponse:
    """
    Map MaintenanceAlert entity to AlertResponse DTO.

    Args:
        alert: MaintenanceAlert entity

    Returns:
        AlertResponse DTO
    """
    return AlertResponse(
        id=alert.id,
        vehicle_id=alert.vehicle_id,
        alert_type=alert.alert_type.value,
        mileage=alert.mileage,
        timestamp=alert.timestamp.isoformat(),
    )


@app.post(
    "/vehicles",
    response_model=VehicleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_vehicle(request: CreateVehicleRequest, vehicle_repo: SqliteVehicleRepository = Depends(get_vehicle_repository), observer_factory: ObserverFactoryImpl = Depends(get_observer_factory)):
    """
    Create a new vehicle.

    Args:
        request: Vehicle creation data
        vehicle_repo: Vehicle repository injected by FastAPI
        observer_factory: Observer factory injected by FastAPI

    Returns:
        Created vehicle data

    Raises:
        HTTPException: 400 if vehicle with same ID already exists
    """
    try:
        use_case = RegisterVehicleUseCase(vehicle_repository=vehicle_repo, observer_factory=observer_factory)

        # Map web DTO to application DTO
        command = RegisterVehicleCommand(vehicle_id=request.id, plate=request.plate, model=request.model, initial_mileage=request.initial_mileage)

        # Execute use case
        vehicle_dto = use_case.execute(command)

        # Map application DTO to web DTO
        return VehicleResponse(
            id=vehicle_dto.id,
            plate=vehicle_dto.plate,
            model=vehicle_dto.model,
            current_mileage=vehicle_dto.current_mileage,
            status=vehicle_dto.status,
        )
    except DuplicateVehicleException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get(
    "/vehicles",
    response_model=list[VehicleWithAlertsResponse],
    status_code=status.HTTP_200_OK,
)
def get_all_vehicles(status: str | None = Query(None, alias="status"), vehicle_repo: SqliteVehicleRepository = Depends(get_vehicle_repository), alert_repo: SqliteAlertRepository = Depends(get_alert_repository)):
    """
    Get all vehicles with their alerts, optionally filtered by status.

    Args:
        status: Optional status to filter vehicles (active, inactive, in_maintenance, retired)
        vehicle_repo: Vehicle repository injected by FastAPI
        alert_repo: Alert repository injected by FastAPI

    Returns:
        List of all vehicles (or filtered by status) with their alerts ordered by timestamp descending

    Raises:
        HTTPException: 400 if invalid status value provided
    """
    from fastapi import status as http_status

    from src.application.use_cases.get_vehicles_by_status_use_case import GetVehiclesByStatusUseCase
    from src.domain.entities.vehicle_status import VehicleStatus

    # If status filter is provided, use GetVehiclesByStatusUseCase
    if status is not None:
        # Validate and convert status string to enum
        try:
            # Case-insensitive conversion
            status_enum = VehicleStatus(status.lower())
        except ValueError:
            valid_statuses = [s.value for s in VehicleStatus]
            raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=f"Estado inválido '{status}'. Estados válidos: {', '.join(valid_statuses)}")

        # Use GetVehiclesByStatusUseCase for filtering
        use_case = GetVehiclesByStatusUseCase(vehicle_repository=vehicle_repo)
        vehicle_dtos = use_case.execute(status_enum)

        # Convert DTOs to response models (without alerts for filtered results)
        response = []
        for vehicle_dto in vehicle_dtos:
            response.append(
                VehicleWithAlertsResponse(
                    id=vehicle_dto.id,
                    plate=vehicle_dto.plate,
                    model=vehicle_dto.model,
                    current_mileage=vehicle_dto.current_mileage,
                    status=vehicle_dto.status,
                    alerts=[],  # No alerts in filtered response
                )
            )
        return response

    # No filter - use GetAllVehiclesUseCase (original behavior)
    use_case = GetAllVehiclesUseCase(
        vehicle_repository=vehicle_repo,
        alert_repository=alert_repo,
    )
    result = use_case.execute()

    # Convert DTOs to response models
    response = []
    for item in result:
        vehicle_dto = item.vehicle
        alert_dtos = item.alerts

        alert_responses = [
            AlertResponse(
                id=alert_dto.id,
                vehicle_id=alert_dto.vehicle_id,
                alert_type=alert_dto.alert_type,
                mileage=alert_dto.mileage,
                timestamp=alert_dto.timestamp.isoformat(),
            )
            for alert_dto in alert_dtos
        ]

        response.append(
            VehicleWithAlertsResponse(
                id=vehicle_dto.id,
                plate=vehicle_dto.plate,
                model=vehicle_dto.model,
                current_mileage=vehicle_dto.current_mileage,
                status=vehicle_dto.status,
                alerts=alert_responses,
            )
        )

    return response


@app.get("/vehicles/search", response_model=VehicleWithAlertsResponse | list[VehicleWithAlertsResponse], status_code=status.HTTP_200_OK)
def search_vehicle_by_plate(
    plate: str = Query(..., description="License plate to search for (supports partial match)"),
    vehicle_repo: SqliteVehicleRepository = Depends(get_vehicle_repository),
    alert_repo: SqliteAlertRepository = Depends(get_alert_repository)
):
    """
    Search vehicles by plate number (case-insensitive, supports partial match).

    Args:
        plate: License plate or partial plate to search for
        vehicle_repo: Vehicle repository injected by FastAPI
        alert_repo: Alert repository injected by FastAPI

    Returns:
        Single vehicle or list of vehicles matching the plate (with alerts)

    Raises:
        HTTPException: 400 if plate format is invalid, 404 if no vehicles found

    User Story: HU-006 - Búsqueda de vehículos por placa
    Business Rules:
    - RN-010: Plate must follow XXX-123 or XXX-1234 format (for exact matches)
    - RN-031: Search must be case-insensitive
    - RN-032: Search must support partial matches
    - RN-034: Search results must include alerts for each vehicle
    - RN-035: Search results must maintain chronological order of alerts
    """
    from src.application.use_cases.get_vehicle_by_plate_use_case import GetVehicleByPlateUseCase
    from src.domain.exceptions.invalid_plate_exception import InvalidPlateException

    try:
        use_case = GetVehicleByPlateUseCase(vehicle_repository=vehicle_repo)
        result = use_case.execute(plate)

        # Handle both single result and multiple results
        if isinstance(result, list):
            # Multiple vehicles found - include alerts for each
            response_list = []
            for vehicle_dto in result:
                # Get alerts for this vehicle
                alerts = alert_repo.get_by_vehicle_id(vehicle_dto.id)
                # Sort alerts by timestamp descending (most recent first) - RN-035
                alerts_sorted = sorted(alerts, key=lambda a: a.timestamp, reverse=True)

                alert_responses = [
                    AlertResponse(
                        id=alert.id,
                        vehicle_id=alert.vehicle_id,
                        alert_type=alert.alert_type.value,
                        mileage=alert.mileage,
                        timestamp=alert.timestamp.isoformat(),
                    )
                    for alert in alerts_sorted
                ]

                response_list.append(
                    VehicleWithAlertsResponse(
                        id=vehicle_dto.id,
                        plate=vehicle_dto.plate,
                        model=vehicle_dto.model,
                        current_mileage=vehicle_dto.current_mileage,
                        status=vehicle_dto.status,
                        alerts=alert_responses,
                    )
                )
            return response_list
        else:
            # Single vehicle found - include alerts
            alerts = alert_repo.get_by_vehicle_id(result.id)
            # Sort alerts by timestamp descending (most recent first) - RN-035
            alerts_sorted = sorted(alerts, key=lambda a: a.timestamp, reverse=True)

            alert_responses = [
                AlertResponse(
                    id=alert.id,
                    vehicle_id=alert.vehicle_id,
                    alert_type=alert.alert_type.value,
                    mileage=alert.mileage,
                    timestamp=alert.timestamp.isoformat(),
                )
                for alert in alerts_sorted
            ]

            return VehicleWithAlertsResponse(
                id=result.id,
                plate=result.plate,
                model=result.model,
                current_mileage=result.current_mileage,
                status=result.status,
                alerts=alert_responses,
            )
    except InvalidPlateException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except VehicleNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))



@app.get("/vehicles/{vehicle_id}", response_model=VehicleResponse, status_code=status.HTTP_200_OK)
def get_vehicle(vehicle_id: str, vehicle_repo: SqliteVehicleRepository = Depends(get_vehicle_repository)):
    """
    Get vehicle by ID.

    Args:
        vehicle_id: Unique identifier of the vehicle
        vehicle_repo: Vehicle repository injected by FastAPI

    Returns:
        Vehicle data

    Raises:
        HTTPException: 404 if vehicle not found
    """
    try:
        # Use use case instead of direct repository access
        use_case = GetVehicleUseCase(vehicle_repository=vehicle_repo)
        vehicle_dto = use_case.execute(vehicle_id)

        # Map DTO to response
        return VehicleResponse(
            id=vehicle_dto.id,
            plate=vehicle_dto.plate,
            model=vehicle_dto.model,
            current_mileage=vehicle_dto.current_mileage,
            status=vehicle_dto.status,
        )
    except VehicleNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.put("/vehicles/{vehicle_id}/mileage", response_model=VehicleResponse, status_code=status.HTTP_200_OK)
def update_vehicle_mileage(vehicle_id: str, request: UpdateMileageRequest, vehicle_repo: SqliteVehicleRepository = Depends(get_vehicle_repository), observer_factory: ObserverFactoryImpl = Depends(get_observer_factory)):
    """
    Update vehicle mileage.

    Args:
        vehicle_id: Unique identifier of the vehicle
        request: Update mileage request with new mileage value
        vehicle_repo: Vehicle repository injected by FastAPI
        observer_factory: Observer factory injected by FastAPI

    Returns:
        Updated vehicle data

    Raises:
        HTTPException: 400 if invalid mileage, 404 if vehicle not found
    """
    # Create use case with injected dependencies
    use_case = UpdateVehicleMileageUseCase(vehicle_repository=vehicle_repo, observer_factory=observer_factory)

    try:
        # Map to command DTO
        command = UpdateMileageCommand(vehicle_id=vehicle_id, new_mileage=request.new_mileage)

        # Execute use case
        vehicle_dto = use_case.execute(command)

        # Map DTO to response
        return VehicleResponse(
            id=vehicle_dto.id,
            plate=vehicle_dto.plate,
            model=vehicle_dto.model,
            current_mileage=vehicle_dto.current_mileage,
            status=vehicle_dto.status,
        )
    except InvalidMileageException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except VehicleNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.get("/vehicles/{vehicle_id}/alerts", response_model=list[AlertResponse], status_code=status.HTTP_200_OK)
def get_vehicle_alerts(vehicle_id: str, alert_repo: SqliteAlertRepository = Depends(get_alert_repository)):
    """
    Get all alerts for a specific vehicle.

    Args:
        vehicle_id: Unique identifier of the vehicle
        alert_repo: Alert repository injected by FastAPI

    Returns:
        List of maintenance alerts for the vehicle
    """
    # Use use case instead of direct repository access
    use_case = GetVehicleAlertsUseCase(alert_repository=alert_repo)
    alert_dtos = use_case.execute(vehicle_id)

    # Map DTOs to responses
    return [AlertResponse(id=alert_dto.id, vehicle_id=alert_dto.vehicle_id, alert_type=alert_dto.alert_type, mileage=alert_dto.mileage, timestamp=alert_dto.timestamp.isoformat()) for alert_dto in alert_dtos]


@app.delete(
    "/vehicles/{vehicle_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_vehicle(vehicle_id: str, vehicle_repo: SqliteVehicleRepository = Depends(get_vehicle_repository)):
    """
    Delete a vehicle by ID.

    This operation will cascade and delete all associated alerts automatically.

    Args:
        vehicle_id: Unique identifier of the vehicle to delete
        vehicle_repo: Vehicle repository injected by FastAPI

    Raises:
        HTTPException: 404 if vehicle not found

    Returns:
        204 No Content on successful deletion
    """
    try:
        use_case = DeleteVehicleUseCase(vehicle_repository=vehicle_repo)

        # Map to command DTO
        command = DeleteVehicleCommand(vehicle_id=vehicle_id)

        # Execute use case (returns confirmation DTO, but we don't use it for 204 response)
        use_case.execute(command)
    except VehicleNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
