'use client';

import { useEffect } from 'react';
import CustomCursor from '@/components/CustomCursor';
import MinimalNav from '@/components/MinimalNav';
import ScrollProgressBar from '@/components/ScrollProgressBar';
import MinimalHero from '@/components/MinimalHero';
import MinimalFeatures from '@/components/MinimalFeatures';
import ParallaxSection from '@/components/ParallaxSection';
import ProblemSolution from '@/components/ProblemSolution';
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

      {/* Navigation */}
      <MinimalNav />

      <main className="bg-[#0a0a0a] min-h-screen overflow-x-hidden">
        {/* Hero Section */}
        <MinimalHero />

        {/* Spacer for breathing room */}
        <div className="h-[20vh]" />

        {/* Features Grid */}
        <MinimalFeatures />

        {/* Spacer */}
        <div className="h-[20vh]" />

        {/* Parallax Philosophy */}
        <ParallaxSection />

        {/* Spacer */}
        <div className="h-[20vh]" />

        {/* Problem-Solution */}
        <ProblemSolution />

        {/* Spacer */}
        <div className="h-[20vh]" />

        {/* Final CTA */}
        <MinimalCTA />

        {/* Footer */}
        <MinimalFooter />
      </main>
    </>
  );
}
