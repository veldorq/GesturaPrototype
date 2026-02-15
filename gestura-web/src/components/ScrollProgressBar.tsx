'use client';

import { motion, useScroll, useSpring } from 'framer-motion';

export default function ScrollProgressBar() {
  const { scrollYProgress } = useScroll();
  
  // Add spring physics for smoother animation
  const scaleX = useSpring(scrollYProgress, {
    stiffness: 100,
    damping: 30,
    restDelta: 0.001
  });

  return (
    <>
      {/* Progress Bar */}
      <motion.div
        className="fixed top-0 left-0 right-0 h-1 bg-gradient-to-r from-gestura-cyan via-gestura-purple to-gestura-cyan origin-left z-50 shadow-lg shadow-gestura-cyan/50"
        style={{ scaleX }}
      />
      
      {/* Glow Effect */}
      <motion.div
        className="fixed top-0 left-0 right-0 h-2 bg-gradient-to-r from-gestura-cyan/30 via-gestura-purple/30 to-gestura-cyan/30 origin-left z-40 blur-sm"
        style={{ scaleX }}
      />
    </>
  );
}
