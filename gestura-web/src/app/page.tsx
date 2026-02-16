'use client';

import { useEffect } from 'react';
import CustomCursor from '@/components/CustomCursor';
import MinimalNav from '@/components/MinimalNav';
import ScrollProgressBar from '@/components/ScrollProgressBar';
import ScrollToTop from '@/components/ScrollToTop';
import MinimalHero from '@/components/MinimalHero';
import MinimalFeatures from '@/components/MinimalFeatures';
import HowItWorks from '@/components/HowItWorks';
import TechStack from '@/components/TechStack';
import TechnicalSpecs from '@/components/TechnicalSpecs';
import GestureLibrary from '@/components/GestureLibrary';
import SystemRequirements from '@/components/SystemRequirements';
import ParallaxSection from '@/components/ParallaxSection';
import ProblemSolution from '@/components/ProblemSolution';
import FAQ from '@/components/FAQ';
import MinimalCTA from '@/components/MinimalCTA';
import MinimalFooter from '@/components/MinimalFooter';

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
