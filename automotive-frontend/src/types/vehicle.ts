export interface Alert {
  id: string;
  vehicle_id: string;
  alert_type: 'BASIC' | 'MAJOR' | 'CRITICAL';
  mileage: number;
  timestamp: string;
}

export type VehicleStatus = 'active' | 'inactive' | 'in_maintenance' | 'retired';

export interface Vehicle {
  id: string;
  plate: string;
  model: string;
  current_mileage: number;
  status: VehicleStatus;
  alerts: Alert[];
}

export interface CreateVehicleRequest {
  id: string;
  plate: string;
  model: string;
  initial_mileage: number;
}

export interface UpdateMileageRequest {
  new_mileage: number;
}

export interface UpdateStatusRequest {
  new_status: VehicleStatus;
}
