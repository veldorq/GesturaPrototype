'use client';

import { motion } from 'framer-motion';

export default function MinimalHero() {

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
        className="absolute right-20 top-20 text-[12rem] font-jp font-bold text-white pointer-events-none hidden lg:block"
        style={{ writingMode: 'vertical-rl', textOrientation: 'upright' }}
      >
        手
      </motion.div>

      {/* Hero Content */}
      <div className="relative z-10 text-center px-4 max-w-7xl mx-auto">
        {/* Main Title */}
        <motion.h1 className="text-[clamp(2rem,6vw,4rem)] font-light leading-tight mb-6 tracking-tight">
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
          className="text-base md:text-lg text-neutral-400 font-light mb-8 max-w-2xl mx-auto"
        >
          No hardware. No setup. Just your webcam and 30 seconds.
        </motion.p>

        {/* Trust Signals */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.7, duration: 1 }}
          className="flex flex-wrap justify-center gap-6 mb-12 max-w-3xl mx-auto"
        >
          <div className="flex items-center gap-2 text-sm text-neutral-500">
            <svg className="w-5 h-5 text-gestura-cyan" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
            <span className="font-light">100% Local Processing</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-neutral-500">
            <svg className="w-5 h-5 text-gestura-cyan" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            <span className="font-light">Works Offline</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-neutral-500">
            <svg className="w-5 h-5 text-gestura-cyan" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            <span className="font-light">Zero Data Collection</span>
          </div>
        </motion.div>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.8, duration: 1 }}
          className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-4"
        >
          <motion.a
            href="#features"
            onClick={(e) => {
              e.preventDefault();
              document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' });
            }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-10 py-4 border border-white text-white hover:bg-white hover:text-black transition-all duration-300 rounded-full font-light tracking-wide cursor-pointer"
          >
            Get Started
          </motion.a>
          
          <motion.a
            href="https://github.com/veldorq/GesturaPrototype/releases"
            target="_blank"
            rel="noopener noreferrer"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-10 py-4 text-white/60 hover:text-white transition-colors duration-300 font-light tracking-wide"
          >
            Download Now
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
    </section>
  );
}
