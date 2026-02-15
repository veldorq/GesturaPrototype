'use client';

import { motion } from 'framer-motion';
import GestureCard from './GestureCard';
import { gestureFeatures } from '@/data/features';

export default function GestureShowcase() {
  return (
    <section id="features" className="py-32 px-4 md:px-8 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 bg-gradient-to-b from-gestura-navy-dark via-gestura-navy to-gestura-navy-dark opacity-80" />
      
      {/* Floating Hand Icons */}
      {['✋', '👆', '✊', '🤏', '👈', '👉'].map((emoji, i) => (
        <motion.div
          key={i}
          initial={{ y: 0, opacity: 0.1 }}
          animate={{
            y: [0, -30, 0],
            opacity: [0.1, 0.2, 0.1],
            rotate: [0, 10, -10, 0]
          }}
          transition={{
            repeat: Infinity,
            duration: 5 + i,
            delay: i * 0.5
          }}
          className="absolute text-7xl pointer-events-none"
          style={{
            left: `${10 + i * 15}%`,
            top: `${20 + Math.random() * 60}%`
          }}
        >
          {emoji}
        </motion.div>
      ))}

      <div className="max-w-7xl mx-auto relative z-10">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-20"
        >
          <motion.span
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="inline-block px-4 py-2 bg-gestura-cyan/10 border border-gestura-cyan/30 rounded-full text-gestura-cyan text-sm font-semibold uppercase tracking-wider mb-6"
          >
            11 Powerful Gestures
          </motion.span>
          
          <h2 className="text-6xl md:text-8xl font-playfair font-bold gradient-text mb-6">
            Control Everything
          </h2>
          <p className="text-xl md:text-2xl text-gestura-text-secondary font-inter max-w-3xl mx-auto">
            From navigation to media control, discover gestures that transform how you interact with your computer
          </p>
        </motion.div>

        {/* Gesture Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          {gestureFeatures.map((feature, index) => (
            <GestureCard key={feature.id} feature={feature} index={index} />
          ))}
        </div>

        {/* Stats Banner */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="glass-panel rounded-3xl p-12"
        >
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <motion.div
                initial={{ scale: 0 }}
                whileInView={{ scale: 1 }}
                viewport={{ once: true }}
                transition={{ type: 'spring', stiffness: 200 }}
                className="text-6xl md:text-7xl font-playfair font-bold gradient-text mb-3"
              >
                &lt;30ms
              </motion.div>
              <p className="text-gestura-text-secondary font-inter text-lg">Response Time</p>
            </div>
            <div>
              <motion.div
                initial={{ scale: 0 }}
                whileInView={{ scale: 1 }}
                viewport={{ once: true }}
                transition={{ type: 'spring', stiffness: 200, delay: 0.1 }}
                className="text-6xl md:text-7xl font-playfair font-bold gradient-text mb-3"
              >
                99%
              </motion.div>
              <p className="text-gestura-text-secondary font-inter text-lg">Accuracy Rate</p>
            </div>
            <div>
              <motion.div
                initial={{ scale: 0 }}
                whileInView={{ scale: 1 }}
                viewport={{ once: true }}
                transition={{ type: 'spring', stiffness: 200, delay: 0.2 }}
                className="text-6xl md:text-7xl font-playfair font-bold gradient-text mb-3"
              >
                30FPS
              </motion.div>
              <p className="text-gestura-text-secondary font-inter text-lg">Real-Time Tracking</p>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
