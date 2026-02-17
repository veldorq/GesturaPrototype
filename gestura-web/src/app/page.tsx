'use client';

import { useEffect } from 'react';
import dynamic from 'next/dynamic';
import MinimalNav from '@/components/MinimalNav';
import MinimalHero from '@/components/MinimalHero';

// Premium UI Components
const PremiumCursor = dynamic(() => import('@/components/premium/CustomCursor'), { ssr: false });
const NoiseOverlay = dynamic(() => import('@/components/premium/NoiseOverlay'), { ssr: false });
const GridPattern = dynamic(() => import('@/components/premium/GridPattern'), { ssr: false });
const AmbientLights = dynamic(() => import('@/components/premium/AmbientLights'), { ssr: false });
const ReadingProgress = dynamic(() => import('@/components/premium/ReadingProgress'), { ssr: false });
const PageTransition = dynamic(() => import('@/components/premium/PageTransition'), { ssr: false });

// Lazy load non-critical components with SSR disabled for faster initial load
const ScrollToTop = dynamic(() => import('@/components/ScrollToTop'), { ssr: false });

// Lazy load below-the-fold sections
const MinimalFeatures = dynamic(() => import('@/components/MinimalFeatures'));
const HowItWorks = dynamic(() => import('@/components/HowItWorks'));
const TechStack = dynamic(() => import('@/components/TechStack'));
const TechnicalSpecs = dynamic(() => import('@/components/TechnicalSpecs'));
const GestureLibrary = dynamic(() => import('@/components/GestureLibrary'));
const SystemRequirements = dynamic(() => import('@/components/SystemRequirements'));
const ProblemSolution = dynamic(() => import('@/components/ProblemSolution'));
const FAQ = dynamic(() => import('@/components/FAQ'));
const MinimalCTA = dynamic(() => import('@/components/MinimalCTA'));
const MinimalFooter = dynamic(() => import('@/components/MinimalFooter'));

export default function Home() {
  useEffect(() => {
    // Smooth scroll behavior
    document.documentElement.style.scrollBehavior = 'smooth';
    
    // Prevent FOUC
    document.body.classList.add('loaded');
  }, []);

  return (
    <>
      {/* Premium UI Enhancements */}
      <PageTransition />
      <PremiumCursor />
      <ReadingProgress />
      <NoiseOverlay />
      <GridPattern />
      <AmbientLights />
      <ScrollToTop />

      {/* Navigation Header */}
      <header>
        <MinimalNav />
      </header>

      <main id="main-content" className="bg-[#0a0f1a] min-h-screen overflow-x-hidden relative" tabIndex={-1} role="main">
        {/* Hero Section */}
        <MinimalHero />

        {/* Spacer for breathing room */}
        <div className="h-[10vh] md:h-[15vh]" />

        {/* Features Grid */}
        <section aria-label="Key features of Gestura">
          <MinimalFeatures />
        </section>

        {/* Spacer */}
        <div className="h-[10vh] md:h-[15vh]" />

        {/* How It Works - Detailed Technical Explanation */}
        <section aria-label="How Gestura works">
          <HowItWorks />
        </section>

        {/* Tech Stack */}
        <section aria-label="Technology stack">
          <TechStack />
        </section>

        {/* Spacer */}
        <div className="h-[10vh] md:h-[15vh]" />

        {/* Technical Specifications */}
        <TechnicalSpecs />

        {/* Gesture Library */}
        <GestureLibrary />

        {/* System Requirements */}
        <SystemRequirements />

        {/* Spacer */}
        <div className="h-[10vh] md:h-[15vh]" />

        {/* Problem-Solution */}
        <ProblemSolution />

        {/* FAQ Section */}
        <section aria-label="Frequently asked questions">
          <FAQ />
        </section>

        {/* Spacer */}
        <div className="h-[10vh] md:h-[15vh]" />

        {/* Final CTA */}
        <section aria-label="Download Gestura">
          <MinimalCTA />
        </section>
      </main>

      {/* Footer */}
      <footer role="contentinfo">
        <MinimalFooter />
      </footer>
    </>
  );
}
