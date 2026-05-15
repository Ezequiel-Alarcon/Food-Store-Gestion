import { ReactNode } from 'react';

export type CardShadow = 'none' | 'sm' | 'md' | 'lg';
export type CardPadding = 'none' | 'sm' | 'md' | 'lg';

export interface CardProps {
  children: ReactNode;
  shadow?: CardShadow;
  padding?: CardPadding;
  hover?: boolean;
  className?: string;
}

const shadowClasses: Record<CardShadow, string> = {
  none: '',
  sm: 'shadow-sm',
  md: 'shadow-md',
  lg: 'shadow-lg',
};

const paddingClasses: Record<CardPadding, string> = {
  none: '',
  sm: 'p-3',
  md: 'p-4',
  lg: 'p-6',
};

export function Card({
  children,
  shadow = 'md',
  padding = 'md',
  hover = false,
  className = '',
}: CardProps) {
  const hoverClasses = hover
    ? 'transition-all duration-200 hover:shadow-xl hover:-translate-y-0.5 cursor-pointer'
    : '';

  return (
    <div
      className={`
        bg-white rounded-xl
        ${shadowClasses[shadow]}
        ${paddingClasses[padding]}
        ${hoverClasses}
        ${className}
      `}
    >
      {children}
    </div>
  );
}