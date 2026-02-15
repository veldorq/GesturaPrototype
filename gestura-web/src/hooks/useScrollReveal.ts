/**
 * useScrollReveal Hook
 * Fade in elements as they enter viewport
 * Performance-optimized with IntersectionObserver
 */

import { useEffect, useState, useRef, RefObject } from 'react';

interface ScrollRevealOptions {
  threshold?: number;
  rootMargin?: string;
  once?: boolean; // Animate only once
}

interface ScrollRevealReturn {
  ref: RefObject<HTMLDivElement>;
  isVisible: boolean;
  opacity: number;
  translateY: number;
}

export function useScrollReveal(options: ScrollRevealOptions = {}): ScrollRevealReturn {
  const {
    threshold = 0.3,
    rootMargin = '0px',
    once = true,
  } = options;

  const ref = useRef<HTMLDivElement>(null);
  const [isVisible, setIsVisible] = useState(false);
  const [hasAnimated, setHasAnimated] = useState(false);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    // Check for reduced motion preference
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) {
      setIsVisible(true);
      return;
    }

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          setHasAnimated(true);
          
          if (once) {
            observer.disconnect();
          }
        } else if (!once && hasAnimated) {
          setIsVisible(false);
        }
      },
      {
        threshold,
        rootMargin,
      }
    );

    observer.observe(element);

    return () => {
      observer.disconnect();
    };
  }, [threshold, rootMargin, once, hasAnimated]);

  // Calculate animation values
  const opacity = isVisible ? 1 : 0;
  const translateY = isVisible ? 0 : 30;

  return { ref, isVisible, opacity, translateY };
}

/**
 * useScrollTrigger Hook
 * More granular control with progress value
 */
export function useScrollTrigger(
  callback: (progress: number) => void,
  thresholdSteps: number = 20
) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    // Generate threshold array [0, 0.05, 0.1, ..., 1.0]
    const thresholds = Array.from(
      { length: thresholdSteps + 1 },
      (_, i) => i / thresholdSteps
    );

    const observer = new IntersectionObserver(
      ([entry]) => {
        callback(entry.intersectionRatio);
      },
      { threshold: thresholds }
    );

    observer.observe(element);

    return () => {
      observer.disconnect();
    };
  }, [callback, thresholdSteps]);

  return ref;
}
