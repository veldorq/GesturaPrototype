'use client';

import { motion } from 'framer-motion';

export default function MinimalCTA() {
  return (
    <section className="relative py-32 px-6">
      <div className="max-w-5xl mx-auto text-center relative z-10">
        {/* Main Heading */}
        <motion.h2
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-4xl md:text-6xl font-light leading-tight mb-12"
        >
          Code With <span className="gradient-text">Clarity</span>
        </motion.h2>

        {/* Stats Row */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2 }}
          className="flex flex-wrap justify-center gap-12 md:gap-20 mb-16"
        >
          {[
            { value: '<30ms', label: 'Response Time' },
            { value: '5,000+', label: 'Active Users'  },
            { value: '100%', label: 'Privacy First' },
          ].map((stat, i) => (
            <motion.div
              key={i}
              whileHover={{ scale: 1.1 }}
              className="text-center cursor-pointer"
            >
              <div className="text-4xl font-light gradient-text mb-2">
                {stat.value}
              </div>
              <div className="text-xs text-neutral-500 uppercase tracking-[0.2em]">
                {stat.label}
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.4 }}
          className="flex flex-col sm:flex-row gap-4 justify-center items-center"
        >
          <motion.a
            href="/download"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-10 py-4 bg-white text-black hover:bg-gestura-cyan transition-all duration-300 rounded-full font-medium"
          >
            Download Now
          </motion.a>

          <motion.a
            href="/dashboard"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-10 py-4 border border-white/20 text-white hover:border-white transition-all duration-300 rounded-full font-light"
          >
            Try Demo
          </motion.a>
        </motion.div>

        {/* Decorative Line */}
        <motion.div
          initial={{ scaleX: 0 }}
          whileInView={{ scaleX: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.6, duration: 1 }}
          className="mt-20 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent"
        />
      </div>
    </section>
  );
}
