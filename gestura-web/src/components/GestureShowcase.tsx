'use client';

import { motion } from 'framer-motion';
import GestureCard from './GestureCard';
import { gestureFeatures } from '@/data/features';

export default function GestureShowcase() {
  return (
    <section id="features" className="relative py-32 px-4 md:px-8 overflow-hidden">
      {/* Enhanced Background with depth */}
      <div className="absolute inset-0">
        {/* Gradient overlays */}
        <div className="absolute inset-0 bg-gradient-to-b from-gestura-navy-dark via-transparent to-gestura-navy-dark" />
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-gestura-cyan/10 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-gestura-purple/10 rounded-full blur-3xl" />
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        {/* Section Header - Enhanced */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-24"
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="inline-flex items-center gap-2 px-5 py-2 mb-8 bg-gestura-cyan/10 backdrop-blur-sm border border-gestura-cyan/30 rounded-full"
          >
            <div className="w-2 h-2 bg-gestura-cyan rounded-full animate-pulse" />
            <span className="text-gestura-cyan text-sm font-semibold uppercase tracking-wider">
              Powerful Gestures
            </span>
          </motion.div>
          
          <h2 className="text-4xl md:text-5xl font-space font-semibold mb-6">
            <span className="gradient-text">Control Everything</span>
          </h2>
          <p className="text-lg md:text-xl text-gestura-text-secondary font-inter max-w-3xl mx-auto leading-relaxed">
            From navigation to media control, discover gestures that transform  
            <span className="text-white font-medium"> how you interact</span> with your computer
          </p>
        </motion.div>

        {/* Gesture Cards Grid - Better spacing and layout */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-24">
          {gestureFeatures.map((feature, index) => (
            <GestureCard key={feature.id} feature={feature} index={index} />
          ))}
        </div>

        {/* Enhanced Stats Banner */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="relative overflow-hidden rounded-3xl p-1"
        >
          {/* Gradient border effect */}
          <div className="absolute inset-0 bg-gradient-to-r from-gestura-cyan via-gestura-purple to-gestura-cyan opacity-50 blur-xl" />
          
          <div className="relative bg-[#0f1419]/90 backdrop-blur-2xl rounded-3xl p-12">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 sm:gap-12 text-center px-4">
              <motion.div
                initial={{ scale: 0 }}
                whileInView={{ scale: 1 }}
                viewport={{ once: true }}
                transition={{ type: 'spring', stiffness: 200 }}
                className="group"
              >
                <div className="text-3xl sm:text-4xl md:text-5xl font-space font-semibold mb-2">
                  <span className="bg-gradient-to-r from-gestura-cyan to-blue-400 bg-clip-text text-transparent group-hover:scale-110 inline-block transition-transform">
                    &lt;30ms
                  </span>
                </div>
                <p className="text-gestura-text-secondary font-inter font-medium text-sm sm:text-base">
                  Response Time
                </p>
                <p className="text-gestura-text-secondary/60 font-inter text-xs sm:text-sm mt-2">
                  Faster than human perception
                </p>
              </motion.div>

              <motion.div
                initial={{ scale: 0 }}
                whileInView={{ scale: 1 }}
                viewport={{ once: true }}
                transition={{ type: 'spring', stiffness: 200, delay: 0.1 }}
                className="group"
              >
                <div className="text-3xl sm:text-4xl md:text-5xl font-space font-semibold mb-2">
                  <span className="bg-gradient-to-r from-gestura-purple to-pink-400 bg-clip-text text-transparent group-hover:scale-110 inline-block transition-transform">
                    99%
                  </span>
                </div>
                <p className="text-gestura-text-secondary font-inter font-medium text-sm sm:text-base">
                  Accuracy Rate
                </p>
                <p className="text-gestura-text-secondary/60 font-inter text-xs sm:text-sm mt-2">
                  Reliable gesture recognition
                </p>
              </motion.div>

              <motion.div
                initial={{ scale: 0 }}
                whileInView={{ scale: 1 }}
                viewport={{ once: true }}
                transition={{ type: 'spring', stiffness: 200, delay: 0.2 }}
                className="group"
              >
                <div className="text-3xl sm:text-4xl md:text-5xl font-space font-semibold mb-2">
                  <span className="bg-gradient-to-r from-gestura-cyan to-gestura-purple bg-clip-text text-transparent group-hover:scale-110 inline-block transition-transform">
                    30 FPS
                  </span>
                </div>
                <p className="text-gestura-text-secondary font-inter font-medium text-sm sm:text-base">
                  Real-Time Tracking
                </p>
                <p className="text-gestura-text-secondary/60 font-inter text-xs sm:text-sm mt-2">
                  Smooth, responsive control
                </p>
              </motion.div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
