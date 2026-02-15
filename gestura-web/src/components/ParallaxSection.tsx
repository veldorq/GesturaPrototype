'use client';

import { motion, useScroll, useTransform } from 'framer-motion';
import { useRef } from 'react';

export default function ParallaxSection() {
  const containerRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ['start end', 'end start'],
  });

  const y = useTransform(scrollYProgress, [0, 1], ['-20%', '20%']);
  const opacity = useTransform(scrollYProgress, [0, 0.5, 1], [0.5, 1, 0.5]);

  return (
    <section ref={containerRef} className="relative py-32 px-6 overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-[#0a0a0a] via-[#151515] to-[#0a0a0a]" />

      <div className="max-w-6xl mx-auto relative z-10">
        <div className="grid md:grid-cols-2 gap-16 items-center">
          {/* Text Content */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 1, ease: [0.16, 1, 0.3, 1] }}
            className="space-y-8"
          >
            <h2 className="text-3xl md:text-4xl font-light leading-tight">
              To master the gesture is to master the interface.
            </h2>
            
            <div className="w-24 h-px bg-gestura-purple" />
            
            <p className="text-base text-neutral-400 leading-relaxed font-light">
              Every movement carries intention. Every intention becomes action.
            </p>

            <div className="flex gap-4 items-center text-sm text-neutral-500">
              <span className="tracking-[0.2em] uppercase">Philosophy</span>
              <div className="h-px flex-1 bg-neutral-800" />
            </div>
          </motion.div>

          {/* Parallax Image */}
          <motion.div
            style={{ y, opacity }}
            className="relative h-[400px] md:h-[500px] overflow-hidden rounded-lg shadow-2xl"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-gestura-cyan/20 to-gestura-purple/20 mix-blend-overlay z-10" />
            <img
              src="https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800&q=80"
              alt="Gesture philosophy"
              className="absolute inset-0 w-full h-full object-cover opacity-60"
            />
          </motion.div>
        </div>
      </div>
    </section>
  );
}
