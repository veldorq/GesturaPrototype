'use client';

import { useEffect } from 'react';
import HeroCanvasAnimation from '@/components/HeroCanvasAnimation';
import GestureShowcase from '@/components/GestureShowcase';
import FeatureHighlights from '@/components/FeatureHighlights';
import UseCases from '@/components/UseCases';
import FinalCTA from '@/components/FinalCTA';

export default function Home() {
  useEffect(() => {
    // Smooth scroll behavior
    document.documentElement.style.scrollBehavior = 'smooth';
    
    // Prevent FOUC (Flash of Unstyled Content)
    document.body.classList.add('loaded');
  }, []);

  return (
    <main className="bg-gestura-navy-dark min-h-screen overflow-x-hidden">
      {/* Hero: Scroll-Triggered Canvas Animation */}
      <HeroCanvasAnimation />

      {/* Gesture Features Showcase */}
      <GestureShowcase />

      {/* Feature Highlights with Center Visual */}
      <FeatureHighlights />

      {/* Use Cases Section */}
      <UseCases />

      {/* Final Call-to-Action */}
      <FinalCTA />

      {/* Footer */}
      <footer className="py-8 px-4 border-t border-gestura-navy-light/30 text-center">
        <p className="text-gestura-text-secondary font-inter text-sm">
          © 2026 Gestura. All rights reserved. | <span className="gradient-text font-semibold">Hands Speak. System Listens.</span>
        </p>
      </footer>
    </main>
  );
}
