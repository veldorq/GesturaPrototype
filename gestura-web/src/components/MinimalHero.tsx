'use client';

import { motion } from 'framer-motion';
import { useState } from 'react';
import DemoChoiceModal from './DemoChoiceModal';

export default function MinimalHero() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Split text animation
  const title = "HANDS SPEAK.";
  const subtitle = "SYSTEM LISTENS.";

  return (
    <section className="relative h-screen flex items-center justify-center overflow-hidden">
      {/* Background with subtle gradient */}
      <div className="absolute inset-0 bg-gradient-radial from-[#1a1a1a] to-[#0a0a0a] z-0" />
      
      {/* Grid lines overlay */}
      <div
        className="absolute inset-0 opacity-20 pointer-events-none"
        style={{
          backgroundImage: `
            linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px)
          `,
          backgroundSize: '100px 100px',
        }}
      />

      {/* Japanese character - decorative */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 0.05 }}
        transition={{ delay: 0.5, duration: 1.5 }}
        className="absolute right-20 top-20 text-[20rem] font-jp font-bold text-white pointer-events-none hidden lg:block"
        style={{ writingMode: 'vertical-rl', textOrientation: 'upright' }}
      >
        手
      </motion.div>

      {/* Hero Content */}
      <div className="relative z-10 text-center px-4 max-w-7xl mx-auto">
        {/* Main Title */}
        <motion.h1 className="text-[clamp(3rem,10vw,8rem)] font-light leading-none mb-8 tracking-tight">
          {title.split('').map((char, i) => (
            <motion.span
              key={i}
              initial={{ opacity: 0, y: 100 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{
                duration: 0.8,
                delay: 0.3 + i * 0.05,
                ease: [0.16, 1, 0.3, 1],
              }}
              className="inline-block"
            >
              {char === ' ' ? '\u00A0' : char}
            </motion.span>
          ))}
          <br />
          {subtitle.split('').map((char, i) => (
            <motion.span
              key={i}
              initial={{ opacity: 0, y: 100 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{
                duration: 0.8,
                delay: 0.8 + i * 0.05,
                ease: [0.16, 1, 0.3, 1],
              }}
              className="inline-block"
            >
              {char === ' ' ? '\u00A0' : char}
            </motion.span>
          ))}
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.5, duration: 1 }}
          className="text-xl text-[#737373] font-light mb-12"
        >
          Control with Elegance, Not Effort.
        </motion.p>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.8, duration: 1 }}
          className="flex flex-col sm:flex-row gap-4 justify-center items-center"
        >
          <motion.button
            onClick={() => setIsModalOpen(true)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-10 py-4 border border-white text-white hover:bg-white hover:text-black transition-all duration-300 rounded-full font-light tracking-wide"
          >
            Experience Demo
          </motion.button>
          
          <motion.a
            href="/download"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-10 py-4 text-white/60 hover:text-white transition-colors duration-300 font-light tracking-wide"
          >
            Download
          </motion.a>
        </motion.div>
      </div>

      {/* Scroll Indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 2.2, duration: 1 }}
        className="absolute bottom-12 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2"
      >
        <span className="text-xs tracking-[0.3em] uppercase text-neutral-500">Scroll</span>
        <motion.div
          animate={{ scaleY: [1, 0.5, 1] }}
          transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
          className="w-px h-16 bg-gradient-to-b from-transparent via-white/50 to-transparent"
        />
      </motion.div>

      {/* Demo Modal */}
      <DemoChoiceModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </section>
  );
}
