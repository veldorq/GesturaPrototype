'use client';

import { motion } from 'framer-motion';
import { useCases } from '@/data/features';

export default function UseCases() {
  return (
    <section className="py-32 px-4 md:px-8 relative overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gestura-navy-dark" />

      <div className="max-w-7xl mx-auto relative z-10">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-20"
        >
          <h2 className="text-6xl md:text-8xl font-playfair font-bold text-gestura-text-primary mb-6">
            Who <span className="gradient-text">Benefits</span>?
          </h2>
          <p className="text-xl md:text-2xl text-gestura-text-secondary font-inter max-w-3xl mx-auto">
            From presentations to accessibility, Gestura empowers everyone
          </p>
        </motion.div>

        {/* Use Case Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {useCases.map((useCase, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              whileHover={{ scale: 1.05, y: -10 }}
              className="glass-panel rounded-3xl p-8 hover:border-gestura-cyan/50 transition-all duration-500 shadow-xl hover:shadow-2xl group"
            >
              {/* Icon */}
              <motion.div
                whileHover={{ scale: 1.2, rotate: 360 }}
                transition={{ duration: 0.5 }}
                className={`w-20 h-20 flex items-center justify-center rounded-2xl bg-gradient-to-br ${useCase.gradient} border border-gestura-cyan/20 mb-6 text-4xl`}
              >
                {useCase.icon}
              </motion.div>

              {/* Title */}
              <h3 className="text-2xl font-playfair font-bold text-gestura-text-primary mb-3 group-hover:gradient-text transition-all">
                {useCase.title}
              </h3>

              {/* Description */}
              <p className="text-sm text-gestura-text-secondary font-inter leading-relaxed">
                {useCase.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
