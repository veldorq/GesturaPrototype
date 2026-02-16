'use client';

import { motion } from 'framer-motion';

export default function MinimalNav() {
  return (
    <motion.nav
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="fixed top-0 left-0 right-0 z-50 px-8 py-6 flex justify-between items-center mix-blend-difference"
    >
      <div className="text-xl font-light tracking-tight text-white">
        Gestura
      </div>

      <div className="flex gap-6 md:gap-8 text-xs md:text-sm uppercase tracking-widest text-white">
        <a 
          href="#features" 
          onClick={(e) => {
            e.preventDefault();
            document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' });
          }}
          className="relative group cursor-pointer"
        >
          <span>Features</span>
          <span className="absolute bottom-0 left-0 w-0 h-px bg-white transition-all duration-300 group-hover:w-full" />
        </a>
        <a 
          href="#how-it-works" 
          onClick={(e) => {
            e.preventDefault();
            document.getElementById('how-it-works')?.scrollIntoView({ behavior: 'smooth' });
          }}
          className="relative group cursor-pointer"
        >
          <span>How It Works</span>
          <span className="absolute bottom-0 left-0 w-0 h-px bg-white transition-all duration-300 group-hover:w-full" />
        </a>
        <a href="https://github.com/veldorq/GesturaPrototype/releases" target="_blank" rel="noopener noreferrer" className="relative group cursor-pointer">
          <span>Download</span>
          <span className="absolute bottom-0 left-0 w-0 h-px bg-white transition-all duration-300 group-hover:w-full" />
        </a>
      </div>
    </motion.nav>
  );
}
