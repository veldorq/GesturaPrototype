'use client';

import { useEffect, useRef } from 'react';

export default function CustomCursor() {
  const dotRef = useRef<HTMLDivElement>(null);
  const outlineRef = useRef<HTMLDivElement>(null);
  const rafRef = useRef<number>();

  useEffect(() => {
    // Only enable on desktop with fine pointer
    const mediaQuery = window.matchMedia('(pointer: fine)');
    if (!mediaQuery.matches) return;

    // Add cursor-enabled class to body
    document.body.classList.add('cursor-enabled');

    const dot = dotRef.current;
    const outline = outlineRef.current;
    if (!dot || !outline) return;

    let mouseX = 0;
    let mouseY = 0;
    let outlineX = 0;
    let outlineY = 0;
    let isAnimating = false;

    // Mouse move handler (passive for better performance)
    const handleMouseMove = (e: MouseEvent) => {
      mouseX = e.clientX;
      mouseY = e.clientY;

      // Update dot position immediately
      if (dot) {
        dot.style.left = `${mouseX}px`;
        dot.style.top = `${mouseY}px`;
      }

      // Start animation if not already running
      if (!isAnimating) {
        isAnimating = true;
        animateOutline();
      }
    };

    // Smooth outline animation
    const animateOutline = () => {
      // Lerp for smooth following
      outlineX += (mouseX - outlineX) * 0.15;
      outlineY += (mouseY - outlineY) * 0.15;

      if (outline) {
        outline.style.left = `${outlineX}px`;
        outline.style.top = `${outlineY}px`;
      }

      rafRef.current = requestAnimationFrame(animateOutline);
    };

    // Hover state handlers
    const handleMouseEnter = () => {
      if (outline) outline.classList.add('hover');
    };

    const handleMouseLeave = () => {
      if (outline) outline.classList.remove('hover');
    };

    // Add event listeners with passive flag
    window.addEventListener('mousemove', handleMouseMove, { passive: true });
    
    // Defer hover listeners setup to reduce blocking time
    const setupHoverListeners = () => {
      const interactiveElements = document.querySelectorAll('a, button, [role="button"]');
      interactiveElements.forEach(el => {
        el.addEventListener('mouseenter', handleMouseEnter, { passive: true } as any);
        el.addEventListener('mouseleave', handleMouseLeave, { passive: true } as any);
      });
      return interactiveElements;
    };

    // Use requestIdleCallback if available, otherwise setTimeout
    let interactiveElements: NodeListOf<Element>;
    if ('requestIdleCallback' in window) {
      requestIdleCallback(() => {
        interactiveElements = setupHoverListeners();
      });
    } else {
      setTimeout(() => {
        interactiveElements = setupHoverListeners();
      }, 100);
    }

    // Cleanup
    return () => {
      document.body.classList.remove('cursor-enabled');
      window.removeEventListener('mousemove', handleMouseMove);
      if (rafRef.current) {
        cancelAnimationFrame(rafRef.current);
      }
      if (interactiveElements) {
        interactiveElements.forEach(el => {
          el.removeEventListener('mouseenter', handleMouseEnter);
          el.removeEventListener('mouseleave', handleMouseLeave);
        });
      }
    };
  }, []);

  return (
    <>
      <div ref={dotRef} className="cursor-dot" />
      <div ref={outlineRef} className="cursor-outline" />
    </>
  );
}
