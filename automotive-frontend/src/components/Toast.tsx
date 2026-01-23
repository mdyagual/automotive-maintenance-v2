import type { Toast as ToastType } from '../hooks/useToast';

interface ToastProps {
  toasts: ToastType[];
  onRemove: (id: string) => void;
}

const icons = {
  success: '✅',
  error: '❌',
  warning: '⚠️',
  info: 'ℹ️',
};

export const Toast = ({ toasts }: ToastProps) => {
  return (
    <div className="toast-container">
      {toasts.map((toast) => (
        <div key={toast.id} className={`toast toast-${toast.type}`}>
          <div className="toast-icon">{icons[toast.type]}</div>
          <div className="toast-content">
            <div className="toast-message">{toast.message}</div>
          </div>
        </div>
      ))}
    </div>
  );
};
