/**
 * StickyHeader Component
 * Section titles that stick to top and fade as user scrolls past
 * Inspired by StringTune's navigation pattern
 */

'use client';

import React, { useEffect, useRef, useState } from 'react';

interface StickyHeaderProps {
  children: React.ReactNode;
  stickDuration?: string; // How long to stick (e.g., '50vh')
  className?: string;
}

export default function StickyHeader({ 
  children, 
  stickDuration = '50vh',
  className = '' 
}: StickyHeaderProps) {
  const ref = useRef<HTMLDivElement>(null);
  const [opacity, setOpacity] = useState(1);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const handleScroll = () => {
      const rect = element.getBoundingClientRect();
      const windowHeight = window.innerHeight;
      
      // Calculate fade based on position
      // When element is at top (sticky): opacity = 1
      // When element starts leaving viewport: opacity decreases
      const fadeStart = windowHeight * 0.2; // Start fading at 20% from top
      
      if (rect.top <= fadeStart) {
        const fadeProgress = 1 - Math.abs(rect.top) / fadeStart;
        setOpacity(Math.max(0, Math.min(1, fadeProgress)));
      } else {
        setOpacity(1);
      }
    };

    // Throttle scroll with RAF
    let rafId: number;
    const throttledScroll = () => {
      rafId = requestAnimationFrame(handleScroll);
    };

    window.addEventListener('scroll', throttledScroll, { passive: true });
    handleScroll(); // Initial call

    return () => {
      window.removeEventListener('scroll', throttledScroll);
      cancelAnimationFrame(rafId);
    };
  }, []);

  return (
    <div
      ref={ref}
      className={`sticky z-30 ${className}`}
      style={{
        top: '20vh',
        opacity,
        transition: 'opacity 0.1s ease-out',
        minHeight: stickDuration,
      }}
    >
      {children}
    </div>
  );
}
