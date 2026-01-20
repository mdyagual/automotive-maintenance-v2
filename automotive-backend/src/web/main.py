"""FastAPI application - Web layer."""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field

from src.application.use_cases.delete_vehicle_use_case import DeleteVehicleUseCase
from src.application.use_cases.get_all_vehicles_use_case import GetAllVehiclesUseCase
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
from src.domain.strategies.basic_maintenance_strategy import BasicMaintenanceStrategy
from src.domain.strategies.critical_threshold_strategy import CriticalThresholdStrategy
from src.domain.strategies.major_maintenance_strategy import MajorMaintenanceStrategy
from src.web.dependencies import (
    get_alert_repository,
    get_vehicle_repository,
    initialize_test_data,
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
    alerts: list[AlertResponse]


# Initialize dependencies and test data
initialize_test_data()

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
def create_vehicle(request: CreateVehicleRequest):
    """
    Create a new vehicle.

    Args:
        request: Vehicle creation data

    Returns:
        Created vehicle data

    Raises:
        HTTPException: 400 if vehicle with same ID already exists
    """
    try:
        use_case = RegisterVehicleUseCase(
            vehicle_repository=get_vehicle_repository(),
            alert_repository=get_alert_repository(),
            strategies=[
                BasicMaintenanceStrategy(),
                MajorMaintenanceStrategy(),
                CriticalThresholdStrategy()
            ]
        )
        vehicle = use_case.execute(
            vehicle_id=request.id,
            plate=request.plate,
            model=request.model,
            initial_mileage=request.initial_mileage,
        )

        return VehicleResponse(
            id=vehicle.id,
            plate=vehicle.plate,
            model=vehicle.model,
            current_mileage=vehicle.current_mileage,
        )
    except DuplicateVehicleException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get(
    "/vehicles",
    response_model=list[VehicleWithAlertsResponse],
    status_code=status.HTTP_200_OK,
)
def get_all_vehicles():
    """
    Get all vehicles with their alerts.

    Returns:
        List of all vehicles with their alerts ordered by timestamp descending
    """
    use_case = GetAllVehiclesUseCase(
        vehicle_repository=get_vehicle_repository(),
        alert_repository=get_alert_repository(),
    )
    result = use_case.execute()

    # Convert to response DTOs
    response = []
    for item in result:
        vehicle = item["vehicle"]
        alerts = item["alerts"]

        alert_responses = [_map_alert_to_response(alert) for alert in alerts]

        response.append(
            VehicleWithAlertsResponse(
                id=vehicle.id,
                plate=vehicle.plate,
                model=vehicle.model,
                current_mileage=vehicle.current_mileage,
                alerts=alert_responses,
            )
        )

    return response


@app.get("/vehicles/{vehicle_id}", response_model=VehicleResponse, status_code=status.HTTP_200_OK)
def get_vehicle(vehicle_id: str):
    """
    Get vehicle by ID.

    Args:
        vehicle_id: Unique identifier of the vehicle

    Returns:
        Vehicle data

    Raises:
        HTTPException: 404 if vehicle not found
    """
    try:
        vehicle = get_vehicle_repository().get_by_id(vehicle_id)
        return VehicleResponse(
            id=vehicle.id,
            plate=vehicle.plate,
            model=vehicle.model,
            current_mileage=vehicle.current_mileage
        )
    except VehicleNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.put(
    "/vehicles/{vehicle_id}/mileage",
    response_model=VehicleResponse,
    status_code=status.HTTP_200_OK
)
def update_vehicle_mileage(vehicle_id: str, request: UpdateMileageRequest):
    """
    Update vehicle mileage.

    Args:
        vehicle_id: Unique identifier of the vehicle
        request: Update mileage request with new mileage value

    Returns:
        Updated vehicle data

    Raises:
        HTTPException: 400 if invalid mileage, 404 if vehicle not found
    """
    # Create use case with all strategies
    use_case = UpdateVehicleMileageUseCase(
        vehicle_repository=get_vehicle_repository(),
        alert_repository=get_alert_repository(),
        strategies=[
            BasicMaintenanceStrategy(),
            MajorMaintenanceStrategy(),
            CriticalThresholdStrategy()
        ]
    )

    try:
        use_case.execute(vehicle_id=vehicle_id, new_mileage=request.new_mileage)
        vehicle = get_vehicle_repository().get_by_id(vehicle_id)
        return VehicleResponse(
            id=vehicle.id,
            plate=vehicle.plate,
            model=vehicle.model,
            current_mileage=vehicle.current_mileage
        )
    except InvalidMileageException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except VehicleNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.get(
    "/vehicles/{vehicle_id}/alerts",
    response_model=list[AlertResponse],
    status_code=status.HTTP_200_OK
)
def get_vehicle_alerts(vehicle_id: str):
    """
    Get all alerts for a specific vehicle.

    Args:
        vehicle_id: Unique identifier of the vehicle

    Returns:
        List of maintenance alerts for the vehicle
    """
    all_alerts = get_alert_repository().get_all()
    vehicle_alerts = [alert for alert in all_alerts if alert.vehicle_id == vehicle_id]

    return [
        AlertResponse(
            id=alert.id,
            vehicle_id=alert.vehicle_id,
            alert_type=alert.alert_type.value,
            mileage=alert.mileage,
            timestamp=alert.timestamp.isoformat()
        )
        for alert in vehicle_alerts
    ]


@app.delete(
    "/vehicles/{vehicle_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_vehicle(vehicle_id: str):
    """
    Delete a vehicle by ID.

    This operation will cascade and delete all associated alerts automatically.

    Args:
        vehicle_id: Unique identifier of the vehicle to delete

    Raises:
        HTTPException: 404 if vehicle not found

    Returns:
        204 No Content on successful deletion
    """
    try:
        use_case = DeleteVehicleUseCase(vehicle_repository=get_vehicle_repository())
        use_case.execute(vehicle_id=vehicle_id)
    except VehicleNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
