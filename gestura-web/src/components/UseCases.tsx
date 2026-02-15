'use client';

import { motion } from 'framer-motion';
import { useCases } from '@/data/features';

export default function UseCases() {
  return (
    <section className="relative py-32 px-4 md:px-8 overflow-hidden">
      {/* Enhanced Background */}
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-gestura-navy-dark" />
        <div className="absolute top-0 right-0 w-96 h-96 bg-gestura-cyan/10 rounded-full blur-3xl" />
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-gestura-purple/10 rounded-full blur-3xl" />
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        {/* Section Header - Enhanced */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-20"
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="inline-flex items-center gap-2 px-5 py-2 mb-8 bg-gestura-purple/10 backdrop-blur-sm border border-gestura-purple/30 rounded-full"
          >
            <span className="text-gestura-purple text-sm font-semibold uppercase tracking-wider">
              Built For Everyone
            </span>
          </motion.div>

          <h2 className="text-4xl md:text-5xl font-space font-semibold text-gestura-text-primary mb-6">
            Who <span className="gradient-text">Benefits</span>?
          </h2>
          <p className="text-lg md:text-xl text-gestura-text-secondary font-inter max-w-3xl mx-auto leading-relaxed">
            From presentations to accessibility,
            <span className="text-white font-medium"> Gestura empowers everyone</span>
          </p>
        </motion.div>

        {/* Use Case Cards - Enhanced */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {useCases.map((useCase, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              whileHover={{ scale: 1.05, y: -10 }}
              className="relative glass-panel rounded-3xl p-8 hover:border-gestura-cyan/50 transition-all duration-500 shadow-xl hover:shadow-2xl group overflow-hidden"
            >
              {/* Gradient Overlay on Hover */}
              <div className={`absolute inset-0 bg-gradient-to-br ${useCase.gradient} opacity-0 group-hover:opacity-100 transition-opacity duration-500`} />

              {/* Content */}
              <div className="relative z-10">
                {/* Icon */}
                <motion.div
                  whileHover={{ scale: 1.2, rotate: 10 }}
                  transition={{ type: 'spring', stiffness: 300 }}
                  className={`w-20 h-20 flex items-center justify-center rounded-2xl bg-gradient-to-br ${useCase.gradient.replace('/20', '/30')} border-2 border-gestura-cyan/30 mb-6 text-4xl shadow-lg group-hover:shadow-xl group-hover:border-white/50 transition-all`}
                >
                  {useCase.icon}
                </motion.div>

                {/* Title */}
                <h3 className="text-2xl font-space font-bold text-gestura-text-primary mb-3 group-hover:text-white transition-all">
                  {useCase.title}
                </h3>

                {/* Description */}
                <p className="text-sm text-gestura-text-secondary font-inter leading-relaxed group-hover:text-white/90 transition-all">
                  {useCase.description}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
