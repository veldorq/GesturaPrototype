'use client';

import { useEffect, useState, useRef } from 'react';

export default function ReadingProgress() {
  const [progress, setProgress] = useState(0);
  const rafRef = useRef<number>();

  useEffect(() => {
    let isScheduled = false;

    const handleScroll = () => {
      // Throttle with requestAnimationFrame for better performance
      if (!isScheduled) {
        isScheduled = true;
        rafRef.current = requestAnimationFrame(() => {
          const windowHeight = window.innerHeight;
          const documentHeight = document.documentElement.scrollHeight - windowHeight;
          const scrolled = window.scrollY;
          const newProgress = Math.min((scrolled / documentHeight) * 100, 100);
          setProgress(newProgress);
          isScheduled = false;
        });
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll(); // Initial calculation

    return () => {
      window.removeEventListener('scroll', handleScroll);
      if (rafRef.current) {
        cancelAnimationFrame(rafRef.current);
      }
    };
  }, []);

  return (
    <div 
      className="progress-bar" 
      style={{ width: `${progress}%` }}
      role="progressbar"
      aria-valuenow={Math.round(progress)}
      aria-valuemin={0}
      aria-valuemax={100}
      aria-label="Reading progress"
    />
  );
}
