'use client';

import { motion, useMotionValue, useTransform, animate } from 'framer-motion';
import { useEffect, useRef } from 'react';
import { useInView } from 'framer-motion';

interface AnimatedStatProps {
  value: number;
  suffix?: string;
  prefix?: string;
  label: string;
  description?: string;
  delay?: number;
}

function AnimatedStat({ value, suffix = '', prefix = '', label, description, delay = 0 }: AnimatedStatProps) {
  const count = useMotionValue(0);
  const rounded = useTransform(count, (latest) => Math.round(latest));
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: true, margin: '-100px' });

  useEffect(() => {
    if (isInView) {
      const controls = animate(count, value, {
        duration: 2,
        delay,
        ease: 'easeOut'
      });
      return controls.stop;
    }
  }, [isInView, count, value, delay]);

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, scale: 0.5 }}
      animate={isInView ? { opacity: 1, scale: 1 } : {}}
      transition={{ duration: 0.5, delay }}
      className="text-center group"
    >
      <div className="relative inline-block">
        <motion.div className="text-4xl md:text-5xl font-space font-semibold gradient-text mb-2 group-hover:scale-110 transition-transform inline-block">
          {prefix}
          <motion.span>{rounded}</motion.span>
          {suffix}
        </motion.div>
      </div>
      <div className="text-gestura-text-secondary font-inter uppercase tracking-wider text-sm font-semibold mb-1">
        {label}
      </div>
      {description && (
        <div className="text-gestura-text-secondary/60 font-inter text-xs">
          {description}
        </div>
      )}
    </motion.div>
  );
}

interface AnimatedStatsProps {
  stats: Array<{
    value: number;
    suffix?: string;
    prefix?: string;
    label: string;
    description?: string;
  }>;
  title?: string;
  subtitle?: string;
}

export default function AnimatedStats({ stats, title, subtitle }: AnimatedStatsProps) {
  return (
    <section className="relative py-24 bg-[#0A0118] overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-1/2 left-1/4 w-64 h-64 bg-gestura-cyan rounded-full blur-[100px]" />
        <div className="absolute top-1/2 right-1/4 w-64 h-64 bg-gestura-purple rounded-full blur-[100px]" />
      </div>

      <div className="relative max-w-7xl mx-auto px-6">
        {title && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-space font-semibold gradient-text mb-4">
              {title}
            </h2>
            {subtitle && (
              <p className="text-lg text-gestura-text-secondary font-inter max-w-2xl mx-auto">
                {subtitle}
              </p>
            )}
          </motion.div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 md:gap-16">
          {stats.map((stat, index) => (
            <AnimatedStat
              key={index}
              {...stat}
              delay={index * 0.2}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
