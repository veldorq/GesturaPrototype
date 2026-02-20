'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';

export default function MinimalFooter() {
  return (
    <footer className="relative py-16 px-6 border-t border-white/5">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-center gap-6 md:gap-8">
          {/* Logo */}
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-lg md:text-xl font-light tracking-tight"
          >
            <Link href="/" className="hover:opacity-80 transition-opacity">
              Gestura
            </Link>
          </motion.div>

          {/* Links */}
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="flex gap-8 text-sm text-neutral-500"
          >
            <Link href="/download" className="hover:text-white transition-colors cursor-pointer">
              Download
            </Link>
            <Link href="/features" className="hover:text-white transition-colors cursor-pointer">
              Features
            </Link>
            <Link href="/how-it-works" className="hover:text-white transition-colors cursor-pointer">
              How It Works
            </Link>
          </motion.div>

          {/* Copyright */}
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="text-sm text-neutral-600 font-light"
          >
            © 2026 Gestura
          </motion.div>
        </div>

        {/* Tagline */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.3 }}
          className="mt-8 text-center text-xs text-neutral-600 tracking-[0.3em] uppercase"
        >
          Hands Speak. System Listens.
        </motion.div>
      </div>
    </footer>
  );
}
