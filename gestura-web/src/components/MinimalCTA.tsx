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
          className="text-3xl md:text-4xl font-light leading-tight mb-10"
        >
          Code With <span className="gradient-text">Clarity</span>
        </motion.h2>

        {/* Stats Row */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2 }}
          className="flex flex-wrap justify-center gap-16 mb-16"
        >
          {[
            { value: '<30ms', label: 'Response Time' },
            { value: '99%', label: 'Accuracy Rate'  },
            { value: '100%', label: 'Privacy First' },
          ].map((stat, i) => (
            <motion.div
              key={i}
              whileHover={{ scale: 1.1 }}
              className="text-center cursor-pointer group"
            >
              <div className="text-2xl md:text-3xl font-light gradient-text mb-2 transition-transform group-hover:scale-110">
                {stat.value}
              </div>
              <div className="text-xs text-neutral-500 uppercase tracking-widest">
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
            href="#features"
            onClick={(e) => {
              e.preventDefault();
              document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' });
            }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-10 py-4 bg-white text-black hover:bg-gestura-cyan transition-all duration-300 rounded-full font-medium cursor-pointer"
          >
            Get Started
          </motion.a>

          <motion.a
            href="https://github.com/veldorq/GesturaPrototype/releases"
            target="_blank"
            rel="noopener noreferrer"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-10 py-4 border border-white/20 text-white hover:border-white transition-all duration-300 rounded-full font-light"
          >
            Download Now
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
