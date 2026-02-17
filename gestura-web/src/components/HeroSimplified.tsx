/**
 * HeroSimplified Component
 * Premium hero section with enhanced visuals
 * Combines SVG gestures with rich gradient backgrounds
 */

'use client';

import React, { useState } from 'react';
import { useScroll, useTransform, motion } from 'framer-motion';
import DemoChoiceModal from './DemoChoiceModal';

export default function HeroSimplified() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { scrollYProgress } = useScroll();

  // Parallax effects for depth
  const y1 = useTransform(scrollYProgress, [0, 1], [0, -200]);
  const y2 = useTransform(scrollYProgress, [0, 1], [0, -100]);
  const opacity = useTransform(scrollYProgress, [0, 0.5], [1, 0]);
  const scale = useTransform(scrollYProgress, [0, 0.5], [1, 0.95]);

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-[#0A0118]">
      {/* Animated gradient orbs background */}
      <div className="absolute inset-0">
        <motion.div
          style={{ y: y1 }}
          className="absolute top-0 left-1/4 w-96 h-96 bg-gestura-cyan/30 rounded-full blur-3xl"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.3, 0.5, 0.3],
          }}
          transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
        />
        <motion.div
          style={{ y: y2 }}
          className="absolute bottom-0 right-1/4 w-96 h-96 bg-gestura-purple/30 rounded-full blur-3xl"
          animate={{
            scale: [1.2, 1, 1.2],
            opacity: [0.5, 0.3, 0.5],
          }}
          transition={{ duration: 10, repeat: Infinity, ease: 'easeInOut' }}
        />
      </div>

      {/* Grid pattern overlay */}
      <div className="absolute inset-0 opacity-10">
        <div
          className="w-full h-full"
          style={{
            backgroundImage: `linear-gradient(rgba(0, 217, 255, 0.1) 1px, transparent 1px),
                             linear-gradient(90deg, rgba(0, 217, 255, 0.1) 1px, transparent 1px)`,
            backgroundSize: '50px 50px',
          }}
        />
      </div>

      {/* Floating gesture icons */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        {[
          { icon: '✋', x: '10%', y: '20%', delay: 0, duration: 6 },
          { icon: '👆', x: '80%', y: '30%', delay: 1, duration: 7 },
          { icon: '✊', x: '15%', y: '70%', delay: 2, duration: 8 },
          { icon: '🤏', x: '85%', y: '60%', delay: 1.5, duration: 7.5 },
        ].map((item, i) => (
          <motion.div
            key={i}
            className="absolute text-6xl opacity-20"
            style={{ left: item.x, top: item.y }}
            animate={{
              y: [-20, 20, -20],
              rotate: [-10, 10, -10],
              scale: [1, 1.1, 1],
            }}
            transition={{
              duration: item.duration,
              delay: item.delay,
              repeat: Infinity,
              ease: 'easeInOut',
            }}
          >
            {item.icon}
          </motion.div>
        ))}
      </div>

      {/* Hero Content */}
      <motion.div
        className="relative z-10 text-center px-4 max-w-7xl mx-auto"
        style={{ opacity, scale }}
      >
        {/* Badge */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="inline-flex items-center gap-2 px-5 py-2 mb-8 bg-gestura-cyan/10 backdrop-blur-sm border border-gestura-cyan/30 rounded-full"
        >
          <span className="w-2 h-2 bg-gestura-cyan rounded-full animate-pulse" />
          <span className="text-gestura-cyan text-sm font-semibold uppercase tracking-wider">
            AI-Powered Gesture Control
          </span>
        </motion.div>

        {/* Main Headline */}
        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="font-space text-[clamp(2.5rem,8vw,5rem)] font-semibold leading-relaxed mb-6"
        >
          <span className="block bg-gradient-to-r from-gestura-cyan via-white to-gestura-purple bg-clip-text text-transparent py-1">
            HANDS SPEAK.
          </span>
          <span className="block bg-gradient-to-r from-gestura-purple via-white to-gestura-cyan bg-clip-text text-transparent mt-2 py-1">
            SYSTEM LISTENS.
          </span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="text-[clamp(1.25rem,2.5vw,1.75rem)] text-gestura-text-secondary font-inter font-light max-w-4xl mx-auto leading-relaxed mb-12"
        >
          Control your computer with natural hand gestures.
          <br />
          <span className="text-white font-medium">No keyboard. No mouse. Just your hands.</span>
        </motion.p>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="flex flex-col sm:flex-row items-center justify-center gap-6"
        >
          <motion.button
            onClick={() => setIsModalOpen(true)}
            whileHover={{ scale: 1.05, y: -2 }}
            whileTap={{ scale: 0.95 }}
            className="group relative px-10 py-5 bg-gradient-to-r from-gestura-cyan to-gestura-purple rounded-full font-semibold text-lg text-white shadow-2xl shadow-gestura-cyan/50 overflow-hidden"
          >
            <span className="relative z-10 flex items-center gap-3">
              Try Demo
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M5 12h14M12 5l7 7-7 7" />
              </svg>
            </span>
            <div className="absolute inset-0 bg-gradient-to-r from-gestura-purple to-gestura-cyan opacity-0 group-hover:opacity-100 transition-opacity" />
          </motion.button>

          <motion.a
            href="#features"
            whileHover={{ scale: 1.05, y: -2 }}
            whileTap={{ scale: 0.95 }}
            className="px-10 py-5 bg-gestura-navy-light/50 backdrop-blur-sm border border-gestura-cyan/30 rounded-full font-semibold text-lg text-white hover:border-gestura-cyan/60 hover:bg-gestura-navy-light/80 transition-all"
          >
            Explore Features
          </motion.a>
        </motion.div>

        {/* Scroll Indicator */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.2 }}
          className="mt-20 flex flex-col items-center gap-3 text-gestura-cyan/70"
        >
          <motion.div
            animate={{ y: [0, 10, 0] }}
            transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
          >
            <svg
              width="32"
              height="32"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M12 5v14M19 12l-7 7-7-7" />
            </svg>
          </motion.div>
          <span className="text-sm font-inter uppercase tracking-wider">Scroll to explore</span>
        </motion.div>
      </motion.div>

      {/* Demo Choice Modal */}
      <DemoChoiceModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </section>
  );
}
