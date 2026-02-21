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
    <section ref={containerRef} className="relative py-20 sm:py-24 md:py-32 px-4 sm:px-6 overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-[#0f1419] via-[#1a1f2e] to-[#0f1419]" />

      <div className="max-w-6xl mx-auto relative z-10">
        <div className="grid md:grid-cols-1 gap-16 items-center justify-center">
          {/* Text Content */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 1, ease: [0.16, 1, 0.3, 1] }}
            className="space-y-8 max-w-2xl mx-auto text-center"
          >
            <div className="w-24 h-px bg-gestura-purple mx-auto" />
            
            <p className="text-base text-neutral-400 leading-relaxed font-light">
              Every movement carries intention. Every intention becomes action.
            </p>

            <div className="flex gap-4 items-center text-sm text-neutral-500 justify-center">
              <span className="tracking-[0.2em] uppercase">Philosophy</span>
              <div className="h-px w-24 bg-neutral-800" />
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
