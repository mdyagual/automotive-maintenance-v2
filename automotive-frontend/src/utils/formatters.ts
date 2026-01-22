export const formatNumber = (num: number): string => {
  return num.toLocaleString('es-CO');
};

export const formatDate = (isoString: string): string => {
  const date = new Date(isoString);
  return date.toLocaleString('es-CO', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

export const getAlertTypeText = (alertType: string): string => {
  const types: Record<string, string> = {
    'BASIC': 'Mantenimiento Básico (cada 10,000 km)',
    'MAJOR': 'Mantenimiento Mayor (cada 50,000 km)',
    'CRITICAL': 'Umbral Crítico (≥100,000 km)',
  };
  return types[alertType] || alertType;
};

export const getAlertBadgeClass = (alertCount: number): string => {
  if (alertCount === 0) return 'badge-success';
  if (alertCount <= 2) return 'badge-warning';
  return 'badge-error';
};

export const getAlertIcon = (alertCount: number): string => {
  return alertCount === 0 ? '✓' : '⚠️';
};

export const getAlertItemClass = (alertType: string): string => {
  const classes: Record<string, string> = {
    'BASIC': 'alert-basic',
    'MAJOR': 'alert-major',
    'CRITICAL': 'alert-critical',
  };
  return classes[alertType] || '';
};

export const getAlertItemIcon = (alertType: string): string => {
  const icons: Record<string, string> = {
    'BASIC': 'ℹ️',
    'MAJOR': '⚠️',
    'CRITICAL': '🚨',
  };
  return icons[alertType] || 'ℹ️';
};

// HU-005: Vehicle Status Utilities
export const getStatusText = (status: string): string => {
  const statusTexts: Record<string, string> = {
    'active': 'Activo',
    'inactive': 'Inactivo',
    'in_maintenance': 'En Mantenimiento',
    'retired': 'Retirado',
  };
  return statusTexts[status] || status;
};

export const getStatusBadgeClass = (status: string): string => {
  const classes: Record<string, string> = {
    'active': 'status-badge-active',
    'inactive': 'status-badge-inactive',
    'in_maintenance': 'status-badge-maintenance',
    'retired': 'status-badge-retired',
  };
  return classes[status] || 'status-badge-inactive';
};

export const getStatusIcon = (status: string): string => {
  const icons: Record<string, string> = {
    'active': '✓',
    'inactive': '⏸',
    'in_maintenance': '🔧',
    'retired': '🚫',
  };
  return icons[status] || '•';
};
