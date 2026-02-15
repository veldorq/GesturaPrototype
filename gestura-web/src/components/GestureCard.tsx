'use client';

import { motion } from 'framer-motion';
import { GestureFeature } from '@/data/features';

interface GestureCardProps {
  feature: GestureFeature;
  index: number;
}

export default function GestureCard({ feature, index }: GestureCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-100px' }}
      transition={{ duration: 0.6, delay: index * 0.1 }}
      whileHover={{ scale: 1.05, y: -8 }}
      className="glass-panel rounded-3xl p-8 hover:border-gestura-cyan/60 transition-all duration-500 shadow-xl hover:shadow-2xl hover:glow-cyan group"
    >
      {/* Icon & Rating */}
      <div className="flex items-start justify-between mb-6">
        <motion.div
          whileHover={{ scale: 1.2, rotate: 10 }}
          transition={{ type: 'spring', stiffness: 300 }}
          className={`text-6xl bg-gradient-to-br ${feature.color} p-4 rounded-2xl shadow-lg`}
        >
          {feature.icon}
        </motion.div>
        <div className="flex items-center gap-2 bg-gestura-navy-dark/70 px-3 py-1 rounded-full">
          <span className="text-yellow-400 text-lg">★</span>
          <span className="text-gestura-text-primary font-semibold text-sm">{feature.rating}</span>
        </div>
      </div>

      {/* Category Badge */}
      <div className="inline-block px-3 py-1 bg-gestura-purple/20 border border-gestura-purple/40 rounded-full mb-4">
        <span className="text-xs text-gestura-purple font-semibold uppercase tracking-wider">{feature.category}</span>
      </div>

      {/* Title & Description */}
      <h3 className="text-3xl font-playfair font-bold text-gestura-text-primary mb-3 group-hover:gradient-text transition-all duration-300">
        {feature.name}
      </h3>
      <p className="text-sm text-gestura-text-secondary font-inter mb-6 leading-relaxed">
        {feature.description}
      </p>

      {/* Action Button */}
      <motion.div
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className="flex items-center justify-between px-5 py-3 bg-gradient-to-r from-gestura-cyan/20 to-gestura-purple/20 rounded-xl border border-gestura-cyan/30 hover:border-gestura-cyan cursor-pointer transition-all group-hover:glow-cyan"
      >
        <span className="text-gestura-text-primary font-inter font-medium">{feature.action}</span>
        <motion.span
          animate={{ x: [0, 5, 0] }}
          transition={{ repeat: Infinity, duration: 1.5 }}
          className="text-gestura-cyan text-xl"
        >
          →
        </motion.span>
      </motion.div>
    </motion.div>
  );
}
