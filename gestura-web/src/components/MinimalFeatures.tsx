'use client';

import { motion } from 'framer-motion';
import { gestureFeatures } from '../data/features';

export default function MinimalFeatures() {
  return (
    <section id="features" className="relative py-32 px-6 overflow-x-hidden scroll-mt-20">

      <div className="max-w-7xl mx-auto relative z-10">
        {/* Section Title */}
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="mb-16"
        >
          <h2 className="text-3xl md:text-4xl font-light leading-relaxed mb-4">
            <motion.span
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 1, ease: [0.16, 1, 0.3, 1] }}
              className="block"
            >
              ⚡ Flow Control
            </motion.span>
          </h2>
          <div className="w-24 h-px bg-gestura-cyan" />
        </motion.div>

        {/* Feature Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {gestureFeatures.slice(0, 6).map((feature, index) => (
            <motion.div
              key={feature.id}
              initial={{ opacity: 0, y: 60 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{
                duration: 0.6,
                delay: index * 0.1,
                ease: [0.16, 1, 0.3, 1],
              }}
              whileHover={{ y: -5 }}
              className="group relative glass-panel p-8 overflow-hidden rounded-lg"
            >
              {/* Gradient overlay on hover */}
              <div className="absolute inset-0 bg-gradient-to-br from-gestura-cyan/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

              {/* Number */}
              <div className="relative text-gestura-cyan text-sm font-mono mb-4">
                {String(index + 1).padStart(2, '0')}
              </div>

              {/* Icon */}
              <div className="relative text-4xl mb-4">{feature.icon}</div>

              {/* Title */}
              <h3 className="relative text-xl font-light mb-3 group-hover:text-gestura-cyan transition-colors duration-300">
                {feature.name}
              </h3>

              {/* Description */}
              <p className="relative text-neutral-400 text-sm leading-relaxed">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
