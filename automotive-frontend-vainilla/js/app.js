/**
 * APP.JS - Lógica principal de la aplicación
 * Sistema de Gestión de Flota Vehicular
 */

// ===================================
// STATE MANAGEMENT
// ===================================
let vehicles = [];
let currentVehicle = null;

// ===================================
// INITIALIZATION
// ===================================
document.addEventListener('DOMContentLoaded', async () => {
    // Setup form listeners
    setupFormListeners();

    // Load initial data
    await loadVehicles();
});

// ===================================
// DATA LOADING
// ===================================
async function loadVehicles() {
    try {
        vehicles = await API.getAllVehicles();
        renderVehicles();
        updateStats();
    } catch (error) {
        showToast('Error al cargar vehículos: ' + error.message, 'error');
        console.error('Error loading vehicles:', error);
    }
}

// ===================================
// RENDERING
// ===================================
function renderVehicles() {
    const grid = document.getElementById('vehiclesGrid');
    const emptyState = document.getElementById('emptyState');

    if (vehicles.length === 0) {
        grid.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }

    grid.style.display = 'grid';
    emptyState.style.display = 'none';

    grid.innerHTML = vehicles.map(vehicle => {
        const alertCount = vehicle.alerts ? vehicle.alerts.length : 0;
        const badgeClass = alertCount === 0 ? 'badge-success' :
                          alertCount <= 2 ? 'badge-warning' : 'badge-error';
        const badgeIcon = alertCount === 0 ? '✓' : '⚠️';

        return `
            <div class="vehicle-card">
                <div class="vehicle-header">
                    <div>
                        <div class="vehicle-id">${vehicle.id}</div>
                        <div class="vehicle-plate">${vehicle.plate}</div>
                    </div>
                    <span class="badge ${badgeClass}" onclick="openAlertsModal('${vehicle.id}')">
                        ${badgeIcon} ${alertCount} ${alertCount === 1 ? 'alerta' : 'alertas'}
                    </span>
                </div>

                <div class="vehicle-model">${vehicle.model}</div>

                <div class="vehicle-mileage">
                    <span class="mileage-icon">📊</span>
                    <div>
                        <div class="mileage-value">${formatNumber(vehicle.current_mileage)} km</div>
                        <div class="mileage-label">Kilometraje actual</div>
                    </div>
                </div>

                <div class="vehicle-actions">
                    <button class="btn btn-small btn-primary" onclick="openUpdateModal('${vehicle.id}')">
                        Actualizar KM
                    </button>
                    <button class="btn btn-small btn-secondary" onclick="openDetailsModal('${vehicle.id}')">
                        Ver Detalles
                    </button>
                    <button class="btn btn-small btn-danger" onclick="openDeleteModal('${vehicle.id}')">
                        Eliminar
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

function updateStats() {
    const totalVehicles = vehicles.length;
    const totalAlerts = vehicles.reduce((sum, v) => sum + (v.alerts ? v.alerts.length : 0), 0);

    document.getElementById('totalVehicles').textContent = totalVehicles;
    document.getElementById('totalAlerts').textContent = totalAlerts;
}

// ===================================
// FORM SETUP
// ===================================
function setupFormListeners() {
    // Create Vehicle Form
    document.getElementById('createForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        await handleCreateVehicle();
    });

    // Update Mileage Form
    document.getElementById('updateForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        await handleUpdateMileage();
    });

    // Real-time validation for update mileage
    document.getElementById('updateNewMileage').addEventListener('input', (e) => {
        validateNewMileage();
    });
}

// ===================================
// MODAL MANAGEMENT
// ===================================
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';

        // Reset forms
        const form = modal.querySelector('form');
        if (form) {
            form.reset();
        }
    }
}

// Make functions available globally
window.openModal = openModal;
window.closeModal = closeModal;

// ===================================
// CREATE VEHICLE
// ===================================
async function handleCreateVehicle() {
    const vehicleData = {
        id: document.getElementById('createId').value.trim(),
        plate: document.getElementById('createPlate').value.trim().toUpperCase(),
        model: document.getElementById('createModel').value.trim(),
        initial_mileage: parseInt(document.getElementById('createMileage').value),
    };

    try {
        await API.createVehicle(vehicleData);
        showToast('Vehículo registrado exitosamente', 'success');
        closeModal('createModal');
        await loadVehicles();
    } catch (error) {
        showToast('Error al registrar vehículo: ' + error.message, 'error');
        console.error('Error creating vehicle:', error);
    }
}

// ===================================
// VIEW DETAILS
// ===================================
function openDetailsModal(vehicleId) {
    const vehicle = vehicles.find(v => v.id === vehicleId);
    if (!vehicle) return;

    document.getElementById('detailId').textContent = vehicle.id;
    document.getElementById('detailPlate').textContent = vehicle.plate;
    document.getElementById('detailModel').textContent = vehicle.model;
    document.getElementById('detailMileage').textContent = formatNumber(vehicle.current_mileage) + ' km';

    openModal('detailsModal');
}

window.openDetailsModal = openDetailsModal;

// ===================================
// UPDATE MILEAGE
// ===================================
function openUpdateModal(vehicleId) {
    const vehicle = vehicles.find(v => v.id === vehicleId);
    if (!vehicle) return;

    currentVehicle = vehicle;

    document.getElementById('updateVehicleId').value = vehicle.id;
    document.getElementById('updateVehicleInfo').textContent = `${vehicle.plate} - ${vehicle.model}`;
    document.getElementById('updateCurrentMileage').textContent = formatNumber(vehicle.current_mileage);
    document.getElementById('updateNewMileage').value = '';
    document.getElementById('updateNewMileage').min = vehicle.current_mileage;

    updateMileageHint(vehicle.current_mileage);

    openModal('updateModal');
}

window.openUpdateModal = openUpdateModal;

function updateMileageHint(currentMileage) {
    const hint = document.getElementById('updateHint');
    hint.textContent = `Debe ser mayor a ${formatNumber(currentMileage)} km`;
}

function validateNewMileage() {
    if (!currentVehicle) return;

    const input = document.getElementById('updateNewMileage');
    const newMileage = parseInt(input.value);

    if (newMileage <= currentVehicle.current_mileage) {
        input.setCustomValidity('El nuevo kilometraje debe ser mayor al actual');
    } else {
        input.setCustomValidity('');
    }
}

async function handleUpdateMileage() {
    const vehicleId = document.getElementById('updateVehicleId').value;
    const newMileage = parseInt(document.getElementById('updateNewMileage').value);

    try {
        await API.updateMileage(vehicleId, newMileage);
        showToast('Kilometraje actualizado exitosamente', 'success');
        closeModal('updateModal');
        await loadVehicles();
    } catch (error) {
        showToast('Error al actualizar kilometraje: ' + error.message, 'error');
        console.error('Error updating mileage:', error);
    }
}

// ===================================
// VIEW ALERTS
// ===================================
async function openAlertsModal(vehicleId) {
    const vehicle = vehicles.find(v => v.id === vehicleId);
    if (!vehicle) return;

    document.getElementById('alertsVehicleInfo').textContent = `${vehicle.plate} - ${vehicle.model}`;

    const alertsList = document.getElementById('alertsList');

    if (!vehicle.alerts || vehicle.alerts.length === 0) {
        alertsList.innerHTML = `
            <div class="no-alerts">
                <div class="no-alerts-icon">✅</div>
                <p>No hay alertas de mantenimiento para este vehículo</p>
            </div>
        `;
    } else {
        alertsList.innerHTML = '<div class="alerts-list">' +
            vehicle.alerts.map(alert => {
                const alertClass = alert.alert_type === 'BASIC' ? 'alert-basic' :
                                  alert.alert_type === 'MAJOR' ? 'alert-major' : 'alert-critical';
                const alertIcon = alert.alert_type === 'BASIC' ? 'ℹ️' :
                                 alert.alert_type === 'MAJOR' ? '⚠️' : '🚨';
                const alertTypeText = getAlertTypeText(alert.alert_type);

                return `
                    <div class="alert-item ${alertClass}">
                        <div class="alert-icon">${alertIcon}</div>
                        <div class="alert-content">
                            <div class="alert-type">${alertTypeText}</div>
                            <div class="alert-mileage">Generada a los ${formatNumber(alert.mileage)} km</div>
                            <div class="alert-timestamp">${formatDate(alert.timestamp)}</div>
                        </div>
                    </div>
                `;
            }).join('') +
            '</div>';
    }

    openModal('alertsModal');
}

window.openAlertsModal = openAlertsModal;

function getAlertTypeText(alertType) {
    const types = {
        'BASIC': 'Mantenimiento Básico (cada 10,000 km)',
        'MAJOR': 'Mantenimiento Mayor (cada 50,000 km)',
        'CRITICAL': 'Umbral Crítico (≥100,000 km)',
    };
    return types[alertType] || alertType;
}

// ===================================
// DELETE VEHICLE
// ===================================
function openDeleteModal(vehicleId) {
    const vehicle = vehicles.find(v => v.id === vehicleId);
    if (!vehicle) return;

    document.getElementById('deleteVehicleId').value = vehicle.id;
    document.getElementById('deleteVehicleInfo').textContent = `${vehicle.plate} - ${vehicle.model}`;

    openModal('deleteModal');
}

window.openDeleteModal = openDeleteModal;

async function confirmDelete() {
    const vehicleId = document.getElementById('deleteVehicleId').value;

    try {
        await API.deleteVehicle(vehicleId);
        showToast('Vehículo eliminado exitosamente', 'success');
        closeModal('deleteModal');
        await loadVehicles();
    } catch (error) {
        showToast('Error al eliminar vehículo: ' + error.message, 'error');
        console.error('Error deleting vehicle:', error);
    }
}

window.confirmDelete = confirmDelete;

// ===================================
// TOAST NOTIFICATIONS
// ===================================
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');

    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️',
    };

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-icon">${icons[type]}</div>
        <div class="toast-content">
            <div class="toast-message">${message}</div>
        </div>
    `;

    container.appendChild(toast);

    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => {
            container.removeChild(toast);
        }, 300);
    }, 3000);
}

// ===================================
// UTILITY FUNCTIONS
// ===================================
function formatNumber(num) {
    return num.toLocaleString('es-CO');
}

function formatDate(isoString) {
    const date = new Date(isoString);
    return date.toLocaleString('es-CO', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    });
}

// ===================================
// BUTTON HANDLER - New Vehicle
// ===================================
document.getElementById('btnNewVehicle')?.addEventListener('click', () => {
    openModal('createModal');
});
