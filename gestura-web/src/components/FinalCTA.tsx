'use client';

import { motion } from 'framer-motion';

export default function FinalCTA() {
  return (
    <section className="py-40 px-4 relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-gestura-navy to-gestura-navy-dark" />
      
      {/* Animated Glow Orbs */}
      <motion.div
        animate={{
          scale: [1, 1.3, 1],
          opacity: [0.3, 0.6, 0.3]
        }}
        transition={{ repeat: Infinity, duration: 8 }}
        className="absolute top-1/4 left-1/4 w-96 h-96 bg-gestura-cyan/20 rounded-full blur-3xl"
      />
      <motion.div
        animate={{
          scale: [1, 1.2, 1],
          opacity: [0.3, 0.5, 0.3]
        }}
        transition={{ repeat: Infinity, duration: 10, delay: 2 }}
        className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-gestura-purple/20 rounded-full blur-3xl"
      />

      <div className="max-w-5xl mx-auto text-center relative z-10">
        {/* Main Heading */}
        <motion.h2
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-6xl md:text-8xl lg:text-9xl font-playfair font-bold gradient-text mb-8 leading-tight"
        >
          Ready to Experience Gestura?
        </motion.h2>

        {/* Subheading */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2 }}
          className="text-xl md:text-2xl text-gestura-text-secondary mb-16 font-inter"
        >
          Join thousands empowering their workflow with gesture control
        </motion.p>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.4 }}
          className="flex flex-col sm:flex-row gap-6 justify-center items-center"
        >
          <motion.a
            href="/download"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="group px-12 py-6 bg-gradient-to-r from-gestura-cyan to-gestura-purple text-white text-xl font-semibold font-inter rounded-full shadow-2xl glow-cyan hover:glow-purple transition-all flex items-center gap-3"
          >
            Download Now
            <motion.span
              animate={{ x: [0, 5, 0] }}
              transition={{ repeat: Infinity, duration: 1.5 }}
            >
              →
            </motion.span>
          </motion.a>

          <motion.a
            href="/dashboard"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-12 py-6 glass-panel border-2 border-gestura-cyan/50 text-gestura-text-primary text-xl font-semibold font-inter rounded-full hover:border-gestura-cyan transition-all"
          >
            Try Demo
          </motion.a>
        </motion.div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.6 }}
          className="mt-20 flex flex-wrap justify-center gap-12"
        >
          {[
            { value: '5,000+', label: 'Active Users' },
            { value: '100%', label: 'Privacy Protected' },
            { value: '2 Min', label: 'Setup Time' }
          ].map((stat, i) => (
            <div key={i} className="text-center">
              <div className="text-4xl font-playfair font-bold gradient-text mb-2">
                {stat.value}
              </div>
              <div className="text-sm text-gestura-text-secondary font-inter uppercase tracking-wider">
                {stat.label}
              </div>
            </div>
          ))}
        </motion.div>

        {/* Decorative Sparkle */}
        <motion.div
          animate={{
            rotate: [0, 360],
            scale: [1, 1.3, 1]
          }}
          transition={{ repeat: Infinity, duration: 6 }}
          className="mt-16 text-gestura-cyan text-5xl"
        >
          ✦
        </motion.div>
      </div>
    </section>
  );
}
