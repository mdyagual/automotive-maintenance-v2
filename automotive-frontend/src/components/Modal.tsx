import { ReactNode } from 'react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
  footer?: ReactNode;
  size?: 'small' | 'medium' | 'wide';
}

export const Modal = ({ isOpen, onClose, title, children, footer, size = 'medium' }: ModalProps) => {
  if (!isOpen) return null;

  const sizeClass = size === 'small' ? 'modal-small' : size === 'wide' ? 'modal-wide' : '';

  return (
    <div className="modal active">
      <div className="modal-overlay" onClick={onClose}></div>
      <div className={`modal-content ${sizeClass}`}>
        <div className="modal-header">
          <h2 className="modal-title">{title}</h2>
          <button className="modal-close" onClick={onClose}>
            &times;
          </button>
        </div>
        <div className="modal-body">{children}</div>
        {footer && <div className="modal-footer">{footer}</div>}
      </div>
    </div>
  );
};
