'use client';

import { motion } from 'framer-motion';
import { featureHighlights } from '@/data/features';

export default function FeatureHighlights() {
  return (
    <section className="py-32 px-4 md:px-8 relative overflow-hidden">
      {/* Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-gestura-navy via-gestura-navy-dark to-gestura-navy opacity-90" />
      
      {/* Radial Glow */}
      <motion.div
        animate={{
          scale: [1, 1.2, 1],
          opacity: [0.3, 0.5, 0.3]
        }}
        transition={{ repeat: Infinity, duration: 8 }}
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gestura-purple/20 rounded-full blur-3xl"
      />

      <div className="max-w-7xl mx-auto relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-16 items-center">
          {/* Left Features */}
          <div className="space-y-10">
            {featureHighlights.filter(f => f.position === 'left').map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -50 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: i * 0.2 }}
                className="glass-panel p-8 rounded-2xl border border-gestura-navy-light/50 hover:border-gestura-cyan/50 transition-all duration-300 group"
              >
                {feature.metric && (
                  <div className="mb-4">
                    <span className="text-5xl font-playfair font-bold gradient-text">
                      {feature.metric}
                    </span>
                    <span className="text-sm text-gestura-text-secondary ml-2 uppercase tracking-wider">
                      {feature.metricLabel}
                    </span>
                  </div>
                )}
                <h3 className="text-3xl font-playfair font-semibold text-gestura-text-primary mb-4 group-hover:gradient-text transition-all">
                  {feature.title}
                </h3>
                <p className="text-sm text-gestura-text-secondary font-inter leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>

          {/* Center: Hand Gesture Visual */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="flex items-center justify-center"
          >
            <div className="relative">
              {/* Rotating Glow Ring */}
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ repeat: Infinity, duration: 20, ease: 'linear' }}
                className="absolute inset-0 bg-gradient-to-r from-gestura-cyan/30 to-gestura-purple/30 rounded-full blur-3xl scale-150"
              />
              
              {/* Pulse Effect */}
              <motion.div
                animate={{
                  scale: [1, 1.2, 1],
                  opacity: [0.5, 0.2, 0.5]
                }}
                transition={{ repeat: Infinity, duration: 3 }}
                className="absolute inset-0 border-4 border-gestura-cyan/40 rounded-full"
              />

              {/* Hand Emoji Container */}
              <motion.div
                animate={{
                  y: [0, -20, 0],
                  rotate: [0, 5, -5, 0]
                }}
                transition={{ repeat: Infinity, duration: 4, ease: 'easeInOut' }}
                className="relative z-10 w-80 h-80 flex items-center justify-center bg-gradient-to-br from-gestura-navy-dark to-gestura-navy rounded-full border-2 border-gestura-cyan/30 shadow-2xl"
              >
                <span className="text-9xl filter drop-shadow-2xl">✋</span>
              </motion.div>

              {/* Orbiting Icons */}
              {['👆', '✊', '🤏', '👈'].map((emoji, i) => (
                <motion.div
                  key={i}
                  animate={{
                    rotate: 360,
                  }}
                  transition={{
                    repeat: Infinity,
                    duration: 10,
                    delay: i * 2.5,
                    ease: 'linear'
                  }}
                  className="absolute top-1/2 left-1/2 w-full h-full"
                  style={{ transformOrigin: 'center' }}
                >
                  <motion.div
                    animate={{
                      scale: [1, 1.3, 1],
                      rotate: [-360, 0, -360]
                    }}
                    transition={{
                      repeat: Infinity,
                      duration: 10,
                      delay: i * 2.5
                    }}
                    className="absolute -top-8 left-1/2 -translate-x-1/2 text-5xl bg-gestura-navy border-2 border-gestura-purple/40 rounded-full p-3 shadow-lg"
                  >
                    {emoji}
                  </motion.div>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Right Features */}
          <div className="space-y-10">
            {featureHighlights.filter(f => f.position === 'right').map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: 50 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: i * 0.2 }}
                className="glass-panel p-8 rounded-2xl border border-gestura-navy-light/50 hover:border-gestura-purple/50 transition-all duration-300 group"
              >
                {feature.metric && (
                  <div className="mb-4">
                    <span className="text-5xl font-playfair font-bold gradient-text">
                      {feature.metric}
                    </span>
                    <span className="text-sm text-gestura-text-secondary ml-2 uppercase tracking-wider">
                      {feature.metricLabel}
                    </span>
                  </div>
                )}
                <h3 className="text-3xl font-playfair font-semibold text-gestura-text-primary mb-4 group-hover:gradient-text transition-all">
                  {feature.title}
                </h3>
                <p className="text-sm text-gestura-text-secondary font-inter leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
