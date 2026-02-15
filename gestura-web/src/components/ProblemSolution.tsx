'use client';

import { motion } from 'framer-motion';
import { useScrollReveal } from '../hooks/useScrollReveal';

interface ProblemSolutionItem {
  problem: string;
  solution: string;
  icon: string;
}

const comparisons: ProblemSolutionItem[] = [
  {
    problem: 'Constant switching between mouse and keyboard breaks workflow',
    solution: 'Control everything with natural hand gestures without touching anything',
    icon: '⚡'
  },
  {
    problem: 'Giving presentations means being tied to your computer',
    solution: 'Present from anywhere in the room with gesture controls',
    icon: '🎯'
  },
  {
    problem: 'Repetitive strain from hours of mouse clicking',
    solution: 'Reduce physical strain with contactless gesture control',
    icon: '💪'
  },
  {
    problem: 'Difficult for people with limited mobility to use computers',
    solution: 'Accessible computing through simple hand movements',
    icon: '♿'
  }
];

export default function ProblemSolution() {
  const { ref, opacity, translateY } = useScrollReveal();

  return (
    <section className="relative py-32 bg-gestura-navy overflow-hidden">
      {/* Background Gradient Orbs */}
      <div className="absolute top-20 left-10 w-96 h-96 bg-gestura-cyan/10 rounded-full blur-[128px] animate-pulse" />
      <div className="absolute bottom-20 right-10 w-96 h-96 bg-gestura-purple/10 rounded-full blur-[128px] animate-pulse" style={{ animationDelay: '2s' }} />

      <div ref={ref} className="relative max-w-7xl mx-auto px-6">
        {/* Section Header */}
        <motion.div
          style={{ opacity, y: translateY }}
          className="text-center mb-20"
        >
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="inline-flex items-center gap-2 px-4 py-2 mb-6 bg-gestura-purple/10 backdrop-blur-sm border border-gestura-purple/30 rounded-full"
          >
            <span className="w-2 h-2 bg-gestura-purple rounded-full animate-pulse" />
            <span className="text-gestura-purple text-sm font-semibold uppercase tracking-wider">
              The Transformation
            </span>
          </motion.div>

          <h2 className="text-4xl md:text-5xl font-space font-semibold mb-6">
            From <span className="text-red-400">Frustration</span> to{' '}
            <span className="gradient-text">Freedom</span>
          </h2>
          <p className="text-lg md:text-xl text-gestura-text-secondary font-inter max-w-3xl mx-auto leading-relaxed">
            See how Gestura solves the challenges you face
            <span className="text-white font-medium"> every single day</span>
          </p>
        </motion.div>

        {/* Comparison Grid */}
        <div className="space-y-8">
          {comparisons.map((item, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="grid md:grid-cols-2 gap-6"
            >
              {/* Problem Side */}
              <motion.div
                whileHover={{ scale: 1.02, x: -5 }}
                className="relative glass-panel rounded-2xl p-6 border-2 border-red-500/30 hover:border-red-500/50 transition-all overflow-hidden group"
              >
                {/* Red Glow on Hover */}
                <div className="absolute inset-0 bg-gradient-to-br from-red-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />

                <div className="relative flex items-start gap-4">
                  <div className="flex-shrink-0 w-12 h-12 rounded-xl bg-red-500/20 flex items-center justify-center text-2xl border border-red-500/30">
                    ❌
                  </div>
                  <div>
                    <div className="text-xs uppercase tracking-wider text-red-400 font-semibold mb-2">
                      Problem
                    </div>
                    <p className="text-gestura-text-primary font-inter leading-relaxed">
                      {item.problem}
                    </p>
                  </div>
                </div>
              </motion.div>

              {/* Solution Side */}
              <motion.div
                whileHover={{ scale: 1.02, x: 5 }}
                className="relative glass-panel rounded-2xl p-6 border-2 border-gestura-cyan/30 hover:border-gestura-cyan transition-all overflow-hidden group"
              >
                {/* Cyan Glow on Hover */}
                <div className="absolute inset-0 bg-gradient-to-br from-gestura-cyan/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />

                <div className="relative flex items-start gap-4">
                  <div className="flex-shrink-0 w-12 h-12 rounded-xl bg-gradient-to-br from-gestura-cyan to-blue-500 flex items-center justify-center text-2xl shadow-lg shadow-gestura-cyan/50 border border-gestura-cyan/30">
                    {item.icon}
                  </div>
                  <div>
                    <div className="text-xs uppercase tracking-wider text-gestura-cyan font-semibold mb-2">
                      Gestura Solution
                    </div>
                    <p className="text-white font-inter leading-relaxed font-medium">
                      {item.solution}
                    </p>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          ))}
        </div>

        {/* Bottom CTA */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mt-16"
        >
          <motion.a
            href="#demo"
            whileHover={{ scale: 1.05, y: -2 }}
            whileTap={{ scale: 0.95 }}
            className="inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-gestura-cyan to-gestura-purple text-white font-semibold font-inter rounded-full shadow-2xl shadow-gestura-cyan/30"
          >
            Experience the Difference
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </motion.a>
        </motion.div>
      </div>
    </section>
  );
}
