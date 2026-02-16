'use client';

import { useEffect } from 'react';
import dynamic from 'next/dynamic';
import MinimalNav from '@/components/MinimalNav';
import MinimalHero from '@/components/MinimalHero';

// Lazy load non-critical components with SSR disabled for faster initial load
const CustomCursor = dynamic(() => import('@/components/CustomCursor'), { ssr: false });
const ScrollProgressBar = dynamic(() => import('@/components/ScrollProgressBar'), { ssr: false });
const ScrollToTop = dynamic(() => import('@/components/ScrollToTop'), { ssr: false });

// Lazy load below-the-fold sections
const MinimalFeatures = dynamic(() => import('@/components/MinimalFeatures'));
const HowItWorks = dynamic(() => import('@/components/HowItWorks'));
const TechStack = dynamic(() => import('@/components/TechStack'));
const TechnicalSpecs = dynamic(() => import('@/components/TechnicalSpecs'));
const GestureLibrary = dynamic(() => import('@/components/GestureLibrary'));
const SystemRequirements = dynamic(() => import('@/components/SystemRequirements'));
const ParallaxSection = dynamic(() => import('@/components/ParallaxSection'));
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
      {/* Custom Cursor */}
      <CustomCursor />

      {/* Scroll Progress Indicator */}
      <ScrollProgressBar />

      {/* Scroll to Top Button */}
      <ScrollToTop />

      {/* Navigation */}
      <MinimalNav />

      <main className="bg-[#0a0a0a] min-h-screen overflow-x-hidden">
        {/* Hero Section */}
        <MinimalHero />

        {/* Spacer for breathing room */}
        <div className="h-[10vh] md:h-[15vh]" />

        {/* Features Grid */}
        <MinimalFeatures />

        {/* Spacer */}
        <div className="h-[10vh] md:h-[15vh]" />

        {/* How It Works - Detailed Technical Explanation */}
        <HowItWorks />

        {/* Tech Stack */}
        <TechStack />

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

        {/* Parallax Philosophy */}
        <ParallaxSection />

        {/* Spacer */}
        <div className="h-[10vh] md:h-[15vh]" />

        {/* Problem-Solution */}
        <ProblemSolution />

        {/* FAQ Section */}
        <FAQ />

        {/* Spacer */}
        <div className="h-[10vh] md:h-[15vh]" />

        {/* Final CTA */}
        <MinimalCTA />

        {/* Footer */}
        <MinimalFooter />
      </main>
    </>
  );
}
