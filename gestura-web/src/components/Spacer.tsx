/**
 * Spacer Component
 * Creates vertical breathing room between sections
 * Part of Phase 1: Premium whitespace implementation
 */

import React from 'react';

interface SpacerProps {
  height?: string;
  className?: string;
}

export default function Spacer({ height = '60vh', className = '' }: SpacerProps) {
  return (
    <div 
      className={`w-full ${className}`}
      style={{ height }}
      aria-hidden="true"
    />
  );
}
