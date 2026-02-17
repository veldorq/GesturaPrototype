'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function MinimalNav() {
  const pathname = usePathname();

  return (
    <motion.nav
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="fixed top-0 left-0 right-0 z-50 px-8 py-6 flex justify-between items-center mix-blend-difference"
      role="navigation"
      aria-label="Main navigation"
    >
      <Link href="/" className="text-xl font-light tracking-tight text-white hover:opacity-80 transition-opacity">
        Gestura
      </Link>

      <div className="flex gap-6 md:gap-8 text-xs md:text-sm uppercase tracking-widest text-white">
        <Link 
          href="/features"
          className="relative group cursor-pointer"
          aria-label="Navigate to features page"
        >
          <span>Features</span>
          <span className={`absolute bottom-0 left-0 h-px bg-white transition-all duration-300 ${pathname === '/features' ? 'w-full' : 'w-0 group-hover:w-full'}`} />
        </Link>
        <Link 
          href="/how-it-works"
          className="relative group cursor-pointer"
          aria-label="Navigate to how it works page"
        >
          <span>How It Works</span>
          <span className={`absolute bottom-0 left-0 h-px bg-white transition-all duration-300 ${pathname === '/how-it-works' ? 'w-full' : 'w-0 group-hover:w-full'}`} />
        </Link>
        <Link 
          href="/download"
          className="relative group cursor-pointer"
          aria-label="Navigate to download page"
        >
          <span>Download</span>
          <span className={`absolute bottom-0 left-0 h-px bg-white transition-all duration-300 ${pathname === '/download' ? 'w-full' : 'w-0 group-hover:w-full'}`} />
        </Link>
      </div>
    </motion.nav>
  );
}
