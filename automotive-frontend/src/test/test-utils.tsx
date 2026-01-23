import { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';

/**
 * Custom render function that wraps components with providers if needed
 * Currently no providers, but can be extended for Context providers, Router, etc.
 */
const customRender = (ui: ReactElement, options?: Omit<RenderOptions, 'wrapper'>) =>
  render(ui, { ...options });

export * from '@testing-library/react';
export { customRender as render };
