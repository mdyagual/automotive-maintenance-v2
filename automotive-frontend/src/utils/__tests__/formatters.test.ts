/**
 * Tests for formatter utility functions
 *
 * Tests number formatting, date formatting, and status/alert utilities
 */

import { describe, it, expect } from 'vitest';
import {
  formatNumber,
  formatDate,
  getAlertTypeText,
  getAlertBadgeClass,
  getAlertIcon,
  getAlertItemClass,
  getAlertItemIcon,
  getStatusText,
  getStatusBadgeClass,
  getStatusIcon,
} from '../formatters';

describe('formatters', () => {
  describe('formatNumber', () => {
    it('should format number with thousands separator', () => {
      expect(formatNumber(1000)).toBe('1.000');
      expect(formatNumber(10000)).toBe('10.000');
      expect(formatNumber(100000)).toBe('100.000');
      expect(formatNumber(1000000)).toBe('1.000.000');
    });

    it('should handle small numbers', () => {
      expect(formatNumber(0)).toBe('0');
      expect(formatNumber(100)).toBe('100');
      expect(formatNumber(999)).toBe('999');
    });

    it('should format numbers with decimals', () => {
      expect(formatNumber(1234.56)).toBe('1.234,56');
    });
  });

  describe('formatDate', () => {
    it('should format ISO date string to Spanish locale', () => {
      const isoDate = '2026-01-20T09:15:00';
      const formatted = formatDate(isoDate);

      // Check that the formatted string contains key elements
      expect(formatted).toContain('2026');
      expect(formatted).toContain('09:15');
      // The month name might vary by locale, so just check it's not empty
      expect(formatted.length).toBeGreaterThan(10);
    });

    it('should handle different months', () => {
      const feb = formatDate('2026-02-15T10:00:00');
      const mar = formatDate('2026-03-15T10:00:00');
      const dec = formatDate('2026-12-25T10:00:00');

      // Just verify they're different and contain the year
      expect(feb).toContain('2026');
      expect(mar).toContain('2026');
      expect(dec).toContain('2026');
      expect(feb).not.toBe(mar);
    });
  });

  describe('getAlertTypeText', () => {
    it('should return correct text for BASIC alert', () => {
      expect(getAlertTypeText('BASIC')).toBe('Mantenimiento Básico (cada 10,000 km)');
    });

    it('should return correct text for MAJOR alert', () => {
      expect(getAlertTypeText('MAJOR')).toBe('Mantenimiento Mayor (cada 50,000 km)');
    });

    it('should return correct text for CRITICAL alert', () => {
      expect(getAlertTypeText('CRITICAL')).toBe('Umbral Crítico (≥100,000 km)');
    });

    it('should return original value for unknown alert type', () => {
      expect(getAlertTypeText('UNKNOWN')).toBe('UNKNOWN');
    });
  });

  describe('getAlertBadgeClass', () => {
    it('should return success class for zero alerts', () => {
      expect(getAlertBadgeClass(0)).toBe('badge-success');
    });

    it('should return warning class for 1-2 alerts', () => {
      expect(getAlertBadgeClass(1)).toBe('badge-warning');
      expect(getAlertBadgeClass(2)).toBe('badge-warning');
    });

    it('should return error class for 3+ alerts', () => {
      expect(getAlertBadgeClass(3)).toBe('badge-error');
      expect(getAlertBadgeClass(5)).toBe('badge-error');
      expect(getAlertBadgeClass(10)).toBe('badge-error');
    });
  });

  describe('getAlertIcon', () => {
    it('should return checkmark for zero alerts', () => {
      expect(getAlertIcon(0)).toBe('✓');
    });

    it('should return warning icon for alerts', () => {
      expect(getAlertIcon(1)).toBe('⚠️');
      expect(getAlertIcon(5)).toBe('⚠️');
    });
  });

  describe('getAlertItemClass', () => {
    it('should return correct class for BASIC alert', () => {
      expect(getAlertItemClass('BASIC')).toBe('alert-basic');
    });

    it('should return correct class for MAJOR alert', () => {
      expect(getAlertItemClass('MAJOR')).toBe('alert-major');
    });

    it('should return correct class for CRITICAL alert', () => {
      expect(getAlertItemClass('CRITICAL')).toBe('alert-critical');
    });

    it('should return empty string for unknown alert type', () => {
      expect(getAlertItemClass('UNKNOWN')).toBe('');
    });
  });

  describe('getAlertItemIcon', () => {
    it('should return correct icon for BASIC alert', () => {
      expect(getAlertItemIcon('BASIC')).toBe('ℹ️');
    });

    it('should return correct icon for MAJOR alert', () => {
      expect(getAlertItemIcon('MAJOR')).toBe('⚠️');
    });

    it('should return correct icon for CRITICAL alert', () => {
      expect(getAlertItemIcon('CRITICAL')).toBe('🚨');
    });

    it('should return default icon for unknown alert type', () => {
      expect(getAlertItemIcon('UNKNOWN')).toBe('ℹ️');
    });
  });

  describe('getStatusText - HU-005', () => {
    it('should return correct text for active status', () => {
      expect(getStatusText('active')).toBe('Activo');
    });

    it('should return correct text for inactive status', () => {
      expect(getStatusText('inactive')).toBe('Inactivo');
    });

    it('should return correct text for in_maintenance status', () => {
      expect(getStatusText('in_maintenance')).toBe('En Mantenimiento');
    });

    it('should return correct text for retired status', () => {
      expect(getStatusText('retired')).toBe('Retirado');
    });

    it('should return original value for unknown status', () => {
      expect(getStatusText('unknown')).toBe('unknown');
    });
  });

  describe('getStatusBadgeClass - HU-005', () => {
    it('should return correct class for active status', () => {
      expect(getStatusBadgeClass('active')).toBe('status-badge-active');
    });

    it('should return correct class for inactive status', () => {
      expect(getStatusBadgeClass('inactive')).toBe('status-badge-inactive');
    });

    it('should return correct class for in_maintenance status', () => {
      expect(getStatusBadgeClass('in_maintenance')).toBe('status-badge-maintenance');
    });

    it('should return correct class for retired status', () => {
      expect(getStatusBadgeClass('retired')).toBe('status-badge-retired');
    });

    it('should return default class for unknown status', () => {
      expect(getStatusBadgeClass('unknown')).toBe('status-badge-inactive');
    });
  });

  describe('getStatusIcon - HU-005', () => {
    it('should return correct icon for active status', () => {
      expect(getStatusIcon('active')).toBe('✓');
    });

    it('should return correct icon for inactive status', () => {
      expect(getStatusIcon('inactive')).toBe('⏸');
    });

    it('should return correct icon for in_maintenance status', () => {
      expect(getStatusIcon('in_maintenance')).toBe('🔧');
    });

    it('should return correct icon for retired status', () => {
      expect(getStatusIcon('retired')).toBe('🚫');
    });

    it('should return default icon for unknown status', () => {
      expect(getStatusIcon('unknown')).toBe('•');
    });
  });
});
